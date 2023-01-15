from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .forms import CommentForm
from .models import Post, HotPost, Comment
from django.db.models import Q
from taggit.models import Tag


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        hot_posts = HotPost.objects.all()
        common_tags = Post.tag.most_common()

        return render(request, 'blog/index.html', context={
            'page_obj': page_obj,
            'hot_posts': hot_posts,
            'common_tags': common_tags,
        })


class PostDetailView(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        hot_posts = HotPost.objects.all()
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        prev_post = post.get_prev_post()
        next_post = post.get_next_post()
        comment_form = CommentForm()

        return render(request, 'blog/post_detail.html', context={
            'post': post,
            'hot_posts': hot_posts,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'prev_post': prev_post,
            'next_post': next_post,
            'comment_form': comment_form
    })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            author = self.request.user
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(post=post, author=author, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'myblog/post_detail.html', context={
            'comment_form': comment_form
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        results = ""
        if query:
            results = Post.objects.filter(
                Q(title__contains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'blog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })
