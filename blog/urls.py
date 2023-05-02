from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsView.as_view(), name="main"),
    path('news/<int:category_id>/', views.CategoryNewsView.as_view(), name="category-news"),
    path('profile/<int:user_id>', views.Profile.as_view(), name='profile'),
    path('news/create_news/', views.CreateNews.as_view(), name='create-news'),
    path('news/check_news/', views.CheckNews.as_view(), name='check-news'),
    path('news/check_news/<slug:news_slug>/delete', views.DeleteCheckNews.as_view(), name='delete-check-news'),
    path('news/check_news/<slug:news_slug>', views.ConfirmationNews.as_view(), name='confirmation-news'),
    path('news/<slug:news_slug>/edit_news', views.EditNews.as_view(), name='edit-news'),
    path('news/<slug:news_slug>/delete_news', views.DeleteNews.as_view(), name='delete-news'),

    path('news/<slug:news_slug>', views.NewsDetail.as_view(), name='news-detail'),
    path('news/<slug:news_slug>/new_comment', views.NewComment.as_view(), name='comment'),
    path('news/<int:comment_id>/delete_comment', views.DeleteComment.as_view(), name='delete-comment'),


]


