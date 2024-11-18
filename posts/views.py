from django.views.generic import (
    ListView,  
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import Post, Status 
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)

class PostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["post_list"] = (
            Post.objects
            .filter(status=Status.objects.get(name="published"))
            .order_by("created_on" ).reverse()
        )
        return context
    
class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["post_list"] = (
            Post.objects
            .filter(status=Status.objects.get (name="draft"))
            .filter (author=self.request.user)
            .order_by ("created_on").reverse()
        )
        return context
    
class ArchivedPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = (
        Post.objects
        .filter(status=Status.objects.get (name="archived"))
        .order_by ("created_on").reverse()
        )
        return context
    
class DetailPostView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "posts/detail.html"
    model = Post

    def test_func(self):
        post = self.get_object()
        if post.status.name == "published" or post.status.name == "archived":
            return True
        elif post.status.name == "draft" and post.author == self.request.user:
            return True
        else:
            return False

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "status", "body"]

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostCreateView(LoginRequiredMixin,CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "status", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)