from django.test import TestCase
from unittest.mock import MagicMock
from unittest import skip
from datetime import timedelta
from .settlement import *
from django.utils import timezone

from .views import *

class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        item1 = {'name':'item_1','description': 'desc 1','item_value':100.00,'base_amount':10.00,'increment_amount':1.00}
        item2 = {'name':'item_2','description': 'desc 2','item_value':200.00,'base_amount':20.00,'increment_amount':2.00}
        items = [item1,item2]

        # Seller
        self.seller_user = User.objects.create_user('john')
        wallet = Wallet.objects.create(balance=0.00)
        seller_profile = Profile.objects.create(user=self.seller_user,wallet=wallet,profile_picture=None,user_type='Seller')
        for item in items:
            start_date =  timezone.now()
            end_date = start_date+ timedelta(days=2)
            Item.objects.create(name=item['name'],seller=seller_profile, description=item['description'],
                                item_image=None, start_date=start_date, end_date=end_date,
                                item_value=item['item_value'],
                                base_amount=item['base_amount'],
                                increment_amount=item['increment_amount'],
                                status='Active')
        # Buyer
        self.buyer_user = User.objects.create_user('Aaron')
        wallet = Wallet.objects.create(balance=0.00)
        self.buyer_profile = Profile.objects.create(user=self.buyer_user,wallet=wallet,profile_picture=None,user_type='Buyer')

    def test_home_view(self):
        respone = self.client.get('/')
        self.assertEquals(respone.status_code,200)
        self.assertTemplateUsed(response=respone,template_name='Home.html')
    
    def test_seller_view(self):
        respone = self.client.get('/Seller')
        self.assertEquals(respone.status_code,200)
        self.assertTemplateUsed(response=respone,template_name='Seller.html')
    
    def test_seller_view_exception(self):
        do_settlement = MagicMock(side_effect=Exception('some exception'))
        respone = self.client.get('/Seller')
        self.assertEquals(respone.status_code,200)
        self.assertTemplateUsed(response=respone,template_name='Seller.html')

    def test_buyer_view(self):
        respone = self.client.get('/Buyer')
        self.assertEquals(respone.status_code,200)
        self.assertTemplateUsed(response=respone,template_name='Buyer.html')

    def test_signup_view_profile_already_exists(self):
        self.client.force_login(self.seller_user)
        response = self.client.post('/User',data={'username': 'john', 'register_as':'Seller', 'profile_picture':''})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Seller')

    def test_signup_view_new_profile(self):
        new_usr = User.objects.create(username='hannah')
        self.client.force_login(new_usr)
        User.objects.get(username='hannah').delete()
        response = self.client.post('/User',data={'username': 'hannah', 'register_as':'Seller', 'profile_picture':''})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/')

    def test_login_view_without_authentication(self):
        response = self.client.get('/User')
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/')

    def test_login_view_seller(self):
        self.client.force_login(self.seller_user)
        response = self.client.get('/User')
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Seller')

    def test_login_view_buyer(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/User')
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Buyer')

    def test_login_view_unknown_user_type(self):
        ukwn_user = User.objects.create_user('brian')
        wallet = Wallet.objects.create(balance=0.00)
        Profile.objects.create(user=ukwn_user,wallet=wallet,profile_picture=None,user_type='Unkown')
        self.client.force_login(ukwn_user)
        response = self.client.get('/User')
        self.assertEquals(response.status_code,404)
    
    def test_profile_view(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/profile')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response=response,template_name='profile.html')

    def test_buyer_new_item_should_error(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/newItem')
        self.assertEquals(response.status_code,403)

    def test_seller_new_item_post(self):
        self.client.force_login(self.seller_user)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=2)
        response = self.client.post('/newItem',
            data={
                'name':'new_item',
                'description':'desc',
                'start_date':start_date,
                'end_date':end_date,
                'item_value':100.00,
                'base_amount':50.00,
                'increment_amount':1.00})
        self.assertEquals(response.status_code,302)
        assert Item.objects.filter(name='new_item').exists()
        new_item = Item.objects.get(name='new_item')
        # assert new balance should be increased
        new_balance = new_item.seller.wallet.balance
        assert new_balance == 100.00
        self.assertRedirects(response=response,expected_url='/Seller')
    
    def test_seller_new_item_get(self):
        self.client.force_login(self.seller_user)
        response = self.client.get('/newItem')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response=response,template_name='newItem.html')

    def test_buyer_view_item(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/item/1/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response=response,template_name='buyer_item_popup.html')

    def test_seller_new_bid_should_throw_error(self):
        self.client.force_login(self.seller_user)
        response = self.client.get('/newBid/1/')
        self.assertEquals(response.status_code,403)

    def test_seller_new_bid_get_should_redirect(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/newBid/1/')
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Buyer')

    def test_buyer_new_bid_should_update_bids(self):
        self.client.force_login(self.buyer_user)
        response = self.client.post('/newBid/1/',data={'newBid':110.00})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Buyer')
        item = Item.objects.get(id=1)
        self.assertEquals(item.highest_bidder,self.buyer_profile)
        bid = Bids.objects.get(buyer=self.buyer_profile,item=item)
        self.assertEquals(bid.bid_amount,110.00)
    
    def test_buyer_new_bid_with_low_bid_amount_should_not_update_bids(self):
        self.client.force_login(self.buyer_user)
        # initial bid high
        self.client.post('/newBid/1/',data={'newBid':110.00})
        # subsequent bid low
        response = self.client.post('/newBid/1/',data={'newBid':90.00})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response=response,expected_url='/Buyer')
        item = Item.objects.get(id=1)
        bid = Bids.objects.get(buyer=self.buyer_profile,item=item)
        self.assertEquals(bid.bid_amount,110.00)

    def test_add_money_get_should_render_template(self):
        self.client.force_login(self.seller_user)
        response = self.client.get('/addMoney')
        self.assertTemplateUsed(response=response,template_name='addMoney.html')

    def test_add_money_post_should_update_wallet_balance(self):
        self.client.force_login(self.buyer_user)
        resposne = self.client.post('/addMoney',data={'added_money':10.00})
        buyer_profile  = Profile.objects.get(user=self.buyer_user)
        self.assertEquals(buyer_profile.wallet.balance,10.00)
        self.assertTemplateUsed(response=resposne,template_name='profile.html')

    def test_add_real_money_should_render_template(self):
        self.client.force_login(self.buyer_user)
        response = self.client.get('/addRealMoney')
        self.assertTemplateUsed(response=response,template_name='addMoney.html')
    
    def test_add_real_money(self):
        self.client.force_login(self.buyer_user)
        resposne = self.client.post('/addRealMoney',data={'added_money':10.00})
        self.assertEquals(resposne.status_code,302)

    def test_coinbase_webhook(self):
        response = self.client.post('/webhook')
        self.assertEquals(response.status_code,301)
