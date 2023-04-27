from django import forms
from .models import News, Comments

class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = News
        fields = ('title',
                  'text',
                  'category',
                  'image')
        labels = {"title": 'Заголовок...',
                  "text": 'Текст...',
                  'category': "Выберите категорию...",
                  'image': 'Выберите изображение...'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80}),
                   'image': forms.ClearableFileInput(attrs={"multiple": True})}



class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Comments
        fields = ('comment',)
        labels = {'comment': 'Комментарий...'}
        # widgets = {'comment': forms.Textarea(attrs={'cols': 40, })}