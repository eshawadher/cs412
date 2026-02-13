from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random
# Create your views here.
class ShowAllViews(ListView):
    '''Define a view class to show all blog Article'''
    model = Article 
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'



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
