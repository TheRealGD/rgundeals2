from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from utils.pagination import EnhancedPaginator
from .filters import DealFilter
from .forms import DealForm, ModDealForm
from .models import Category, Comment, CommentVote, Deal, DealVote, SCORE_DOWN, SCORE_UP


#
# Deals
#

class DealListView(View):
    """
    Display a list of deals
    """
    template_name = 'deals/deal_list.html'

    def get(self, request):

        # Retrieve all deals
        # TODO: Implement pagination
        queryset = Deal.objects.select_related(
            'created_by', 'edited_by', 'category'
        ).annotate(
            comment_count=Count('comments')
        )

        # Filter the queryset by request parameters
        queryset = DealFilter(request.GET, queryset).qs

        # Annotate vote information for the current user
        if request.user.is_authenticated:
            deal_votes = DealVote.objects.filter(
                deal__in=queryset, user=request.user
            )
            votes = {v.deal_id: v.score for v in deal_votes}
            for d in queryset:
                d.vote = votes[d.pk] if d.pk in votes else None

        # Paginate deals list
        paginator = EnhancedPaginator(queryset, request.GET.get('per_page'))
        deals = paginator.get_page(request.GET.get('page', 1))

        # Get list of all categories
        categories = Category.objects.add_related_count(
            queryset=Category.objects.all(),
            rel_model=Deal,
            rel_field='category',
            count_attr='deal_count',
            cumulative=True
        )

        return render(request, self.template_name, {
            'deals': deals,
            'categories': categories,
        })


class DealView(View):
    """
    Display a single deal and its comments
    """
    template_name = 'deals/deal.html'

    def get(self, request, pk):

        deal = get_object_or_404(Deal, pk=pk)
        if request.user.is_authenticated:
            try:
                vote = deal.votes.get(user=request.user)
                deal.vote = vote.score
            except DealVote.DoesNotExist:
                deal.vote = None

        comments = deal.comments.select_related(
            'created_by', 'edited_by'
        )

        return render(request, self.template_name, {
            'deal': deal,
            'comments': comments,
        })


class DealEditView(LoginRequiredMixin, View):
    """
    Submit a new deal or edit an existing one.
    """
    template_name = 'deals/deal_edit.html'

    def get(self, request, pk=None):

        deal = get_object_or_404(Deal, pk=pk) if pk else None

        if request.user.is_staff:
            form = ModDealForm(instance=deal)
        else:
            form = DealForm(instance=deal)

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request, pk=None):

        deal = get_object_or_404(Deal, pk=pk) if pk else None

        if request.user.is_staff:
            form = ModDealForm(data=request.POST, instance=deal)
        else:
            form = DealForm(data=request.POST, instance=deal)

        if form.is_valid():

            deal = form.save(commit=False)
            deal.created_by = request.user
            deal.score = 1
            deal.save()

            if pk:
                messages.success(request, 'Updated deal "{}"'.format(deal))
            else:
                messages.success(request, 'Submitted deal "{}"'.format(deal))

            return redirect(deal)

        return render(request, self.template_name, {
            'form': form,
        })


class VoteDealView(LoginRequiredMixin, View):
    """
    Vote on a deal (up, down, or delete)
    """

    def post(self, request, pk, action):

        deal = get_object_or_404(Deal, pk=pk)

        if action not in ['up', 'down', 'delete']:
            return Http404

        if action in ['up', 'down']:

            vote = {
                'up': SCORE_UP,
                'down': SCORE_DOWN,
            }.get(action)

            # Create a new DealVote or update an existing one
            dv, created = DealVote.objects.update_or_create(
                deal=deal,
                user=request.user,
                defaults={'score': vote}
            )

        else:

            # Delete any existing vote on this deal
            DealVote.objects.filter(deal=deal, user=request.user).delete()

        deal = Deal.objects.get(pk=deal.pk)

        return JsonResponse({
            'score': deal.score,
        })


class VoteCommentView(LoginRequiredMixin, View):
    """
    Vote on a comment (up, down, or delete)
    """

    def post(self, request, pk, action):

        comment = get_object_or_404(Comment, pk=pk)

        if action not in ['up', 'down', 'delete']:
            return Http404

        if action in ['up', 'down']:

            vote = {
                'up': SCORE_UP,
                'down': SCORE_DOWN,
            }.get(action)

            # Create a new CommentVote or update an existing one
            dv, created = CommentVote.objects.update_or_create(
                comment=comment,
                user=request.user,
                defaults={'score': vote}
            )

        else:

            # Delete any existing vote on this comment
            CommentVote.objects.filter(comment=comment, user=request.user).delete()

        comment = Comment.objects.get(pk=comment.pk)

        return JsonResponse({
            'score': comment.score,
        })
