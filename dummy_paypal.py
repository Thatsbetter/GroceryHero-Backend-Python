import paypalrestsdk

from databasecredential import Credential

client_id = Credential().get_paypal_client_id()
secret = Credential().get_paypal_secret()
paypalrestsdk.configure(
    {
        "mode": "sandbox",  # sandbox or live
        "client_id": client_id,
        "client_secret": secret
    }
)

payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"},
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "item",
                "sku": "item",
                "price": "5.00",
                "currency": "EUR",
                "quantity": 1}]},
        "amount": {
            "total": "5.00",
            "currency": "EUR"},
        "description": "This is the payment transaction description."}]})

if payment.create():
    print("Payment created successfully")
else:
    print(payment.error)

for link in payment.links:
    if link.rel == "approval_url":
        # Convert to str to avoid Google App Engine Unicode issue
        # https://github.com/paypal/rest-api-sdk-python/pull/58
        approval_url = str(link.href)
        print("Redirect for approval: %s" % (approval_url))
        print(payment)
