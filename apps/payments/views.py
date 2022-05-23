import os
from telnetlib import STATUS
from tkinter.messagebox import NO
from unittest import result
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

import stripe
from apps.courses.models import CoursesPay

from apps.users.models import Users

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

import qrcode
import qrcode.image.svg
from io import BytesIO

from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string

stripe.api_key = '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'
# stripe.api_key = ''

def send_email(email_str: str, context: dict):
    try:
        template = get_template('index.html')
        
        content = template.render(context)
        
        # content = render_to_string(template_name='index.html', context=context)
        
        email = EmailMultiAlternatives(
            'Congreso',
            'Congreso',
            settings.EMAIL_HOST_USER,
            [
                email_str,
                'femengi@yahoo.com.mx',
                'contacto@ole-sfera.com',
                'franco@ole-sfera.com',
                'munozzecuayoel@gmail.com',
            ]
        )
        email.attach_alternative(content, 'text/html')
        email.send()
    except:
        print('error')
        raise Response('Error')
    
@api_view(['POST'])
def send_email_user(request):
    user_id = request.data['user_id']
    user = Users.objects.filter(pk=user_id).first()
    
    course_pre = user.course_pre
    course_trans = user.course_trans
    
    if course_pre.id == 4:
        four_persons = CoursesPay.objects.filter(id=4).first()
        CoursesPay.objects.filter(id=4).update(persons=four_persons.persons+1)

    if course_trans.id == 5:
        five_persons = CoursesPay.objects.filter(id=5).first()
        CoursesPay.objects.filter(id=5).update(persons=five_persons.persons+1)

    Users.objects.filter(pk=user_id).update(accredited_payment=True)

    context = {
        'price_pay': user.price_pay,
        'user': user,
        'image': 'https://congreso.icu/media/{}.jpg'.format(user.id),
        'portada': 'https://congreso.icu/media/portada_photo.jpg'
    }
    
    send_email(user.email, context)
    
    return Response({'ok': True})

@api_view(['POST'])
def create_checkout_session(request):
    user_id = request.data['user_id']
    user = Users.objects.filter(pk=user_id).first()
    amount = user.price_pay * 100
    
    course_pre = user.course_pre
    course_trans = user.course_trans
    
    if amount < 10:
        redirect('https://congresosfemeg.xyz/#/success_pay');
        return Response({'session': 0})
    
    name_product_user = 'Producto para {} - nombre {} - {} {}'.format(
        user.id, 
        user.name,
        course_pre,
        course_trans,
    )
    
    product = stripe.Product.create(name=name_product_user)
    
    price = stripe.Price.create(
        unit_amount=amount,
        currency="mxn",
        product=product['id'],
    )
    
    try:
        customer = stripe.Customer.create(
            description=name_product_user,
            address={
                'line1': user.address,
                'postal_code': user.cp,
                'state': user.state,
            },
            email=user.email,
            name=user.name,
            phone=user.phone_number
        )
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price['id'],
                    'quantity': 1
                },
            ],  
            success_url='https://congresosfemeg.xyz/#/success_pay',
            cancel_url='https://congresosfemeg.xyz/#/payment',
            mode='payment',
            customer=customer['id'],
        )
        
        # success_url='https://congresosfemeg.xyz/#/success_pay',
        # cancel_url='https://congresosfemeg.xyz/#/payment',
        
        return Response({'session': checkout_session['id']})
    except Exception as e:
        return Response({'session': None}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def course_payment(request):
    user_id = request.data.get('user_id')

    user = Users.objects.filter(pk=user_id).first()
    amount = user.price_pay * 100

    if amount >= 10:
        id = request.data.get('id')
        description = request.data.get('description')

    try:

        print('Init Amount')

        if amount >= 10:
           
            
            customer_stripe = stripe.Customer.create(
                description=description,
                address={
                    'line1': user.address,
                    'postal_code': user.cp,
                    'state': user.state,
                },
                email=user.email,
                name=user.name,
                phone=user.phone_number
            )
            
            paymentin = stripe.PaymentIntent.create(
                amount=amount, 
                currency='mxn', 
                payment_method_types=['card'],
                receipt_email='munozzecuayoel@gmail.com',
                payment_method=id,
                description=description,
                customer=customer_stripe['id']
            )
            
            stripe.PaymentIntent.confirm(
                paymentin['id'],
                payment_method=id,
                receipt_email=user.email
            )
            
        print('Finish Mount')

        course_pre = user.course_pre
        course_trans = user.course_trans
        
        print('Init Courses')

        if course_pre.id == 4:
            four_persons = CoursesPay.objects.filter(id=4).first()
            CoursesPay.objects.filter(id=4).update(persons=four_persons.persons+1)

        if course_trans.id == 5:
            five_persons = CoursesPay.objects.filter(id=5).first()
            CoursesPay.objects.filter(id=5).update(persons=five_persons.persons+1)

        # 'image': 'http://144.126.210.41/media/{}.jpg'.format(user.id),
        # 'portada': 'http://144.126.210.41/media/portada.jpg'

        # 'image': 'http://127.0.0.1:8080/media/{}.jpg'.format(user.id),
        # 'portada': 'http://127.0.0.1:8080/media/portada.jpg'

        # 'image': 'https://www.congreso.icu/media/{}.jpg'.format(user.id),
        #     'portada': 'https://www.congreso.icu/media/portada.jpg'

        print('init context')

        context = {
            'price_pay': user.price_pay,
            'user': user,
            'image': 'https://congreso.icu/media/{}.jpg'.format(user.id),
            'portada': 'https://congreso.icu/media/portada.jpg'
        }
        
        print('Send Email')

        send_email(user.email, context)

        print('Finish Email')

        return Response({'ok': True})
    except stripe.error.StripeError as e:
        raise Response({'ok': False})

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

@api_view(['POST'])
def generate_pdf(request):
    user_id = request.data['user_id']

    user = Users.objects.filter(pk=user_id).first()

    # 'image': 'http://144.126.210.41/media/{}.jpg'.format(user.id),
    #     'portada': 'http://144.126.210.41/media/portada.jpg'

    # 'image': 'http://127.0.0.1:8080/media/{}.jpg'.format(user.id),
    # 'portada': 'http://127.0.0.1:8080/media/portada.jpg'

    # 'image': 'https://www.congreso.icu/media/{}.jpg'.format(user.id),
    #     'portada': 'https://www.congreso.icu/media/portada.jpg'

    context = {
        'price_pay': user.price_pay,
        'user': user,
        'image': 'https://congreso.icu/media/{}.jpg'.format(user.id),
        'portada': 'https://congreso.icu/media/portada_photo.jpg'
    }

    template = get_template('index.html')
    html = template.render(context)

    file = open(os.path.join(settings.MEDIA_ROOT, '{}.pdf'.format(user.id)), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file, link_callback=link_callback)
    file.seek(0)
    pdf = file.read()
    file.close ()

    # 'link': 'http://127.0.0.1:8080/media/{}.pdf'.format(user.id)
    # 'link': 'http://144.126.210.41/media/{}.pdf'.format(user.id)

    # 'link': 'https://www.congreso.icu/media/{}.pdf'.format(user.id)

    return Response({
        'link': 'https://congreso.icu/media/{}.pdf'.format(user.id)
    })

# <img class="qr" src="https://qrcode.tec-it.com/API/QRCode?data=smsto%3A555-555-5555%3AGenerador+de+C%C3%B3digos+QR+de+TEC-IT" alt="qr">
# <div style="margin: auto">
#     {{ svg|safe }}
# </div>
# <img class="qr" src={{ image }} alt="qr">