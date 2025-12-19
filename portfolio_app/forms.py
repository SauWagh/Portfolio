from django import forms
from portfolio_app.models import*

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_video','project_des', 'live_demo','github_link']

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['text']

class TechIconForm(forms.ModelForm):
    class Meta:
        model = TechIcon
        fields = ['icon', 'tech_name']

class TechUsedForm(forms.ModelForm):
    class Meta:
        model = TechUsed
        fields = ['name'] 

        
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name', 'icon']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']