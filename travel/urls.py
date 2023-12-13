from django.urls import path
from .import views

app_name = 'travel'

urlpatterns = [
    path('3Dmap/<int:travelplan_id>/', views.get_travel_plan_3D, name='3Dmap'),
    path('CreateTravelPlan/', views.create_travel_plan, name='create_travel_plan'),
    path('getTravelPlan/', views.get_travel_plan, name='get_travel_plan'),
    path('travel_detail_chart/<int:travelplan_id>/', views.travel_detail_chart, name='travel_detail_chart'),    
    path('delete_travel_plan/<int:travelplan_id>/', views.delete_travel_plan, name='delete_travel_plan'),
    path('travel_detail_full/<int:travelplan_id>/', views.travel_detail_full, name='travel_detail_full'),
    path('add_point_trek/<int:travelplan_id>/', views.add_point_trek, name='add_point_trek'),
    path('delete_travel_point/<int:point_trek_id>/', views.delete_travel_point, name='delete_travel_point'),
    path('upload-video', views.upload_video, name='upload_video'),
    path('travel_description/<int:travelplan_id>/', views.travel_description, name='travel_description'),
    path('add_media_travel/<int:travelplan_id>/', views.add_media_travel, name='add_media_travel'),
    path('add_description_travel/<int:travelplan_id>/', views.add_description_travel, name='add_description_travel'),
    path('travel_finance/<int:travelplan_id>/', views.travel_finance, name='travel_finance'),
    path('add_travel_finance/<int:travelplan_id>/', views.add_travel_finance, name='add_travel_finance'),
]
