from django.shortcuts import render, redirect, get_object_or_404
from .models import Holiday
from home_auth.decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime


# 1. Holidays List — Accessible to all logged-in users
@login_required(login_url='login')
def holiday_list(request):
    holidays = Holiday.objects.all()
    today = date.today()

    # Separate upcoming and past holidays
    upcoming_holidays = holidays.filter(end_date__gte=today).order_by('start_date')
    past_holidays = holidays.filter(end_date__lt=today).order_by('-start_date')

    return render(request, 'holiday/holidays.html', {
        'upcoming_holidays': upcoming_holidays,
        'past_holidays': past_holidays,
        'today': today,
    })


# 2. Add a holiday — ADMIN only
@admin_required
def add_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        start_date_str = request.POST.get('start_date', '')
        end_date_str = request.POST.get('end_date', '')
        holiday_type = request.POST.get('holiday_type', 'national')
        description = request.POST.get('description', '').strip()

        # Validation
        errors = []
        if not name:
            errors.append("Holiday name is required.")
        if not start_date_str:
            errors.append("Start date is required.")
        if not end_date_str:
            errors.append("End date is required.")

        if not errors:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date < start_date:
                    errors.append("End date must be equal to or after the start date.")
            except ValueError:
                errors.append("Invalid date format.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'holiday/add-holiday.html', {
                'form_data': request.POST
            })

        Holiday.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            holiday_type=holiday_type,
            description=description,
        )
        messages.success(request, f'✅ The holiday "{name}" has been added successfully.')
        return redirect('holiday_list')

    return render(request, 'holiday/add-holiday.html')


# 3. Edit a holiday — ADMIN only
@admin_required
def edit_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        start_date_str = request.POST.get('start_date', '')
        end_date_str = request.POST.get('end_date', '')
        holiday_type = request.POST.get('holiday_type', 'national')
        description = request.POST.get('description', '').strip()

        # Validation
        errors = []
        if not name:
            errors.append("Holiday name is required.")
        if not start_date_str:
            errors.append("Start date is required.")
        if not end_date_str:
            errors.append("End date is required.")

        if not errors:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date < start_date:
                    errors.append("End date must be equal to or after the start date.")
            except ValueError:
                errors.append("Invalid date format.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'holiday/edit-holiday.html', {'holiday': holiday})

        holiday.name = name
        holiday.start_date = start_date
        holiday.end_date = end_date
        holiday.holiday_type = holiday_type
        holiday.description = description
        holiday.save()
        messages.success(request, f'✅ The holiday "{name}" has been updated successfully.')
        return redirect('holiday_list')

    return render(request, 'holiday/edit-holiday.html', {'holiday': holiday})


# 4. Delete a holiday — ADMIN only (POST only)
@admin_required
def delete_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    if request.method == 'POST':
        name = holiday.name
        holiday.delete()
        messages.success(request, f'🗑️ The holiday "{name}" has been deleted.')
        return redirect('holiday_list')
    # GET: redirect to list (deletion happens via POST modal)
    return redirect('holiday_list')
