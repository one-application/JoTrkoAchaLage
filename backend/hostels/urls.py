from django.urls import path
from .views import (
    hostels, available_rooms, apply_hostel, user_allotments,
    messes, subscribe_mess, user_mess_subscriptions, mess_menu,
    create_complaint, user_complaints, all_complaints, update_complaint_status
)

urlpatterns = [
    # Hostel endpoints
    path('hostels/', hostels, name='hostels'),
    path('hostels/<int:hostel_id>/rooms/', available_rooms, name='available-rooms'),
    path('allotments/apply/', apply_hostel, name='apply-hostel'),
    path('allotments/', user_allotments, name='user-allotments'),
    
    # Mess endpoints
    path('messes/', messes, name='messes'),
    path('mess/subscribe/', subscribe_mess, name='subscribe-mess'),
    path('mess/subscriptions/', user_mess_subscriptions, name='user-mess-subscriptions'),
    path('mess/<int:mess_id>/menu/', mess_menu, name='mess-menu'),
    
    # Complaint endpoints
    path('complaints/', create_complaint, name='create-complaint'),
    path('complaints/my/', user_complaints, name='user-complaints'),
    path('complaints/all/', all_complaints, name='all-complaints'),
    path('complaints/<int:complaint_id>/status/', update_complaint_status, name='update-complaint-status'),
]
