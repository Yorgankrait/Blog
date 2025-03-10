from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Фильтр по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Фильтр по автору
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        
        # Фильтр по дате
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(date_posted__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_posted__lte=date_to)
        
        # Поиск по заголовку и содержимому
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = User.objects.filter(post__isnull=False).distinct()
        if self.request.user.is_authenticated:
            context['favorite_posts'] = self.request.user.favorite_posts.values_list('id', flat=True)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post-detail', pk=pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({
        'likes': post.total_likes(),
        'dislikes': post.total_dislikes()
    })

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return JsonResponse({
        'likes': post.total_likes(),
        'dislikes': post.total_dislikes()
    })

@login_required
def toggle_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
        is_favorite = False
    else:
        post.favorites.add(request.user)
        is_favorite = True
    return JsonResponse({
        'is_favorite': is_favorite,
        'favorites_count': post.favorites.count()
    })

class FavoritePostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/favorites.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(favorites=self.request.user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = User.objects.filter(post__isnull=False).distinct()
        if self.request.user.is_authenticated:
            context['favorite_posts'] = self.request.user.favorite_posts.values_list('id', flat=True)
        return context

def tutorial_view(request):
    return render(request, 'blog/tutorial.html')
