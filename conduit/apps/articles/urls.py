from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet, CommentsListCreateAPIView, CommentsDestroyAPIView
    )

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('articles/<article_slug>/comments',
        CommentsListCreateAPIView.as_view()),

    path('articles/<article_slug>/comments/<comment_pk>',
        CommentsDestroyAPIView.as_view()),
]
