from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of a blog article by an author.'''

    #define data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    #image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''return a string represention of thsi mofel instance.'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''return url to dispaly an instance of this object'''
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        '''return a querset of comments about article'''
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'
    
    