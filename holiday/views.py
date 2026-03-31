from django.shortcuts import render, redirect, get_object_or_404
from .models import Holiday
from home_auth.decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime


# 1. Liste des jours fériés — Accessible à tous les utilisateurs connectés
@login_required(login_url='login')
def holiday_list(request):
    holidays = Holiday.objects.all()
    today = date.today()

    # Séparer les jours fériés à venir et passés
    upcoming_holidays = holidays.filter(end_date__gte=today).order_by('start_date')
    past_holidays = holidays.filter(end_date__lt=today).order_by('-start_date')

    return render(request, 'holiday/holidays.html', {
        'upcoming_holidays': upcoming_holidays,
        'past_holidays': past_holidays,
        'today': today,
    })


# 2. Ajouter un jour férié — ADMIN seulement
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
            errors.append("Le nom du jour férié est obligatoire.")
        if not start_date_str:
            errors.append("La date de début est obligatoire.")
        if not end_date_str:
            errors.append("La date de fin est obligatoire.")

        if not errors:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date < start_date:
                    errors.append("La date de fin doit être égale ou postérieure à la date de début.")
            except ValueError:
                errors.append("Le format de date est invalide.")

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
        messages.success(request, f'✅ Le jour férié "{name}" a été ajouté avec succès.')
        return redirect('holiday_list')

    return render(request, 'holiday/add-holiday.html')


# 3. Modifier un jour férié — ADMIN seulement
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
            errors.append("Le nom du jour férié est obligatoire.")
        if not start_date_str:
            errors.append("La date de début est obligatoire.")
        if not end_date_str:
            errors.append("La date de fin est obligatoire.")

        if not errors:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date < start_date:
                    errors.append("La date de fin doit être égale ou postérieure à la date de début.")
            except ValueError:
                errors.append("Le format de date est invalide.")

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
        messages.success(request, f'✅ Le jour férié "{name}" a été modifié avec succès.')
        return redirect('holiday_list')

    return render(request, 'holiday/edit-holiday.html', {'holiday': holiday})


# 4. Supprimer un jour férié — ADMIN seulement (POST uniquement)
@admin_required
def delete_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    if request.method == 'POST':
        name = holiday.name
        holiday.delete()
        messages.success(request, f'🗑️ Le jour férié "{name}" a été supprimé.')
        return redirect('holiday_list')
    # GET : redirige vers la liste (la suppression se fait via modal POST)
    return redirect('holiday_list')
