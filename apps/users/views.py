from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.bursary.models import Bursary
from apps.courses.models import Course, CoursesPay
from apps.invoices.models import Invoice
from apps.invoices.serializers import InvoiceSerializer

from apps.users.models import Users
from apps.users.serializers import UserExportSerializer, UserSerializer
from datetime import datetime
from apps.courses.utils import courses_pre, courses_trans, prices

import qrcode
import os
from django.http import HttpResponse
from django.conf import settings

import xlsxwriter

def create_qr(text, name):
    img = qrcode.make(text)
    file = open(os.path.join(settings.BASE_DIR, 'media', name), "wb")
    img.save(file)
    file.close()
    
def get_current_price(item_price):
    data_valid = datetime.fromisoformat(item_price['valid'])
    date_now = datetime.now()
    return item_price['price'] if data_valid > date_now else item_price['future_price']    

def calc_price(data):
    course_pre = data['id_course_pre']
    course_transco = data['id_course_transco']
    inscription = data['id_inscription']
    id_user = data['id']
    code = data.get('code')
    invited_by = data.get('invited_by')
    
    if course_pre == 4:
        four_persons = CoursesPay.objects.filter(id=4).first()
        if four_persons.persons >= 16:
            raise Response({'detail': 'Error'})
    
    course_pre_select = None
    course_transco_select = None
    inscription_select = None
    
    for i in courses_pre:
        if i['id'] == course_pre:
            course_pre_select = i
            break
    
    for i in courses_trans:
        if i['id'] == course_transco:
            course_transco_select = i
            break
        
    for i in prices:
        if i['id'] == inscription:
            inscription_select = i
            break
   
    total_pay = (
        course_pre_select['extra_cost'] 
        + 
        course_transco_select['extra_cost']
        + 
        get_current_price(inscription_select)
    )
   
    course_pre_ob = Course.objects.filter(id=course_pre).first()
    course_trans_ob = Course.objects.filter(id=course_transco).first()
   
    if code:
        bursary_code = Bursary.objects.filter(code=code, isActive=True)
        if bursary_code.exists():
            # bursary_code.update(isActive=False, invited_by=invited_by)
            total_pay = 0
   
    user = Users.objects.filter(pk=id_user)
    user.update(
        price_pay=total_pay,
        course_pre=course_pre_ob,
        course_trans=course_trans_ob
    )
    
    return total_pay

def create_invoice(data, id_user): 
    new_invoice = Invoice.objects.create(**data)
    user = Users.objects.filter(pk=id_user)
    user.update(invoice=new_invoice)
    return

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        code_invited = request.data['code']
        
        if code_invited:
            code = Bursary.objects.filter(code=code_invited, isActive=True).exists()
            if not code:
                return Response(
                    {'ok': False}, 
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
        
        data = super().create(request, args, kwargs)
        
        id = data.data['id']
        name = '{}.jpg'.format(id)
        
        create_qr(str(id), name)
        
        request.data['id'] = id
        calc_price(request.data)
        
        data_invoice = request.data['invoice_data']
        
        if data_invoice:
            create_invoice(request.data['invoice_data'], id)
        
        user = Users.objects.filter(pk=id).first()
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
class ExcelViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserExportSerializer
    
    def list(self, request):
        libro = xlsxwriter.Workbook('users.xls')
        hoja = libro.add_worksheet()
        
        header = [
            'id', 
            'nombre', 
            'apellidos', 
            'correo electronico',
            'dirección',
            'cp',
            'estado',
            'municipio o alcaldía',
            'telefono',
            'celular',
            'empresa o institución',
            'especialidad',
            'cédula profesional',
            'cédula de especialidad',
            'costo de inscripcción',
            'pago validado',
            'curso de precongreso',
            'curso de transcongreso',
            'nombre o razon social',
            'rfc',
            'calle',
            'numero exterior',
            'numero interior',
            'colonia',
            'cp',
            'municipio o alcaldia',
            'estado',
            'correo de facturacion',
            'telefono de facturación',
            'forma de pago',
            'uso de la factura',
        ]
        
        row = 0
        col = 0
        
        for i in header:
            hoja.write(row, col, i)
            col+=1
        
        queryset_update = Users.objects.all()
        
        data = self.serializer_class(queryset_update, many=True)
        
        users_data = []
        
        for i in data.data:
            data_user = []
            for j in i:
                data_user.append(i[j])
                
            c1, c2 = data_user.pop(-2), data_user.pop(-2)
            
            co1 = ''

            if Course.objects.filter(pk=c1).exists():
                co1 = Course.objects.filter(pk=c1).first().text
            
            invoice_user_id = data_user.pop()
            data_user.append(co1)
            
            if invoice_user_id:
                invoice = Invoice.objects.filter(pk=invoice_user_id).first()
                invoice_serializer = InvoiceSerializer(invoice)
                
                for i in invoice_serializer.data:
                    data_user.append(invoice_serializer.data[i])
                
            users_data.append(data_user)
            
        row = 1
        col = 0
            
        for _user_data in users_data:
            col = 0
            for i in _user_data:
                hoja.write(row, col, i)
                col+=1
            row+=1
        
        libro.close()
        
        file_path = os.getcwd() + '/users.xls'
        
        with open(file_path, 'rb') as f:
           file_data = f.read()
        
        response = HttpResponse(file_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=usuarios.xls'

        return response