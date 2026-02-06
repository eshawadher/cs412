from django.shortcuts import render # pyright: ignore[reportMissingModuleSource]
from django.http import HttpResponse
# Create your views here.
import random
import datetime
from django.shortcuts import redirect

def main(request):
    template_name = "restaurant/main.html"
    context = {
        'current_time': datetime.datetime.now()
    }
    return render(request, template_name, context)

def order(request):
    template_name = "restaurant/order.html"
    daily_specials = [
        {'name' : "Paella Valenciana", 'price': 24.99, 'description': 'Traditional Spanish rice dish with seafood'},
        {'name': 'Grilled Octopus', 'price': 19.99, 'description': 'Tender octopus with paprika and olive oil'},
        {'name': 'Jamón Ibérico Plate', 'price': 22.99, 'description': 'Premium cured ham with manchego cheese'},
        {'name': 'Seafood Fideuà', 'price': 21.99, 'description': 'Catalan noodle paella with fresh seafood'},
    ]

    daily_special = random.choice(daily_specials)
    context = {
        'daily_special': daily_special,
        'current_time': datetime.datetime.now()
    }

    return render(request, template_name, context)

def confirmation(request):
    template_name = "restaurant/confirmation.html"

    if request.POST:
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        ordered_items = []
        total_price = 0.0

        menu_items = {
            'tapas': {'name': 'Tapas Platter', 'price': 16.99},
            'paella': {'name': 'Paella', 'price': 24.99},
            'sangria': {'name': 'Sangria Pitcher', 'price': 18.99},
            'churros': {'name': 'Churros with Chocolate', 'price': 8.99},
            'daily_special': {'name': request.POST.get('daily_special_name', 'Daily Special'), 
                            'price': float(request.POST.get('daily_special_price', 0))}
        }

        for item_key, item_info in menu_items.items():
            if request.POST.get(item_key):
                ordered_items.append(item_info['name'])
                total_price += item_info['price']

                extras_key = f'{item_key}_extras'
                if extras_key in request.POST:
                    extras = request.POST.get(extras_key)
                    ordered_items[-1] += f'(with{extras})'
        current_time = datetime.datetime.now()
        minutes_to_add  = random.randint(30,60)
        ready_time = current_time + datetime.timedelta(minutes=minutes_to_add)

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time,
            'current_time': current_time
        }
    
        return render(request, template_name, context)
    

    return redirect('order')


