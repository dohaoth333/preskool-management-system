from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TimeTable, ScheduleProposal
from django.http import JsonResponse, HttpResponse
import csv


@login_required(login_url='login')
def timetable_list(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timetables_by_day = {day: [] for day in days}
    # Fetch and sort by start_time. day sorting is handled by the dictionary order
    for t in TimeTable.objects.all().order_by('start_time'):
        if t.day in timetables_by_day:
            timetables_by_day[t.day].append(t)
            
    return render(request, 'timetable/timetable-list.html', {
        'timetables_by_day': timetables_by_day
    })


@login_required(login_url='login')
def add_timetable(request):
    # Strictly for admins
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied. Only admins can modify the main timetable directly.")
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
        messages.success(request, "Class added to timetable successfully!")
        return redirect('timetable_list')

    return render(request, 'timetable/add-timetable.html')


@login_required(login_url='login')
def edit_timetable(request, id):
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    timetable = get_object_or_404(TimeTable, id=id)

    if request.method == 'POST':
        timetable.teacher_name = request.POST.get('teacher_name')
        timetable.subject_name = request.POST.get('subject_name')
        timetable.class_name   = request.POST.get('class_name')
        timetable.day          = request.POST.get('day')
        timetable.start_time   = request.POST.get('start_time')
        timetable.end_time     = request.POST.get('end_time')
        timetable.save()
        messages.success(request, 'Class updated successfully!')
        return redirect('timetable_list')

    return render(request, 'timetable/edit-timetable.html', {'timetable': timetable})


@login_required(login_url='login')
def delete_timetable(request, id):
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    timetable = get_object_or_404(TimeTable, id=id)
    timetable.delete()
    messages.success(request, 'Class deleted successfully!')
    return redirect('timetable_list')


# ─── New Proposal System ───────────────────────────────────────────────────

@login_required(login_url='login')
def add_proposal(request):
    if not getattr(request.user, 'is_teacher', False) and not request.user.is_superuser:
        messages.error(request, "Only teachers can request a schedule.")
        return redirect('timetable_list')

    if request.method == 'POST':
        ScheduleProposal.objects.create(
            teacher=request.user,
            teacher_name=f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username,
            subject_name=request.POST.get('subject_name'),
            class_name=request.POST.get('class_name'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
        messages.success(request, "Your schedule proposal has been submitted for review.")
        return redirect('my_proposals')

    return render(request, 'timetable/add-proposal.html', {
        'days': TimeTable.DAYS_OF_WEEK
    })


@login_required(login_url='login')
def my_proposals(request):
    if not getattr(request.user, 'is_teacher', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    proposals = ScheduleProposal.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'timetable/my-proposals.html', {'proposals': proposals})


@login_required(login_url='login')
def review_proposals(request):
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    proposals = ScheduleProposal.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'timetable/review-proposals.html', {'proposals': proposals})


@login_required(login_url='login')
def approve_proposal(request, id):
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    proposal = get_object_or_404(ScheduleProposal, id=id)
    
    # Create the Live Timetable entry
    TimeTable.objects.create(
        teacher_name=proposal.teacher_name,
        subject_name=proposal.subject_name,
        class_name=proposal.class_name,
        day=proposal.day,
        start_time=proposal.start_time,
        end_time=proposal.end_time
    )
    
    # Mark as approved
    proposal.status = 'approved'
    proposal.save()
    
    messages.success(request, f"Proposal for {proposal.subject_name} approved and added to timetable.")
    return redirect('review_proposals')


@login_required(login_url='login')
def reject_proposal(request, id):
    if not getattr(request.user, 'is_admin', False) and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('timetable_list')

    proposal = get_object_or_404(ScheduleProposal, id=id)
    proposal.status = 'rejected'
    proposal.admin_remarks = request.POST.get('remarks', 'Rejected by admin.')
    proposal.save()
    
    messages.success(request, f"Proposal for {proposal.subject_name} has been rejected.")
    return redirect('review_proposals')


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
    writer.writerow(['Day', 'Start Time', 'End Time', 'Subject', 'Teacher', 'Group'])

    for e in TimeTable.objects.all().order_by('day', 'start_time'):
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
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
        'Thursday': 3, 'Friday': 4, 'Saturday': 5,
    }
    today  = date.today()
    monday = today - timedelta(days=today.weekday())

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//PreSkool//Timetable//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
    ]

    for e in TimeTable.objects.all().order_by('day', 'start_time'):
        offset     = day_map.get(e.day, 0)
        event_date = monday + timedelta(days=offset)
        dtstart    = f"{event_date.strftime('%Y%m%d')}T{e.start_time.strftime('%H%M%S')}"
        dtend      = f"{event_date.strftime('%Y%m%d')}T{e.end_time.strftime('%H%M%S')}"
        lines += [
            'BEGIN:VEVENT',
            f'DTSTART:{dtstart}',
            f'DTEND:{dtend}',
            f'SUMMARY:{e.subject_name} — {e.class_name}',
            f'DESCRIPTION:Teacher: {e.teacher_name}',
            f'LOCATION:{e.class_name}',
            'RRULE:FREQ=WEEKLY',
            'END:VEVENT',
        ]

    lines.append('END:VCALENDAR')

    response = HttpResponse('\r\n'.join(lines), content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="timetable_preskool.ics"'
    return response