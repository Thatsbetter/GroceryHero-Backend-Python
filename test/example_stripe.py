import stripe
from backend.databasecredential  import Credential
stripe.api_key = Credential().get_stripe_secret_key_test()
stripe_publishable_key = Credential().get_stripe_publishable_key_test()
# paymentIntent = stripe.PaymentIntent.create(
#     amount=199,
#     currency='eur',
#     automatic_payment_methods={
#         'enabled': True,
#     },
# )
session_stripe = stripe.checkout.Session.create(
    payment_method_types=['card','paypal'],
    line_items=[{
        'price_data': {
            'currency': 'eur',
            'product_data': {
                'name': 'Your Product',
            },
            'unit_amount': 1000,  # Replace with the amount in cents
        },
        'quantity': 1,
    }],
    mode='payment',
    success_url='https://yourwebsite.com/success',
    cancel_url='https://yourwebsite.com/cancel',
)

payment_url = f'{session_stripe.url}'
print(f'Payment URL: {payment_url}')

inp = input()


session_details = stripe.checkout.Session.retrieve(session_stripe.id)
payment_intent_id = session_details.payment_intent
payment_intent_details = stripe.PaymentIntent.retrieve(payment_intent_id)
print("status: \n",payment_intent_details.status)

stripe.Refund.create(payment_intent=payment_intent_details.id)
