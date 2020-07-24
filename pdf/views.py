from rest_framework.views import APIView
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

class CreateInvoiceToPDF(APIView):

    def post(self, request):
        order_items = [
            {
                "id": 2,
                "item": "Jeans",
                "item_obj": {
                    "id": 1,
                    "title": "Jeans",
                    "category": 1,
                    "description": "skdjksdj",
                    "image": "/media/Shirt_vIrl9Vl.jpg",
                    "discount_price": 0.0,
                    "avg_rating": 0,
                    "no_of_ratings": 0,
                    "price": 1989.0
                },
                "final_price": 7956.0,
                "quantity": 4
            },
            {
                "id": 3,
                "item": "Shirt",
                "item_obj": {
                    "id": 2,
                    "title": "Shirt",
                    "category": 1,
                    "description": "KSDJSJDK",
                    "image": "/media/Shirt_GZ2pzoa.jpg",
                    "discount_price": 0.0,
                    "avg_rating": 0,
                    "no_of_ratings": 0,
                    "price": 1000.0
                },
                "final_price": 2000.0,
                "quantity": 2
            }
        ]
        filename = 'invoice.pdf'
        PDF_title = 'My Company Name'
        document_title = request.user.username + ' Invoice'
        company_address = request.data.get('address')
        company_email = request.data.get('email')
        company_number = request.data.get('number')
        company_website = request.data.get('website')
        total = request.data.get('total')
        elements = []
        product_table = []

        company_data = [[company_address, company_number],
                ['', company_email],
                ['', company_website]]
        pdf = SimpleDocTemplate(
            filename,
            pagesize=letter
        )

        title_style = TableStyle([
            ('FONTSIZE', (0, 0), (0, -1), 20),
            ('BOTTOMPADDING', (0,0),(0,-1), 30),
        ])
        company_name = Table([[document_title]], style=title_style, hAlign='LEFT')
        table = Table(company_data, hAlign='LEFT')
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (1, 0), (-1, -1), 100),
            ('BOTTOMPADDING', (0, 2), (-1, 2), 20),
        ])
        product_table.append(['Product', 'Price', 'Quantity', 'Total'])
        final_price = 0

        for i in range(len(order_items)):
            product_table.append(
                [order_items[i]['item_obj']['title'], order_items[i]['item_obj']['price'], order_items[i]['quantity'], order_items[i]['final_price']]
            )
            final_price += order_items[i]['final_price']

        product_table.append(['Total: ',final_price])

        product_table_style = TableStyle([
            ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (3, 0), 16),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTSIZE', (0,0), (-1,0), 15),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 70),
            ('FONTNAME', (0,3), (1,3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (1, 3), 15),
            ('TOPPADDING', (0, 3), (1, 3), 12),
            ('LINEBELOW', (0, 2), (-1, 2), 0.25, colors.black),
            ('LINEBELOW', (0, 0), (3, 0), 2, colors.black)
        ])
        product_table = Table(product_table, style=product_table_style, hAlign='LEFT')

        table.setStyle(style)
        elements.append(company_name)
        elements.append(table)
        elements.append(product_table)
        pdf.build(elements)
        return Response({'message': 'Pdf Created'})




