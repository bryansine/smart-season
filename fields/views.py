from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from .forms import FieldCreateForm
from django.contrib import messages
from .models import Field, FieldUpdate
from .forms import FieldCreateForm, FieldUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def create_field(request):
    if not (request.user.is_coordinator or request.user.is_superuser):
        messages.error(request, "Access denied. Only Coordinators can create fields.")
        return redirect('fields:dashboard')

    if request.method == 'POST':
        form = FieldCreateForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.created_by = request.user
            field.save()
            messages.success(request, f"Field '{field.name}' created successfully!")
            return redirect('fields:dashboard')
    else:
        form = FieldCreateForm()

    return render(request, 'fields/create_field.html', {'form': form})


@login_required
def update_field(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if not (request.user == field.assigned_agent or request.user.is_coordinator):
        messages.error(request, "You are not authorized to update this field.")
        return redirect('fields:dashboard')

    if request.method == 'POST':
        form = FieldUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.field = field
            update.updated_by = request.user
            update.save()
            
            field.current_stage = update.stage
            field.save()
            
            messages.success(request, f"Status updated for {field.name}!")
            return redirect('fields:dashboard')
    else:
        form = FieldUpdateForm(initial={'stage': field.current_stage})

    return render(request, 'fields/update_field.html', {
        'form': form,
        'field': field
    })
    


@login_required
def dashboard(request):
    user = request.user
    
    if user.is_coordinator or user.is_superuser:
        fields = Field.objects.all().order_by('-updated_at')
        template = 'fields/admin_dashboard.html'
    elif user.is_field_agent:
        fields = Field.objects.filter(assigned_agent=user).order_by('-updated_at')
        template = 'fields/agent_dashboard.html'
    else:
        return redirect('home')

    total_fields = fields.count()
    active_count = 0
    at_risk_count = 0
    completed_count = 0
    stagnant_fields_list = []

    for f in fields:
        status = f.computed_status
        
        if status == 'Active':
            active_count += 1
        elif status == 'At Risk':
            at_risk_count += 1
            stagnant_fields_list.append(f)
        elif status == 'Completed':
            completed_count += 1

    crop_counts = fields.values('crop_type').annotate(count=Count('crop_type')).order_by('-count')
    top_crop = crop_counts.first()['crop_type'] if crop_counts else "N/A"

    priority_alert = f"{at_risk_count} field(s) require immediate inspection" if at_risk_count > 0 else "All systems normal"

    context = {
        'fields': fields,
        'total_fields': total_fields,
        'active_count': active_count,
        'at_risk_count': at_risk_count,
        'completed_count': completed_count,
        'top_crop': top_crop,
        'priority_alert': priority_alert,
    }
    
    return render(request, template, context)