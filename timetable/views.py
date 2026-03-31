from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TimeTable

@login_required(login_url='login')
def timetable_list(request):
    # On récupère tous les cours et on les trie par jour et par heure
    timetables = TimeTable.objects.all().order_by('day', 'start_time')
    return render(request, 'timetable/timetable-list.html', {'timetables': timetables})

@login_required(login_url='login')
def add_timetable(request):
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé.")
        return redirect('timetable_list')

    if request.method == 'POST':
        TimeTable.objects.create(
            teacher_name=request.POST.get('teacher_name'),
            subject_name=request.POST.get('subject_name'),
            class_name=request.POST.get('class_name'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
        messages.success(request, 'Cours ajouté à l\'emploi du temps !')
        return redirect('timetable_list')
        
    return render(request, 'timetable/add-timetable.html')

@login_required(login_url='login')
def edit_timetable(request, id):
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé.")
        return redirect('timetable_list')

    timetable = TimeTable.objects.get(id=id)

    if request.method == 'POST':
        timetable.teacher_name = request.POST.get('teacher_name')
        timetable.subject_name = request.POST.get('subject_name')
        timetable.class_name = request.POST.get('class_name')
        timetable.day = request.POST.get('day')
        timetable.start_time = request.POST.get('start_time')
        timetable.end_time = request.POST.get('end_time')
        timetable.save()
        
        messages.success(request, 'Cours modifié avec succès !')
        return redirect('timetable_list')

    return render(request, 'timetable/edit-timetable.html', {'timetable': timetable})

@login_required(login_url='login')
def delete_timetable(request, id):
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé.")
        return redirect('timetable_list')

    timetable = TimeTable.objects.get(id=id)
    timetable.delete()
    messages.success(request, 'Cours supprimé avec succès !')
    return redirect('timetable_list')