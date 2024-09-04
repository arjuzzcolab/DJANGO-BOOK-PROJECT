from django import forms 
from .models import Book,Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Book Name'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder': 'Enter Book Price'}),
            'Author': forms.Select(attrs={'class':'form-control','placeholder':'Enter Author Name'})
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

