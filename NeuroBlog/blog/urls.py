from django.urls import path
from .views import MainView, PostDetailView, SearchResultsView, TagView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug>/', TagView.as_view(), name="tag"),
]
