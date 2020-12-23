import cbpro
import time

cbpro_apikey = ''
cbpro_secret = ''
cbpro_passphrase = ''


initiate_deposit_when_run = True
funding_id = ''
deposit_amount = 10.00

buys = {}
buys['BTC-USD'] = {'buy': True, 'amount': 10.00}

withdraws = {}
withdraws['BTC-USD'] = {'withdraw': False,
                        'address': ''}

cbpro_api = cbpro.AuthenticatedClient(cbpro_apikey,
                                      cbpro_secret,
                                      cbpro_passphrase)

def automated_purchase(event, context):

    if initiate_deposit_when_run:
        dep_request = cbpro_api.deposit(amount=deposit_amount,
                                        currency='USD',
                                        payment_method_id=funding_id)
        print('dep_request: {}'.format(dep_request))

    for key in buys.keys():
        if buys[key]['buy'] is True:
            order = cbpro_api.place_market_order(product_id=key,
                                                 side='buy',
                                                 funds=buys[key]['amount'])
            time.sleep(2)
            qty = float(cbpro_api.get_order(order['id'])['filled_size'])
            withdraws[key]['qty'] = qty

    withdraws['BTC-USD']['base'] = 'BTC'

    for key in withdraws.keys():
        if withdraws[key]['withdraw'] is True:
            withdraw = cbpro_api.crypto_withdraw(amount=withdraws[key]['qty'],
                       currency=withdraws[key]['base'],
                       crypto_address=withdraws[key]['address'])
