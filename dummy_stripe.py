from databasecredential import Credential
import stripe

stripe.api_key = Credential().get_stripe_secret_key_test()
stripe_publishable_key = Credential().get_stripe_publishable_key_test()
paymentIntent = stripe.PaymentIntent.create(
    amount=199,
    currency='eur',
    automatic_payment_methods={
        'enabled': True,
    },
)
res = paymentIntent=paymentIntent.client_secret

print(res)
