from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import MeasurementModelForm, EditForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_ip_address, get_zoom
import folium
from LuxuryAuction.models import Product, Bid
from django.http import HttpResponse, Http404
from django.core import serializers
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from json import dumps
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from threading import Lock
lock = Lock()
from django.template import loader
import time, threading
import sys
from django.apps import AppConfig

if 'runserver' in sys.argv:
    def jobs():

        num=Product.objects.all().count()

        for id in range(1,num+1):
            starttime=Product.objects.get(id=id).starting_time
            endtime=Product.objects.get(id=id).ending_time
            if (timezone.now().strftime("%Y-%m-%d, %H:%M:%S")>endtime.strftime("%Y-%m-%d, %H:%M:%S")) & Bid.objects.filter(product=id).exists()== True:
                bidid=Bid.objects.filter(product=id).order_by('-price').first().id
                with lock:
                    if Bid.objects.get(id=bidid).emailsent=='N':
                        email=Bid.objects.get(id=bidid)
                        email.emailsent='Y'
                        email.save()
                        subject = 'Congratulations! You win the bidding!'
                        message = f'Hi {Bid.objects.get(id=bidid).user}, Congratulations! You win the bidding! Please click the below url to go to the payment page for this product.'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [Bid.objects.get(id=bidid).user.email, ]
                        html_message = '''
                                        <p>Hi {}, </p>
                                        <p>Congratulations! You win the bidding!</p>
                                        <p>Please click the below url to go to the payment page for this product.</p>
                                        <p><a href="http://{}/payment/{}" target=blank>Click here!</a></p>
                                        '''.format(Bid.objects.get(id=bidid).user,'52.3.245.251', id)
                        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
        # print(num)
        # print(time.ctime())
        threading.Timer(10, jobs).start()
    jobs()


def home_page_action(request):
    context = {}
    # context['product_list'] = Product.objects.order_by("starting_time")
    products = Product.objects.order_by("starting_time")
    product_list = []
    available_list = []
    for product in products:
        if product.ending_time.strftime("%Y-%m-%d, %H:%M:%S") >= timezone.now().strftime("%Y-%m-%d, %H:%M:%S"):
            #product_list.add(product)
            product_list.append(product)
        if ((product.starting_time.strftime("%Y-%m-%d, %H:%M:%S") <= timezone.now().strftime("%Y-%m-%d, %H:%M:%S")) and
            (product.ending_time.strftime("%Y-%m-%d, %H:%M:%S") >= timezone.now().strftime("%Y-%m-%d, %H:%M:%S"))):
            available_list.append(product)


    current_time = datetime.now()

    context['current_time'] = current_time
    context['product_list'] = product_list
    context['available_list'] = available_list
    return render(request, 'LuxuryAuction/index.html', context)

@login_required
def getProducts(request, filter):
    context = {}
    print("what is filter", filter)
    product_list = []
    available_list = []


    if(filter == "All"):
        products = Product.objects.order_by("starting_time")
    else:
        products = Product.objects.filter(category=filter).order_by("starting_time")


    for product in products:
        if product.ending_time.strftime("%Y-%m-%d, %H:%M:%S") >= timezone.now().strftime("%Y-%m-%d, %H:%M:%S"):
            #product_list.add(product)
            product_list.append(product)
        if ((product.starting_time.strftime("%Y-%m-%d, %H:%M:%S") <= timezone.now().strftime("%Y-%m-%d, %H:%M:%S")) and
            (product.ending_time.strftime("%Y-%m-%d, %H:%M:%S") >= timezone.now().strftime("%Y-%m-%d, %H:%M:%S"))):
            available_list.append(product)


    current_time = datetime.now()
    print(current_time)
    context['current_time'] = current_time
    context['product_list'] = product_list
    context['available_list'] = available_list
    return render(request, 'LuxuryAuction/index.html', context)

def searchProducts(request):
    context = {}
    search_error = ''
    filter = request.POST['search2']
    search_result = []
    result1 = Product.objects.filter(category__contains=filter).order_by("starting_time")
    result2 = Product.objects.filter(title__contains=filter).order_by("starting_time")
    search_result.extend(result1)
    search_result.extend(result2)
    if len(search_result) == 0:
        search_result = []
        search_error = 'No such items'

    current_time = datetime.now()
    context['product_list'] = search_result
    context['current_time'] = current_time
    context['searchError'] = search_error
    return render(request, 'LuxuryAuction/index.html', context)



