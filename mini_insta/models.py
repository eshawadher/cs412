from django.db import models

# # Create your models here.
class Profile(models.Model):
    '''encap the data of a users profile'''
    #define data attributes of teh Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.display_name} by {self.username}'


