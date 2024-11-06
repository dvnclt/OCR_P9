from django import forms


class PostReviewForm(forms.Form):
    post_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(),
        label="Titre"
    )
    post_content = forms.CharField(
        widget=forms.Textarea(),
        label="Description"
    )
    post_image = forms.ImageField(
        label="Image"
    )
    review_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(),
        label="Titre"
    )
    review_rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.Select(choices=[(i, i) for i in range(1, 6)]),
        label="Note"
    )
    review_content = forms.CharField(
        widget=forms.Textarea(),
        label="Commentaire"
    )
