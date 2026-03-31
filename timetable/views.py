from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TimeTable
from django.http import JsonResponse, HttpResponse
import csv


@login_required(login_url='login')
def timetable_list(request):
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
        messages.success(request, "Cours ajouté à l'emploi du temps !")
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
        timetable.class_name   = request.POST.get('class_name')
        timetable.day          = request.POST.get('day')
        timetable.start_time   = request.POST.get('start_time')
        timetable.end_time     = request.POST.get('end_time')
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


# ─── Exports Visual Timetabling ───────────────────────────────────────────────

@login_required(login_url='login')
def export_timetable_json(request):
    cours_list = TimeTable.objects.all().order_by('day', 'start_time')
    data = []
    for cours in cours_list:
        data.append({
            'id':         cours.id,
            'day':        cours.day,
            'start_time': cours.start_time.strftime('%H:%M'),
            'end_time':   cours.end_time.strftime('%H:%M'),
            'subject':    cours.subject_name,
            'teacher':    cours.teacher_name,
            'class':      cours.class_name,
        })
    return JsonResponse({'timetable_data': data})


@login_required(login_url='login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="timetable_vt.csv"'
    response.write('\ufeff')  # BOM UTF-8

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Jour', 'Heure debut', 'Heure fin', 'Matiere', 'Enseignant', 'Groupe'])

    for e in TimeTable.objects.all().order_by('day', 'start_time'):  # ← TimeTable corrigé
        writer.writerow([
            e.day,
            e.start_time.strftime('%H:%M'),
            e.end_time.strftime('%H:%M'),
            e.subject_name,
            e.teacher_name,
            e.class_name,
        ])
    return response


@login_required(login_url='login')
def export_ics(request):
    from datetime import date, timedelta

    day_map = {
        'Lundi': 0, 'Mardi': 1, 'Mercredi': 2,
        'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5,
    }
    today  = date.today()
    monday = today - timedelta(days=today.weekday())

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//PreSkool//Timetable//FR',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
    ]

    for e in TimeTable.objects.all().order_by('day', 'start_time'):  # ← TimeTable corrigé
        offset     = day_map.get(e.day, 0)
        event_date = monday + timedelta(days=offset)
        dtstart    = f"{event_date.strftime('%Y%m%d')}T{e.start_time.strftime('%H%M%S')}"
        dtend      = f"{event_date.strftime('%Y%m%d')}T{e.end_time.strftime('%H%M%S')}"
        lines += [
            'BEGIN:VEVENT',
            f'DTSTART:{dtstart}',
            f'DTEND:{dtend}',
            f'SUMMARY:{e.subject_name} — {e.class_name}',
            f'DESCRIPTION:Enseignant: {e.teacher_name}',
            f'LOCATION:{e.class_name}',
            'RRULE:FREQ=WEEKLY',
            'END:VEVENT',
        ]

    lines.append('END:VCALENDAR')

    response = HttpResponse('\r\n'.join(lines), content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="timetable_preskool.ics"'
    return response