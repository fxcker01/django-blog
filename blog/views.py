from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import News
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm, CommentForm, NewsForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Comment


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Main page'
        ctx['top_articles'] = News.objects.order_by('-views')[:3]
        return ctx


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(avtor=user).order_by('-date')

    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)

        ctx['title'] = f"Articles by {self.kwargs.get('username')}"
        return ctx

class NewsDetailView(DetailView):
    model = News

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        session_key = f'viewed_post_{obj.pk}'

        if not self.request.session.get(session_key, False):
            obj.views += 1
            obj.save()
            self.request.session[session_key] = True

        return obj

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        post = self.object

        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        ctx['comments'] = post.comments.filter(parent__isnull=True).order_by('-created')
        ctx['form'] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.name = request.user
            comment.save()
            return redirect('news-detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.name or self.request.user.is_superuser or self.request.user.is_staff



def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if user.is_authenticated:
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))



def reply_comment(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    post = parent_comment.post
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.parent = parent_comment
            reply.name = request.user
            reply.save()
    return redirect('news-detail', pk=post.pk)

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.name or self.request.user.is_superuser or self.request.user.is_staff

class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'blog/create_news.html'


    def get_context_data(self, **kwards):
        ctx = super(UpdateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Update article'
        ctx['btn_text'] = 'Update'
        return ctx
    

    def test_func(self):
        news = self.get_object()
        return (
            self.request.user == news.avtor or
            self.request.user.is_superuser or
            self.request.user.is_staff
        )


    def form_valid(self, form):
        # form.instance.avtor = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'
    template_name = 'blog/delete-news.html'

    def test_func(self):
        news = self.get_object()
        return (
            self.request.user == news.avtor or
            self.request.user.is_superuser or
            self.request.user.is_staff
        )



class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'blog/create_news.html'


    def get_context_data(self, **kwards):
        ctx = super(CreateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Add article'
        ctx['btn_text'] = 'Add'
        return ctx

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)

def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Contacts'})

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Відправка повідомлення на пошту
            subject = f"Message from {name}"
            plain_message = f"From: {name}\nEmail: {email}\n\nnMessage:\n{message}"
            from_email = settings.EMAIL_HOST_USER  # пошта відправника (встановлено в settings.py)
            to_email = settings.DEFAULT_CONTACT_EMAIL  # пошта отримувача

            email = EmailMessage(
                subject,
                plain_message,
                from_email,
                [to_email],
                headers={'Reply-To': email}
            )
            email.send()


            # Повідомлення про успішну відправку
            messages.success(request, 'Your message has been sent! We will contact you soon.')
            return render(request, 'blog/contacts.html', {'form': form})

    else:
        form = ContactForm()

    return render(request, 'blog/contacts.html', {'form': form})

def like_news(request, pk):
    post = get_object_or_404(News, pk=pk)
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

    return redirect('news-detail', pk=pk)


def custom_403_view(request, exception=None):
    return render(request, "errors/403.html", status=403)