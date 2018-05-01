from django.core.exceptions import ValidationError

def clean_email(self):
    email = self.cleaned_data.get("email")
    if( ".edu" in email):
        raise forms.ValidationError("Not a Valid Email")
    return email

CATEGORIES = ['Mexican', 'Asian', 'American', 'Whatever']

def validate_category(value):
    cat = value.capitalize()
    if not value in CATEGORIES and not cat in CATEGORIES:
        raise ValidationError("Not in Categories")
