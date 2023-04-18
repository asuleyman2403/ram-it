from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Answer
from .forms import CreateAnswerForm


def main_home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/main_home.html', context)


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def news_home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'news/news_home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 5


class AnswerListView(ListView):
    model = Answer
    template_name = 'blog/post_detail.html'
    context_object_name = 'answer'
    ordering = ['-date_posted']
    # paginate_by = 5


class MainListView(ListView):
    model = Post
    template_name = 'blog/main_home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')    


def post_detail_page(request, pk):
        post = Post.objects.get(id=pk)
        answers = Answer.objects.filter(post_id=post.id)
        form = CreateAnswerForm()
        return render(request, 'blog/post_detail.html', {'object': post, 'user': request.user, 'form': form,
                                                         'answers': answers})


def create_posts_answer(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(id=pk)
        if request.method == 'POST':
            form = CreateAnswerForm(request.POST)
            if form.is_valid():
                content = form.data.get('content')
                answer = Answer(content=content, author_id=request.user.id, post_id=pk)
                answer.save()
                return redirect('/post/' + str(pk) + '/')
            else:
                answers = Answer.objects.filter(post_id=post.id)
                return render(request, 'blog/post_detail.html', {'object': post, 'user': request.user, 'form': form,
                                                                 'answers': answers})

    else:
        return redirect('/')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'О сайте'})
