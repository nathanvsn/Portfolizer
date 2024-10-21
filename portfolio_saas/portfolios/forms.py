from django import forms
from .models import Project, Resource

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'markdown_content', 'html_content', 'css_content', 'js_content']

    def clean(self):
        cleaned_data = super().clean()
        user_type = self.instance.portfolio.user.profile.user_type
        
        # Lógica de validação personalizada para usuários Ultra
        if user_type == 'ultra' and not cleaned_data.get('html_content'):
            raise forms.ValidationError('Usuários Ultra precisam fornecer conteúdo HTML.')
        
        return cleaned_data
    
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['file']

    def clean(self):
        cleaned_data = super().clean()
        project = self.instance.project
        
        # Verifica se o usuário pode fazer mais uploads
        if not project.can_upload_more_resources:
            raise forms.ValidationError('Limite de upload de recursos atingido para seu plano.')
        
        return cleaned_data

