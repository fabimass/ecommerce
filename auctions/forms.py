from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget=forms.TextInput(attrs={
        'autocomplete':'off', 
        'class': 'form-control'}))
    price = forms.DecimalField(label="Price", required=True, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control'}))
    category = forms.CharField(label="Category (Optional)", required=False, widget=forms.TextInput(attrs={
        'autocomplete':'off', 
        'class': 'form-control'}))
    image= forms.CharField(label="Image URL (Optional)", required=False, widget=forms.URLInput(attrs={
        'autocomplete':'off', 
        'class': 'form-control'}))
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea(attrs={
        'class': 'form-control'}))

class BidForm(forms.Form):
    price = forms.DecimalField(label='', required=True, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Bid'}))

class MessageForm(forms.Form):
    message = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Add new message',
        'style': 'height: 120px'}))