from django.contrib import admin

from apps.courses.models import CategoryCourse, Course, CoursesPay


admin.site.register(CoursesPay)

admin.site.register(CategoryCourse)

admin.site.register(Course)