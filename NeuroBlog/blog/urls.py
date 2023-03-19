from django import settings
from django.contrib import LogoutView
from django.urls import path
from .views import MainView, PostDetailView, SearchResultsView, TagView, SignUpView, SignInView, update


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug>/', TagView.as_view(), name="tag"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path("update_server/", update, name="update"),
]
