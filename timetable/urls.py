from django.urls import path
from . import views

urlpatterns = [
    # Live Timetable
    path('',                 views.timetable_list,        name='timetable_list'),
    path('add/',             views.add_timetable,         name='add_timetable'),
    path('edit/<int:id>/',   views.edit_timetable,        name='edit_timetable'),
    path('delete/<int:id>/', views.delete_timetable,      name='delete_timetable'),
    
    # Proposal System
    path('proposals/add/',    views.add_proposal,         name='add_proposal'),
    path('proposals/my/',     views.my_proposals,         name='my_proposals'),
    path('proposals/review/', views.review_proposals,     name='review_proposals'),
    path('proposals/approve/<int:id>/', views.approve_proposal, name='approve_proposal'),
    path('proposals/reject/<int:id>/',  views.reject_proposal,  name='reject_proposal'),
    
    # Exports
    path('export/json/',     views.export_timetable_json, name='export_timetable_json'),
    path('export/csv/',      views.export_csv,            name='export_csv'),
    path('export/ics/',      views.export_ics,            name='export_ics'),             
]