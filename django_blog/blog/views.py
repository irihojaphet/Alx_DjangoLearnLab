from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserProfileForm, PostForm


def home(request):
    """Home page view"""
    return render(request, 'blog/home.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'blog/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context.get('form'):
            context['form'] = AuthenticationForm()
        return context


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    template_name = 'blog/logout.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    """User profile view and edit"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})


# Blog Post CRUD Views

class PostListView(ListView):
    """Display all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    """Display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post (authenticated users only)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing blog post (author only)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post (author only)"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
