from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('search/', views.course_search, name='course_search'),
    path('<int:course_id>/register/', views.register_course, name='register_course'), 
  
     path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/test/', views.take_test, name='take_test'),
    path('<int:course_id>/submit_test/', views.submit_test, name='submit_test'),
     path('<int:course_id>/upload_video/', views.upload_video, name='upload_video'),
     path('courses/<int:course_id>/certificate/',views.certificate_view, name='certificate_view'),
     path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),
      path('unregister_course/<int:registration_id>/', views.unregister_course, name='unregister_course'),
       path('videos/<int:video_id>/add_comment/', views.add_comment, name='add_comment'),
       path('video_feed/', views.video_feed, name='video_feed'),
    path('courses/<int:course_id>/submit_test/', views.submit_test, name='submit_test'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
