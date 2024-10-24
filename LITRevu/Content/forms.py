from django import forms


class PostReviewForm(forms.Form):
    post_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Titre du post'})
    )
    post_content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Contenu du post'})
    )
    review_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Titre de la critique'})
    )
    review_content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Contenu de la critique'})
    )
