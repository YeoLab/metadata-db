# import django forms
from django import forms
# import Post model
from .models import Post

# is a ModelForm
class PostForm(forms.ModelForm):
# which model should be used to create this form
    class Meta:
        model = Post
        # which fields end up in the form
        fields = ('title', 'text',)