"""
def getProducts(request):
    response_products = []
    for product in Product.objects.all():
        starting_time_string = (product.starting_time).isoformat()
        starting_bid_string = str(product.starting_bid)
        my_product = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'category': product.category,
        'starting_time': starting_time_string,
        'starting_bid': starting_bid_string
        }
        response_products.append(my_product)
    response_json = json.dumps(response_products)
    response = HttpResponse(response_json, content_type='application/json')
    return response


def getProductsFilter(request, filter):
    print("Printing only: ", filter)
    response_products = []
    filtered_products = Product.objects.all()
    if(filter != 'all'):
        filtered_products = Product.objects.filter(category=filter)
    for product in filtered_products:
        starting_time_string = (product.starting_time).isoformat()
        starting_bid_string = str(product.starting_bid)
        my_product = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'category': product.category,
        'starting_time': starting_time_string,
        'starting_bid': starting_bid_string
        }
        response_products.append(my_product)
    response_json = json.dumps(response_products)
    response = HttpResponse(response_json, content_type='application/json')
    return response
"""

@login_required
def profile_action(request):
    context = {}
    user = request.user
    this_user = Profile.objects.filter(user=user)
    profile = this_user[0]
    this_bid = Bid.objects.filter(user=user).order_by('-time')
    current_bid = []
    past_bid = []
    win_bid =[]
    form = EditForm(initial={'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'age': profile.age, 'address': profile.address, 'city': profile.city, 'state': profile.state, 'zip_code': profile.zip_code, 'phone_number': profile.phone_number})
    for bid_item in this_bid:
        if bid_item.product.ending_time.strftime("%Y-%m-%d, %H:%M:%S")>=timezone.now().strftime("%Y-%m-%d, %H:%M:%S"):
            current_bid.append(bid_item.product)
        else:
            past_bid.append(bid_item.product)
            bid = Bid.objects.filter(product=bid_item.product).all().order_by("-price")[0]
            if bid == bid_item:
                win_bid.append(bid_item.product)

    past_bid = list(set(past_bid))
    current_bid = list(set(current_bid))
    context['user'] = user
    context['UserProfile'] = this_user[0]
    context['allProfileFields'] = this_user[0]._meta.fields
    context['form'] = form
    context['pastBidding'] = past_bid
    context['currentBidding'] = current_bid
    context['winBid'] = win_bid
    print(win_bid)
    # print(context['form'])
    return render(request, 'LuxuryAuction/account.html', context)

@login_required
def edit_profile_action(request):
    context = {}
    user = request.user
    this_user = Profile.objects.filter(user=user)
    context['user'] = user
    context['UserProfile'] = this_user[0]
    context['allProfileFields'] = this_user[0]._meta.fields

    form = EditForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'welcome/register.html', context)

    user.first_name=form.cleaned_data['first_name']
    user.last_name=form.cleaned_data['last_name']
    user.email=form.cleaned_data['email']
    user.save()

    changed_profile = Profile.objects.filter(user=user).update(age=form.cleaned_data['age'])
    changed_profile = Profile.objects.filter(user=user).update(city = form.cleaned_data['city'])
    changed_profile = Profile.objects.filter(user=user).update(address = form.cleaned_data['address'])
    changed_profile = Profile.objects.filter(user=user).update(zip_code = form.cleaned_data['zip_code'])
    changed_profile = Profile.objects.filter(user=user).update(state = form.cleaned_data['state'])
    changed_profile = Profile.objects.filter(user=user).update(phone_number = form.cleaned_data['phone_number'])

    # return render(request, 'LuxuryAuction/account.html', context)
    return profile_action(request)


@login_required
def bidding_action(request,id):
    context = {'items': Product.objects.filter(id=id)}
    return render(request,  'LuxuryAuction/bidding.html', context)


@login_required
def getCurrentBid(request):
    response_data = []
    if request.method=='GET':
        id=request.GET.get('item_id')
    else:
        id=request.POST.get('item_id')

    if not Bid.objects.filter(product=id).exists():
        my_item = {
            'price':str(Product.objects.get(id=id).starting_bid),
            }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response

    bidid=Bid.objects.filter(product=id).order_by('-price').first().id

    for model_item in Bid.objects.filter(id=bidid):
        my_item = {
            'id':model_item.id,
            'price':str(model_item.price),
        }
        response_data.append(my_item)

    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    return response


@login_required
def biddingbutton(request):
    response_data=[]
    id=request.GET.get('item_id')
    starttime=Product.objects.get(id=id).starting_time
    endtime=Product.objects.get(id=id).ending_time
    if endtime.strftime("%Y-%m-%d, %H:%M:%S")<timezone.now().strftime("%Y-%m-%d, %H:%M:%S") :
        my_item = {
            'id':id,
            'end':'Y',
        }
        response_data.append(my_item)
        response_json = json.dumps(response_data)
        response = HttpResponse(response_json, content_type='application/json')
        return response
    else:
        my_item = {
            'id':id,
            'end':'N',

        }
        response_data.append(my_item)
        response_json = json.dumps(response_data)
        response = HttpResponse(response_json, content_type='application/json')
        return response


@login_required
def timecountdown(request):
    response_data=[]
    id=request.GET.get('item_id')
    loginuser=request.user
    starttime=Product.objects.get(id=id).starting_time
    endtime=Product.objects.get(id=id).ending_time
    if (timezone.now().strftime("%Y-%m-%d, %H:%M:%S")>endtime.strftime("%Y-%m-%d, %H:%M:%S")) & Bid.objects.filter(product=id).exists()== True:
        bidid=Bid.objects.filter(product=id).order_by('-price').first().id
        # with lock:
        #     if Bid.objects.get(id=bidid).emailsent=='N':
        #         email=Bid.objects.get(id=bidid)
        #         email.emailsent='Y'
        #         email.save()
        #         subject = 'Congratulations! You win the bidding!'
        #         message = f'Hi {Bid.objects.get(id=bidid).user}, Congratulations! You win the bidding!'
        #         email_from = settings.EMAIL_HOST_USER
        #         recipient_list = [Bid.objects.get(id=bidid).user.email, ]
        #         send_mail( subject, message, email_from, recipient_list )

        my_item = {
            'user':Bid.objects.get(id=bidid).user.username,
            'loginuser':str(loginuser),
            'id':id,
            }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response
    else:
        my_item = {
        }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response


@login_required
def addonehund(request):
    response_data = []
    id=request.GET.get('item_id')

    if not Bid.objects.filter(product=id).exists():
        my_item = {
            'price':str(Product.objects.get(id=id).starting_bid),
            }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response

    bidid=Bid.objects.filter(product=id).order_by('-price').first().id
    for model_item in Bid.objects.filter(id=bidid):
        my_item = {
            'id':model_item.id,
            'price':str(model_item.price),
        }
        response_data.append(my_item)

    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    return response


@login_required
def addtwohund(request):
    response_data = []
    id=request.GET.get('item_id')
    if not Bid.objects.filter(product=id).exists():
        my_item = {
            'price':str(Product.objects.get(id=id).starting_bid),
            }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response

    bidid=Bid.objects.filter(product=id).order_by('-price').first().id
    for model_item in Bid.objects.filter(id=bidid):
        my_item = {
            'id':model_item.id,
            'price':str(model_item.price),
        }
        response_data.append(my_item)

    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    return response


@login_required
def addthreehund(request):
    response_data = []
    id=request.GET.get('item_id')
    if not Bid.objects.filter(product=id).exists():
        my_item = {
            'price':str(Product.objects.get(id=id).starting_bid),
            }
        response_data.append(my_item)

        response_json = json.dumps(response_data)

        response = HttpResponse(response_json, content_type='application/json')
        return response

    bidid=Bid.objects.filter(product=id).order_by('-price').first().id
    for model_item in Bid.objects.filter(id=bidid):
        my_item = {
            'id':model_item.id,
            'price':str(model_item.price),
        }
        response_data.append(my_item)

    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    return response


@login_required
def placeBid(request):
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    if not 'bid_value' in request.POST or not request.POST['bid_value']:
        return _my_json_error_response("You must enter a price.")
    if not 'item_id' in request.POST or not request.POST['item_id']:
        return _my_json_error_response("You must enter an item_id to add.")
    if checkLatePay(request):
        return _my_json_error_response("You are not allowed to bid any item because you didn't pay in time")


    id=request.POST.get('item_id')
    product=Product.objects.get(id=id)
    if Bid.objects.filter(product=id).exists():
        bidid=Bid.objects.filter(product=id).order_by('-price').first().id
        value=request.POST.get('bid_value')
        if float(request.POST.get('bid_value')) <= Bid.objects.get(id=bidid).price or float(request.POST.get('bid_value')) <= Product.objects.get(id=id).starting_bid :
             return _my_json_error_response("The bid must higher than the current bid.")
        elif value[::-1].find('.')>2:
            return _my_json_error_response("Maximum number of decimal places is two. Please place the bid again.")
        else:
            new_bid = Bid(price=request.POST.get('bid_value'), user=request.user, product=product, time=str(timezone.now()), emailsent='N')
            new_bid.save()
            return getCurrentBid(request)
    else:
        value=request.POST.get('bid_value')
        if value[::-1].find('.')>2:
            return _my_json_error_response("Maximum number of decimal places is two. Please place the bid again.")
        else:
            new_bid = Bid(price=request.POST.get('bid_value'), user=request.user, product=product, time=str(timezone.now()), emailsent='N')
            new_bid.save()
            return getCurrentBid(request)



def _my_json_error_response(message, status=200):

    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


@login_required
def get_photo(request, id):
    item = get_object_or_404(Product, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.picture, type(item.picture)))

    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)


