from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'category', 'content', 'thumbnail', 'tags', 'is_published']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'category', 'content', 'thumbnail', 'tags', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class PostDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
