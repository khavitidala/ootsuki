import re
from hashlib import md5
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files import File
from django.db.models import Q 
from .forms import CreatePost, CommentForm
from .models import Post, Comment, Category

class ManagePostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/manage.html'

class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        cat = self.request.GET.get('cat')
        posts = Post.objects.all().order_by('-updated_at')
        if query or cat:
            if cat:
                posts = Post.objects.filter(category=cat).order_by('-updated_at')
            if query:
                posts = Post.objects.filter(
                    Q(title__icontains=query) | Q(keyword__icontains=query).order_by('-updated_at')
                )
        return posts
    
    def get_context_data(self):
        context = super().get_context_data()
        context['cat_list'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    def get(self, request, pk, templ):
        x = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = {
            'posts': x,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)

class CommentCreateView(View):
    def post(self, request, pk, templ):
        size = 60
        f = get_object_or_404(Post, id=pk)
        email = str(request.POST['email'].strip().lower()).encode('utf-8')
        email_hash = md5(email).hexdigest()
        url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
        ava_url = url.format(email_hash, size)
        comment = Comment(
            name=request.POST['name'],
            comment=request.POST['comment'],
            post=f,
            img_url=ava_url,
            email=request.POST['email']
        )
        comment.save()
        return redirect(reverse('blog:article', args=[pk, templ]))

class ManagePostCreateView(LoginRequiredMixin, View):
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:main')

    def get(self, request, pk=None):
        form = CreatePost()
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        form = CreatePost(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        post = form.save(commit=False)
        post.author = self.request.user
        post.templ_id = post.title.lower().replace(" ", "-")
        post.save()
        return redirect(self.success_url)

class ManagePostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/update.html'
    success_url = reverse_lazy('blog:main')

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk, author=self.request.user)
        form = CreatePost(instance=post)
        ctx = {
            'form':form
        }
        return render(request,self.template_name, ctx)
    
    def post(self, request, pk=None):
        post = get_object_or_404(Post, id=pk, author=self.request.user)
        form = CreatePost(request.POST, instance=post)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.success_url)

class ManagePostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:main")
'''
class SearchListView(ListView):
    model = Post
    template_name = 'blog/search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        cat = self.request.GET.get('cat')

        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(keyword__icontains=query) | Q(category__icontains=cat)
        )
        return object_list
'''





