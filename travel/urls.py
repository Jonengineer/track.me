from django.urls import path
from .import views

app_name = 'travel'

urlpatterns = [
    path('3Dmap/<int:travelplan_id>/', views.get_travel_plan_3D, name='3Dmap'),
    path('CreateTravelPlan/', views.create_travel_plan, name='create_travel_plan'),
    path('GetTravelPlan/', views.get_travel_plan, name='get_travel_plan'),
    path('TravelDetailChart/<int:travelplan_id>/', views.travel_detail_chart, name='travel_detail_chart'),    
    path('DeleteTravelPlan/<int:travelplan_id>/', views.delete_travel_plan, name='delete_travel_plan'),
    path('TravelDetailFull/<int:travelplan_id>/', views.travel_detail_full, name='travel_detail_full'),
    path('AddPointTrek/<int:travelplan_id>/', views.add_point_trek, name='add_point_trek'),
    path('DeleteTravelPoint/<int:point_trek_id>/', views.delete_travel_point, name='delete_travel_point'),
    path('UploadVideo', views.upload_video, name='upload_video'),
    path('TravelDescription/<int:travelplan_id>/', views.travel_description, name='travel_description'),
    path('AddMediaTravel/<int:travelplan_id>/', views.add_media_travel, name='add_media_travel'),
    path('AddDescriptionTravel/<int:travelplan_id>/', views.add_description_travel, name='add_description_travel'),
    path('TravelFinance/<int:travelplan_id>/', views.travel_finance, name='travel_finance'),
    path('AddTravelFinance/<int:travelplan_id>/', views.add_travel_finance, name='add_travel_finance'),
    path('Expense/delete/<int:expense_id>/<int:travelplan_id>/', views.delete_expense, name='delete_expense'),
]
