from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
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
                return Response(context)
            raise ValidationError('Error')
        else:
            raise ValidationError('Error')

class TransactionStatus(APIView):
    def post(self, request):
        response = request.data
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        try:
            status = client.utility.verify_payment_signature(params_dict)
            return Response({'status': 'Payment Successful'})
        except:
            return Response({'status': 'Payment Faliure!!!'})