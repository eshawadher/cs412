from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

quotes = [
     "I hate to hear you talk about all women as if they were fine ladies instead of rational creatures. None of us want to be in calm waters all our lives.",
     " It isn’t what we say or think that defines us, but what we do.",
     "Indulge your imagination in every possible flight.",
     "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.",
     " To be fond of dancing was a certain step towards falling in love.",
]

images = [
    "janeausten2.jpeg",
    "janeausten3.jpeg",
    "janeausten4.jpeg",
    "janeausten5.jpeg"
]

def home(request):

    response_text = '''
    <html>
        <h1>Quotes of the Day</h1>

        The current time is {time.ctime()}.
    </html>
'''
    return HttpResponse(response_text)



def quote_page(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)

    context = {
        'current_time': time.ctime(),
        'quote': selected_quote,
        'image': selected_image
    }

    template = 'quotes/quote.html'
    return render (request, template, context)

def about(request):
    selected_image = random.choice(images)
    context = {
        'current_time': time.ctime(),
        'image': selected_image,
    }
    template = 'quotes/about.html'
    return render (request, template, context)

def all(request):
    context = {
        'current_time': time.ctime(),
        'quotes': quotes,
        'images': images,
    }
    template = 'quotes/show_all.html'
    return render(request, template, context)