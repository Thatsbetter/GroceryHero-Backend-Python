
import logging

from flask import jsonify, request
from flask_restful import Resource
import stripe


stripe.api_key = Credential().get_stripe_secret_key_test()
stripe_publishable_key = Credential().get_stripe_publishable_key_test()

class CreateStripePayment(Resource):
    def post(self):

        # Validate Parameters
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=str, required=True, help='amount cannot be blank')

        args = parser.parse_args()

        amount = args['amount']

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        response = jsonify(paymentIntent=payment_intent.client_secret,
                           publishableKey=stripe_publishable_key
                           )
        return response


class LogStripePaymentError(Resource):
    def post(self):
        request_data = request.get_json()
        logging.error(request_data)


class RefundStripePayment(Resource):
    def post(self):
        pass