@login_required
def support_action(request):
    context = {}
    return render(request, 'LuxuryAuction/support.html', context)


@login_required
def calculate_distance_view(request, id):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='guiminr@andrew.cmu.edu')
    
    ip = '72.14.207.99'
    country, city, lat, lon = get_geo(ip)
    
    location = geolocator.geocode(city)
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
    
    m = folium.Map(width=555, height=330, location=get_center_coordinates(l_lat, l_lon))
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
    distance = 0
    day = 0
    try:
        if form.is_valid():
            instance = form.save(commit=False)
            destination_ = form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            d_lat = destination.latitude
            d_lon = destination.longitude
        
            pointB = (d_lat, d_lon)
            # print(destination)
        
            distance = round(geodesic(pointA, pointB).km, 2)
            if distance > 1000:
                day = 7
            else:
                day = 3
        
            m = folium.Map(width=555, height=330, location=get_center_coordinates(l_lat, l_lon,d_lat,d_lon), zoom_start=get_zoom(distance))
            folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination, icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        
            # draw the line between location and destination
            line = folium.PolyLine(locations=[pointA, pointB], weight=4, color='blue')
            m.add_child(line)
        
            instance.location = location
            instance.distance = distance
            instance.save()
    except AttributeError:
        print("Attribute")


    m = m._repr_html_()
    item = get_object_or_404(Product, id=id)
    if Bid.objects.filter(product=item).count() == 0:
        message = "This product has no bid"
        displayButton = 0
    else:
        bid = Bid.objects.filter(product=item).all().order_by("-price")[0]
        if bid.user != request.user:
            message = 'You are not the winner'
            displayButton = 0
        else:
            import datetime
            ending_time = item.ending_time
            now = timezone.now()
            if now < ending_time:
                message = "The bidding for this item is not over"
                displayButton = 0
            else:
                if now > (ending_time + datetime.timedelta(1)):
                    message = "It's too late to pay(You only have 24 hours to pay)"
                    displayButton = 0
                else:
                    message = "Congratulation!"
                    displayButton = 1
    context = {
        'distance' : distance,
        'days' : day,
        'form' : form,
        'map' : m,
        'price': bid.price,
        'product_id': id,
        'message': message,
        'displayButton': displayButton,
    }
    return render(request, 'LuxuryAuction/payment.html', context)


@login_required
def paid(request, id):
    if request.method == 'POST':
        item = get_object_or_404(Product, id=id)
        bid = Bid.objects.filter(product=item).all().order_by("-price")[0]
        if float(request.POST['price']) == float(bid.price):
            message = 'Payment Successful'
            item.isPaid = True
            item.save()
        else:
            message = 'Wrong Price'
    else:
        message = 'Method cant be GET'
    context = {
        'message': message,
    }
    response_json = json.dumps(context)
    response = HttpResponse(response_json, content_type='application/json')
    return response


@login_required
def checkLatePay(request):
    bids = Bid.objects.filter(user=request.user)
    if bids.count() > 0:
        import datetime
        for bid in bids:
            if bid == Bid.objects.filter(product=bid.product).all().order_by("-price")[0] and \
                    timezone.now() > (bid.product.ending_time + datetime.timedelta(1)) and bid.product.isPaid is False:
                return True
    return False
