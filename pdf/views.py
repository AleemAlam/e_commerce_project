from rest_framework.views import APIView
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.doctemplate import Indenter

class CreateInvoiceToPDF(APIView):

    def post(self, request):
        filename = 'invoice.pdf'
        PDF_title = request.data.get('company_name')
        document_title = request.data.get('company_name')
        document_sub_title = request.data.get('sub_title')
        company_address = request.data.get('address')
        company_email = request.data.get('email')
        company_number = request.data.get('number')
        company_website = request.data.get('website')
        product_name = request.data.get('product')
        price = request.data.get('price')
        quantity = request.data.get('quantity')
        total = request.data.get('total')

        company_data = [[company_address, company_number],
                ['', company_email],
                ['', company_website]]
        pdf = SimpleDocTemplate(
            filename,
            pagesize=letter
        )

        title_style = TableStyle([
            ('FONTSIZE', (0, 0), (0, -1), 20),
        ])
        company_name = Table([[document_title]], style=title_style, hAlign='LEFT')
        table = Table(company_data, hAlign='LEFT')
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])
        table.setStyle(style)
        elements = []
        elements.append(company_name)
        elements.append(table)
        pdf.build(elements)
        return Response({'message': 'Pdf Created'})




