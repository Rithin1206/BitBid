from django.db import models
from .models import *
from datetime import datetime,date
from django.utils import timezone
import pytz 

ACTIVE_STATUS = "Active"
CLOSED_STATUS = "Closed"
Yettoopen_STATUS = "Yet to open"

def do_settlement():
    # check for unsettled auctions
    unsettled_items = Item.objects.filter(status=ACTIVE_STATUS,
    end_date__lte=datetime.now(pytz.utc)
    # end_date__lte=timezone.now() to avoid warning
    )
    opened= Item.objects.filter(status=Yettoopen_STATUS,start_date__lte=datetime.now(pytz.utc))
    for item in opened:
        item.status=ACTIVE_STATUS
        item.save(update_fields=['status'])
    for item in unsettled_items:
        # step-1 close the auction status
        item.status=CLOSED_STATUS
        item.save(update_fields=['status'])

        # step-2 deduct balance from respective buyers
        bids = Bids.objects.filter(item=item)
        if(bids.count() > 0):
            total_deductions = Decimal(0)
            for bid in bids:
                buyer= bid.buyer
                wallet= buyer.wallet
                wallet.balance -= Decimal(bid.bid_amount)
                wallet.save()
                total_deductions += Decimal(bid.bid_amount)
            
            # step-3 add the deduction amount to the seller's wallet
            wallet = item.seller.wallet
            wallet.balance += Decimal(total_deductions)
            wallet.save()

            # step-4 tansfer item value to highest bidder
            wallet = item.highest_bidder.wallet
            wallet.balance += Decimal(item.item_value)
            wallet.save()

        # step-5 dedect items value from seller
        wallet = item.seller.wallet
        wallet.balance -= Decimal(item.item_value)
        wallet.save()

