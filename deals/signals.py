from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Comment, CommentVote, Deal, DealVote, SCORE_UP


@receiver(post_save, sender=Deal)
def deal_post_save_handler(instance, created, **kwargs):

    # Create a positive DealVote for the author
    if created:
        DealVote(
            deal=instance,
            user=instance.created_by,
            score=SCORE_UP
        ).save()


@receiver(post_save, sender=Comment)
def comment_post_save_handler(instance, created, **kwargs):

    # Create a positive CommentVote for the author
    if created:
        CommentVote(
            comment=instance,
            user=instance.created_by,
            score=SCORE_UP
        ).save()


@receiver(post_save, sender=DealVote)
def dealvote_post_save_handler(instance, **kwargs):

    # Update the Deal's score
    instance.deal.update_score()


@receiver(post_delete, sender=DealVote)
def dealvote_post_delete_handler(instance, **kwargs):

    # Update the Deal's score
    instance.deal.update_score()
