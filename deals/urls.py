from django.urls import path

from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.DealListView.as_view(), name='deal_list'),
    path('submit/', views.DealEditView.as_view(), name='deal_submit'),
    path('<int:pk>/', views.DealView.as_view(), name='deal'),
    path('<int:pk>/edit/', views.DealEditView.as_view(), name='deal_edit'),
    path('<int:pk>/vote/<str:action>/', views.VoteDealView.as_view(), name='deal_vote'),
    path('comments/<int:pk>/vote/<str:action>/', views.VoteCommentView.as_view(), name='comment_vote'),
]
