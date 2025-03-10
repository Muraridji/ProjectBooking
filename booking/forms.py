from django import forms

class PlaceFilterForm(forms.Form):
    capacity = forms.IntegerField(
        label="Мінімальна ємність", required=False, min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    price = forms.IntegerField(
        label="Максимальна ціна", required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    start_time = forms.DateField(
        label="Від", required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_time = forms.DateField(
        label="До", required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

class BookingForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))
    start_time = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}))
    end_time = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Невірні дати бронювання")
        
        return cleaned_data
