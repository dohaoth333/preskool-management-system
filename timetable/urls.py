from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.timetable_list,        name='timetable_list'),
    path('add/',             views.add_timetable,         name='add_timetable'),
    path('edit/<int:id>/',   views.edit_timetable,        name='edit_timetable'),
    path('delete/<int:id>/', views.delete_timetable,      name='delete_timetable'),
    path('export/json/',     views.export_timetable_json, name='export_timetable_json'),
    path('export/csv/',      views.export_csv,            name='export_csv'),
    path('export/ics/',      views.export_ics,            name='export_ics'),             
]