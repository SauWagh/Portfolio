from django.db import models
from django.core.exceptions import ValidationError

class Project(models.Model):

    def validator_video(value):
        valid_Extension = ['.mp4','.mov','.avi','.mkv']

        if not any(value.name.lower().endswith(ext) for ext in valid_Extension):
            raise ValidationError('Only video files (.mp4, .mov, .avi, .mkv) are allowed.')
    

    project_title = models.CharField('Project Name', max_length=100)
    project_video = models.FileField('Project Video',upload_to = "portfolio_app/videos", validators = [validator_video],blank=True, null=True)
    project_des = models.TextField('Project Description')
    live_demo = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.project_title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio_app/profile')


class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    text = models.CharField('Feature', max_length=200)

    def __str__(self):
        return self.text


class TechIcon(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='icons')
    icon = models.ImageField(upload_to='portfolio_app/icon',blank=True,null=True)
    tech_name = models.CharField(max_length=30)

    def __str__(self):
        return self.tech_name


class TechUsed(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField('Technology Used', max_length=50)

    def __str__(self):
        return self.name


class Skill(models.Model):

    CATEGORY_CHOICES = [
        ('languages', 'Languages'),               
        ('frameworks', 'Frameworks/Libraries'),
        ('frontend','Frontend Technologies'),
        ('backend','backend Technologies'),
        ('databases','Databases'),
        ('ml/ds', 'ML/Data Science'),                       
        ('cloud', 'Cloud/DevOps'),       
        ('tools','Tools')         
    ]


    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES,default='languages')
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='portfolio/icon',blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    
    compony_name = models.CharField('Compony Name',max_length=100)
    compony_des = models.TextField('Description',)
    duration = models.CharField('Duration' ,blank=False,max_length=50)
    certificate_link = models.URLField('Certificate Link', blank=True, null=True)

    def __str__(self):
        return self.compony_name
    
class Certificate (models.Model):
    certificate_name = models.CharField("Certification Name",max_length=30)
    link = models.URLField('Link', blank=True, null=True)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return self.name
    
class Resume(models.Model):
    file = models.URLField()
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Resume"
