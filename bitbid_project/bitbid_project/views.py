from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .settlement import *
from coinbase_commerce.client import Client
from coinbase_commerce.webhook import Webhook
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
import logging
from django.views.decorators.csrf import csrf_exempt

ACTIVE_STATUS = "Active"
CLOSED_STATUS = "Closed"
Yettoopen_STATUS = "Yet to open"

def home(request):
    return render(request,'Home.html')

def seller(request):
    try:
        # do settle right on landing of seller page
        do_settlement()
    except Exception as e:
        print('Something went wrong', e)

    context={}
    context['Items']=Item.objects.all()
    return render(request,'Seller.html',context)

def buyer(request):
    try:
        # do settle right on landing of buyer page
        do_settlement()
    except Exception as e:
        print('Something went wrong', e)
    
    context={}
    # context['Items']=Item.objects.all()
    context['Items']=Item.objects.filter(status = ACTIVE_STATUS) | Item.objects.filter(status =Yettoopen_STATUS )
    return render(request,'Buyer.html',context)

# @require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        profile_created = None
        if request.POST:
            username=request.POST.get('username')
            register_as=request.POST.get('register_as')
            if(register_as!= 'Buyer' and register_as!= 'Seller'):
                return HttpResponseNotFound("Oops! You are trying to register as not Buyer or Seller")
            profile_picture=request.FILES.get('profile_picture')
            profile_created = create_user_profile(request.user, username, register_as, profile_picture)

        un = request.user.username
        if profile_exists(un):
            user_type = Profile.objects.get(user__username=un).user_type
            if(user_type == "Buyer"):
                return redirect(buyer)
            elif(user_type == "Seller"):
                return redirect(seller)
            else:
                return HttpResponseNotFound("Oops! Something happened")
        else:
            context = {}
            context['form']= ProfileForm()

            if profile_created == False:
                context['message'] = "Username or profile already exists. Please try a different username"
            return render(request, "Signup.html", context)

    else:
        return redirect(home)

@login_required
def profile(request):
    context={}
    context['pro'] = request.user.profile
    context['bids'] = Bids.objects.filter(buyer=request.user.profile)
    return render(request,"profile.html", context)

@login_required
def newItem(request):
    if request.user.profile.user_type != "Seller":
        return HttpResponseForbidden()
    if request.method=='POST':
        create_item(request.user, request.POST['name'], request.FILES['item_image'] if 'item_image' in request.FILES else None, request.POST['description'], request.POST['start_date'],request.POST['end_date'], request.POST['item_value'], request.POST['base_amount'],request.POST['increment_amount'] )

        return redirect(seller)
    else:
       return render(request,'newItem.html')

@login_required
def bidView(request,id):
    item =Item.objects.filter(id=id).first()
    context={}
    context['item']= item
    return render(request, 'buyer_item_popup.html',context)

@login_required
def newBid(request,id):
    if request.user.profile.user_type != "Buyer":
        return HttpResponseForbidden()
    if request.method=='POST':
        update_item(request.user.profile,id, request.POST['newBid'])
        return redirect(buyer)
    else:
        return redirect(buyer)

@login_required
def addMoney(request):
    if request.method=='POST':
        update_wallet(request.user.profile, request.POST['added_money'])
        context={}
        context['pro']= request.user.profile
        return render(request,"profile.html", context)
    else:
       return render(request,'addMoney.html')

@login_required
def addRealMoney(request):
    if request.method=='POST':
        amount = request.POST["added_money"]
        #TODO put the api value in settings and retrieve it from there
        client = Client(api_key='b2461b61-22af-41fe-984d-e1302a45372c')
        #TODO put heroku hosted website url
        domain_url = 'https://bit-bid.herokuapp.com/'
        product = {
            'metadata': {
            'customer_username': request.user.username if request.user.is_authenticated else None,
            },
            'name': 'Add BTC to BitBid wallet',
            'description': 'Add now to sell/buy items on BitBid!',
            'pricing_type': 'fixed_price',
            'redirect_url': domain_url + 'profile',
            'cancel_url': domain_url + 'profile',
        }
        product['local_price'] = dict()
        product['local_price']['amount'] = amount
        product['local_price']['currency'] = 'BTC'
        charge = client.charge.create(**product)
        response = redirect(charge.hosted_url)
        return response
    else:
       return render(request,'addMoney.html')

@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    '''A view called by coinbase on receiving a payment 
    from any of the users'''
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = "4256d3df-57f2-4519-93d3-eab71843b8fb"

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:confirmed':
            ## logic to update the wallet balance of the correct user
            logger.info('Payment confirmed.')
            username = event['data']['metadata']['customer_username']
            profile = Profile.objects.get(user__username=username)
            amount_added =  event['data']['local_price']['amount']
            update_wallet(profile, amount_added)
    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)

    



        