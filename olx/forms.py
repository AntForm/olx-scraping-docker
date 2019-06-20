from django import forms
from olx.models import OlxRequest

class RequestForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model=OlxRequest
        exclude = ['datetime_add_request']
