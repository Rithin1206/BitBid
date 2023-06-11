from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal
import copy
import base64

USER_TYPES = [
    ("Buyer", "Buyer"),
    ("Seller", "Seller"),
]

ITEM_STATUS = [
    ("Active", "Active"),
    ("Closed", "Closed"),
]



class Wallet(models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    profile_picture = models.BinaryField(blank = True, null = True, editable = True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)

class Item(models.Model):
    # By default django already creates "id = models.BigAutoField(primary_key=True)". Use that(id or item_id?) as auction_number
    name=models.CharField(max_length=25)
    description = models.CharField(max_length=140)
    item_image=models.BinaryField(blank = True, null = True, editable = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    item_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    base_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))]) # Set min_value=0.01 or 0 in forms
    increment_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))]) # Set min_value=0.01 or 0 in forms
    seller = models.ForeignKey(Profile, related_name="sold_items", on_delete=models.CASCADE) # prof.sold_items.all() would give items sold by a particular seller
    highest_bidder = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=0)
    status = models.CharField(max_length=50, choices=ITEM_STATUS)

class Bids(models.Model):
    buyer = models.ForeignKey(Profile, related_name="bids", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="bids", on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=12,decimal_places=2)

###### Helper Functions #####
def create_user_profile(user, username, register_as, profile_picture):
    if(User.objects.filter(username=username).exists()):
        return False
    user.username = username
    user.save()
    if not profile_exists(username):
        Profile.objects.create(user=user, wallet=Wallet.objects.create(balance=0), user_type=register_as, profile_picture=encode_image(profile_picture))
        return True
    else:
        print("Profile already exists!!!")
        return False

def profile_exists(username):
    if User.objects.filter(username=username).exists() and Profile.objects.filter(user__username = username).exists():
        return True

    return False

def create_item(user, name, item_image, description, start_date, end_date, item_value, base_amount, increment_amount):
    # Ex Usage: create_item(request.user, "desc", datetime.datetime(2022, 10, 14, 21, 0, tzinfo=tz.gettz('US/Central')), datetime.datetime(2022, 10, 14, 21, 0, tzinfo=tz.gettz('US/Central')), 100, 10)
    # Add any extra validations
    update_wallet(user.profile, item_value)
    return Item.objects.create(name=name, seller=user.profile, description=description, item_image=encode_image(item_image), start_date=start_date, end_date=end_date, item_value=item_value, base_amount=base_amount, increment_amount=increment_amount, status='Yet to open')

def register_bid(buyer,item,amount):
    Bids.objects.update_or_create(buyer=buyer,item=item,defaults={'bid_amount':amount})


def update_item(profile, id, new_bid):
    item= Item.objects.get(id=id)
    if(item.highest_bid<float(new_bid)):
        item.highest_bid= new_bid
        item.highest_bidder= profile
        item.save()
        register_bid(buyer=profile,item=item,amount=float(new_bid))

def update_wallet(profile, added_money):
    profile= Profile.objects.get(id=profile.id)
    wallet= profile.wallet
    prev_balance = copy.deepcopy(profile.wallet.balance)
    added_money= Decimal(added_money.replace(',','.'))
    wallet.balance= prev_balance+added_money
    wallet.save()

def encode_image(image):
    if image and image != '':
        return base64.b64encode(image.read())
    return None
