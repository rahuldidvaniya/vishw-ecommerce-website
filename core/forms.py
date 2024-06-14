from django import forms
from core.models import ProductReview
from userauths.models import Profile

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['user', 'product', 'review', 'rating']

    widgets = {
        'user': forms.HiddenInput(),
        'product': forms.HiddenInput(),
        'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here'}),
        'rating': forms.TextInput(attrs={'type': 'hidden'}),
    }





class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'phone', 'secondary_phone', 'email'] 

class ContactForm(forms.Form):
    title = forms.ChoiceField(choices=[('primary', 'Primary'), ('secondary', 'Secondary')])
    number = forms.CharField(max_length=20)

class AddressForm(forms.Form):
    title = forms.ChoiceField(choices=[('home', 'Home'), ('office', 'Office'), ('business', 'Business')], label='Title')
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}))

