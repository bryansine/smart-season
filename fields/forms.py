from django import forms
from .models import Field
from users.models import User
from .models import FieldUpdate

class FieldCreateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'crop_type', 'planting_date', 'assigned_agent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. North Section B'}),
            'crop_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Maize'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_agent': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_agent'].queryset = User.objects.filter(is_field_agent=True)
        self.fields['assigned_agent'].empty_label = "Select an Agent to assign"


class FieldUpdateForm(forms.ModelForm):
    class Meta:
        model = FieldUpdate
        fields = ['stage', 'notes']
        widgets = {
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the crop health, pests, or soil moisture...'}),
        }
        


        
        

