from django.urls import path
from .import views

app_name = 'travel'

urlpatterns = [
    path('3Dmap/<int:travelplan_id>/', views.get_travel_plan_3D, name='3Dmap'),
    path('CreateTravelPlan/', views.create_travel_plan, name='create_travel_plan'),
    path('map/', views.map_page, name='map_page'),
    path('getTravelPlan/', views.get_travel_plan, name='get_travel_plan'),
    path('travel_detail_chart/<int:travelplan_id>/', views.travel_detail_chart, name='travel_detail_chart'),    
    path('delete_travel_plan/<int:travelplan_id>/', views.delete_travel_plan, name='delete_travel_plan'),
    path('travel_detail_full/<int:travelplan_id>/', views.travel_detail_full, name='travel_detail_full'),
    path('add_point_trek/<int:travelplan_id>/', views.add_point_trek, name='add_point_trek'),   
]
