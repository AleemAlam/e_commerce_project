from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from product.models import Payments
from django.core.mail import EmailMessage
from django.conf import settings
import razorpay


client = razorpay.Client(auth=("rzp_test_9edOOxXrp0K6He", "NXf4xapbnGmzsaiW3XeF8mQM"))

class Transaction(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        item = request.data.get('item')
        name = request.data.get('name')
        email = request.data.get('email')
        order_receipt = 'order_receipt'

        if amount:
            context = {}
            data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': order_receipt,
                'payment_capture': '0'
            }
            response = client.order.create(data=data)
            order_id = response['id']
            order_status = response['status']
            if order_status == 'created':
                context['product'] = item
                context['price'] = amount
                context['name'] = name
                context['email'] = email
                context['order_id'] = order_id

                email_subject = "New Order Placed"
                admin_mail = 'admin@gmail.com'
                message = f'New Order Place With order Id: {order_receipt} \n customer name: {request.user}\n Amount: {amount}'
                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [admin_mail]
                )
                email_message.send()

                return Response(context)
            raise ValidationError('Error')
        else:
            raise ValidationError('Error')

class TransactionStatus(APIView):
    def post(self, request):
        response = request.data
        payment = Payments.object.create(user = request.user,
                                         razorpay_payment_id = response['razorpay_payment_id'],
                                         status = 'APPROVED',
                                         amount = response['amount'],
                                         )
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        try:
            status = client.utility.verify_payment_signature(params_dict)
            payment = Payments.object.create(user=request.user,
                                             razorpay_payment_id=response['razorpay_payment_id'],
                                             status='APPROVED',
                                             amount=response['amount'],
                                             )
            return Response({'status': 'Payment Successful'})
        except:
            payment = Payments.object.create(user=request.user,
                                             razorpay_payment_id=response['razorpay_payment_id'],
                                             status='FALIURE',
                                             amount=response['amount'],
                                             )
            return Response({'status': 'Payment Faliure!!!'})