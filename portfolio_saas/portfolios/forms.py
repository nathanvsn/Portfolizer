from django import forms
from .models import Project, Resource
from taggit.forms import TagWidget

class ProjectForm(forms.ModelForm):
    MAX_TAGS = 3 
    
    class Meta:
        MAX_TAGS = 3
        model = Project
        fields = ['name', 'description', 'tags', 'img', 'markdown_content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Projeto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descrição curta do Projeto', 'maxlength': 400}),
            # O campo de tags deve ter um placeholder claro e ser gerido via JavaScript
            'tags': forms.HiddenInput(),  # Usamos HiddenInput porque vamos gerenciar via JavaScript
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'markdown_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Projeto em Markdown'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProjectForm, self).__init__(*args, **kwargs)

        if user and user.is_ultra:
            self.fields['html_content'] = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
            self.fields['css_content'] = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
            self.fields['js_content'] = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_tags(self):
        tags = self.cleaned_data['tags']

        # Verifica se o número de tags excede o limite
        if len(tags) > self.MAX_TAGS:
            raise forms.ValidationError(f'Você pode adicionar no máximo {self.MAX_TAGS} tags.')

        return tags  # Retorna a lista diretamente, sem usar 'split'


    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)

        # Salvando arquivos específicos para usuários Ultra
        if 'html_content' in self.cleaned_data:
            project.html_content = self.cleaned_data['html_content']
        if 'css_content' in self.cleaned_data:
            project.css_content = self.cleaned_data['css_content']
        if 'js_content' in self.cleaned_data:
            project.js_content = self.cleaned_data['js_content']

        if commit:
            project.save()
            self.save_m2m()
        return project
    
# Formulário para upload de recursos (imagens, arquivos adicionais)
class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(ResourceUploadForm, self).__init__(*args, **kwargs)
        
        # Verificar se o usuário pode adicionar mais imagens ou recursos
        if project and not project.can_upload_more_images:
            self.fields['file'].disabled = True
            self.fields['file'].help_text = "Você atingiu o limite de upload de imagens para este projeto."
