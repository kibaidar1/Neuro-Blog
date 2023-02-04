from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .forms import CommentForm, SigUpForm, SignInForm, FeedBackForm
from .models import Post, HotPost, Comment
from django.db.models import Q
from taggit.models import Tag


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        last_posts = Post.objects.all().order_by('-id')[:5]
        hot_posts = HotPost.objects.all()
        common_tags = Post.tag.most_common()[:10]

        return render(request, 'blog/index.html', context={
            'page_obj': page_obj,
            'last_posts': last_posts,
            'hot_posts': hot_posts,
            'common_tags': common_tags,
        })


class PostDetailView(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)

        last_posts = Post.objects.all().order_by('-id')[:5]
        hot_posts = HotPost.objects.all()
        common_tags = Post.tag.most_common()

        prev_post = post.get_prev_post()
        next_post = post.get_next_post()
        comment_form = CommentForm()

        return render(request, 'blog/post_detail.html', context={
            'post': post,
            'last_posts': last_posts,
            'hot_posts': hot_posts,
            'common_tags': common_tags,
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
        return render(request, 'blog/post_detail.html', context={
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


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'blog/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signin.html', context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} - {from_email} | {subject}', message, from_email, ['kibaidar1@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form,
        })
