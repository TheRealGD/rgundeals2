from urllib.parse import urlparse

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils import timezone
from markdown import markdown
from mptt.models import MPTTModel, TreeForeignKey, TreeManager


COLOR_CHOICES = (
    ('aa1409', 'Dark red'),
    ('f44336', 'Red'),
    ('e91e63', 'Pink'),
    ('ff66ff', 'Fuschia'),
    ('9c27b0', 'Purple'),
    ('673ab7', 'Dark purple'),
    ('3f51b5', 'Indigo'),
    ('2196f3', 'Blue'),
    ('03a9f4', 'Light blue'),
    ('00bcd4', 'Cyan'),
    ('009688', 'Teal'),
    ('2f6a31', 'Dark green'),
    ('4caf50', 'Green'),
    ('8bc34a', 'Light green'),
    ('cddc39', 'Lime'),
    ('ffeb3b', 'Yellow'),
    ('ffc107', 'Amber'),
    ('ff9800', 'Orange'),
    ('ff5722', 'Dark orange'),
    ('795548', 'Brown'),
    ('c0c0c0', 'Light grey'),
    ('9e9e9e', 'Grey'),
    ('607d8b', 'Dark grey'),
    ('111111', 'Black'),
)


SCORE_UP = 1
SCORE_DOWN = -1
SCORE_CHOICES = (
    (SCORE_UP, 'Up'),
    (SCORE_DOWN, 'Down'),
)


class Vendor(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Company name"
    )
    slug = models.SlugField(
        unique=True
    )
    url = models.URLField(
        verbose_name='URL',
        help_text="Public-facing website"
    )
    domains = ArrayField(
        base_field=models.CharField(max_length=100),
        help_text="URLs matching any of these domains will be associated with this vendor"
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '{}?vendor={}'.format(reverse('deals:deal_list'), self.slug)


class Category(MPTTModel):
    parent = TreeForeignKey(
        to='self',
        related_name='children',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=50,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )
    color = models.CharField(
        max_length=6,
        choices=COLOR_CHOICES
    )

    class Meta:
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by=('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '{}?category={}'.format(reverse('deals:deal_list'), self.slug)


class Deal(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        to='users.User',
        related_name='deals',
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    edited = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )
    edited_by = models.ForeignKey(
        to='users.User',
        related_name='+',
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    title = models.CharField(
        max_length=255
    )
    url = models.URLField(
        max_length=255,
        verbose_name='URL'
    )
    score = models.SmallIntegerField(
        editable=False,
        default=0
    )
    category = models.ForeignKey(
        to='deals.Category',
        related_name='deals',
        on_delete=models.PROTECT
    )
    vendor = models.ForeignKey(
        to='deals.Vendor',
        related_name='deals',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Price in USD'
    )
    qty = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Quantity',
        help_text="The number of items/rounds"
    )
    discount = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text='Fixed percentage discount'
    )
    expires = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The date/time which this deal expires"
    )
    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        help_text="Code required for discount"
    )
    locked = models.BooleanField(
        default=False,
        help_text="The submitter is not allowed to make changes"
    )
    out_of_stock = models.BooleanField(
        default=False,
        help_text="This product is no longer in stock"
    )
    description = models.TextField(
        blank=True,
        max_length=4000
    )
    description_rendered = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deals:deal', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()

        # Erase single/zero quantity
        if self.qty in [0, 1]:
            self.qty = None

        # Generate rendered description
        if self.description:
            self.description_rendered = markdown(self.description, extensions=['mdx_gfm'])

    def save(self, *args, **kwargs):

        # Assign vendor based on URL domain upon creation of new deals
        if not self.pk and not self.vendor and self.domain:
            self.vendor = Vendor.objects.filter(domains__contains=[self.domain]).order_by('pk').first()

        return super().save(*args, **kwargs)

    def update_score(self):
        """
        Sum all votes for this Deal and record the score.
        """
        votes_qs = self.votes.aggregate(Sum('score'))
        self.score = votes_qs['score__sum'] or 0  # Sum() returns None for zero
        Deal.objects.filter(pk=self.pk).update(score=self.score)

    @property
    def domain(self):
        """
        Return the top-level domain from the deal's URL.
        """
        if not self.url:
            return None
        domain = urlparse(self.url).netloc
        # TODO: We can come up with a smarter way to identify the TLD
        if domain.startswith('www.'):
            return domain.split('.', 1)[1]
        return domain

    @property
    def unit_price(self):
        if self.qty > 1:
            return '{0:.2f}'.format(self.price / self.qty)
        return self.price

    @property
    def is_expired(self):
        if not self.expires:
            return False
        return self.expires < timezone.now()


class DealVote(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    deal = models.ForeignKey(
        to='deals.Deal',
        related_name='votes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='deal_votes',
        on_delete=models.CASCADE
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES
    )

    class Meta:
        unique_together = ('deal', 'user')


class CommentManager(TreeManager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            score=Coalesce(Sum('votes__score'), 0)
        )


class Comment(MPTTModel):
    created = models.DateTimeField(
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        to='users.User',
        related_name='comments',
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    edited = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )
    edited_by = models.ForeignKey(
        to='users.User',
        related_name='+',
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    deal = models.ForeignKey(
        to='deals.Deal',
        related_name='comments',
        editable=False,
        on_delete=models.CASCADE
    )
    parent = TreeForeignKey(
        to='self',
        related_name='children',
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        on_delete=models.CASCADE
    )
    body = models.TextField(
        max_length=4000
    )
    body_rendered = models.TextField()

    objects = CommentManager()

    class MPTTMeta:
        order_insertion_by = ('created',)

    def clean(self):
        super().clean()

        # Save rendered body
        if self.body:
            self.body_rendered = markdown(self.body, extensions=['mdx_gfm'])


class CommentVote(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    comment = models.ForeignKey(
        to='deals.Comment',
        related_name='votes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='comment_votes',
        on_delete=models.CASCADE
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES
    )

    class Meta:
        unique_together = ('comment', 'user')
