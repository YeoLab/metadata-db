from django import forms
from .models import Post

# is a ModelForm
class PostForm(forms.ModelForm):
# which model should be used to create this form
    class Meta:
        model = Post
        fields = ('title', 'text',)