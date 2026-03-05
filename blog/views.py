from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm,CreateCommentForm, UpdateArticleForm
import random
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.
class ShowAllViews(ListView):
    '''Define a view class to show all blog Article'''
    model = Article 
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
        return super().dispatch(request, *args, **kwargs)



class ArticleView(DetailView):
    '''Display a single article'''
    model = Article
    template_name = "blog/article.html"
    contect_object_name = "article"

class RandomArticleView(DetailView):
    '''Dispaly a single article selected at random'''
    model = Article 
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        '''return one instrance of the Article objected seelcted at random'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''
 
 
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        return reverse('login')
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
        return super().form_valid(form)
class CreateCommentView(CreateView):
    '''created new comment on new article'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''c'''
        #return reverse('show_all')
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})
    def get_context_data(self):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context
    def form_valid(self):
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        return super().form_valid(form)
    


    def form_valid(self,form):
        print(form.cleaned_data)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        form.instance.article = article

        return super().form_valid(form)
class UpdateArticleView (UpdateView):
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        article = comment.article
        return reverse('article', kwargs={'pk': article.pk})
class UserRegistrationView(CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')
