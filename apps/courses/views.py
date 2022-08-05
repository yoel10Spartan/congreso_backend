from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from apps.bursary.models import Bursary
from apps.courses.models import Course, CoursesPay

from apps.courses.serializers import PaymentCourseSerializer
from apps.users.models import Users
from .utils import courses_pre, courses_trans, prices
from datetime import datetime

def get_current_price(item_price):
    data_valid = datetime.fromisoformat(item_price['valid'])
    date_now = datetime.now()
    return item_price['price'] if data_valid > date_now else item_price['future_price']

@api_view(['POST'])
def buy_courses(request):
    course_pre = request.data['course_pre']
    course_transco = request.data['course_transco']
    inscription = request.data['inscription']
    id_user = request.data['id']
    code = request.data.get('code')
    invited_by = request.data.get('invited_by')
    
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
            bursary_code.update(isActive=False, invited_by=invited_by)
            total_pay = 0
   
    user = Users.objects.filter(pk=id_user)
    user.update(
        price_pay=total_pay,
        course_pre=course_pre_ob,
        course_trans=course_trans_ob
    )
   
    return Response({"ok": True, "pay": total_pay})

@api_view(['GET'])
def payment_course_information(request):
    four = CoursesPay.objects.filter(id=4).first()
    five = CoursesPay.objects.filter(id=5).first()
    id_disables = []
    
    if four.persons >= 16:
        id_disables.append(4)
        
    if five.persons >= 16:
        id_disables.append(5)
    
    return Response({
        'list_disabled': id_disables
    })