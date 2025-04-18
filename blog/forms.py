from django import forms
from .models import Comment, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = 'form-control bg-dark text-light border-secondary'
            else:
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_class} form-control bg-dark text-light border-secondary'
                field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 4,
                'placeholder': 'Write a comment...',
                'style': 'resize: vertical;'
            }),
        }
        labels = {
            'body': '',  # без заголовку над полем
        }




class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your name",
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Enter your email'
        })
    )
    message = forms.CharField(
        label="Your message",
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Write your message...',
            'rows': 6
        })
    )
