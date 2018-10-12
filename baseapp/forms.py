from django import forms
from object.models import Post, PostProfile, PostChatPhoto


class PostCreateForm(forms.ModelForm):

    whose = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'whose'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}))
    title_content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title_content'}), required=False)
    description_content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'description_content'}), required=False)

    class Meta:
        model = Post
        fields = ['whose', 'name', 'description', 'title_content', 'description_content']


class PostProfilePhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    rotate = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = PostProfile
        fields = ('file_300', 'file_50', 'x', 'y', 'width', 'height', 'rotate',)


class PostChatPhotoForm(forms.ModelForm):
    rotate = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = PostChatPhoto
        fields = ('file', 'rotate',)