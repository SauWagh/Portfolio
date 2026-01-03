from django.shortcuts import render,redirect,get_object_or_404
from django.forms import modelformset_factory
from portfolio_app.models import *
from portfolio_app.forms import *
import os

from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


# Create your views here.
def home(request):
    projects= Project.objects.all().order_by('id')
    skills = Skill.objects.all().order_by('id')
    exe = Experience.objects.all().order_by('id')
    cer = Certificate.objects.all().order_by('id')
    pro = Profile.objects.first()
    resume = Resume.objects.first()
    return render(request,'portfolio_app/home.html',{
        'projects' : projects,
        'skills' : skills,
        'exe':exe,
        'cer' :cer,
        'pro':pro,
        'resume':resume,
        })

def project_detail(request, id):
    pro = get_object_or_404(Project, pk = id)

    return render(request, 'portfolio_app/detail.html',{'pro':pro})



def add_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST, request.FILES)

        if project_form.is_valid():
            project_obj = project_form.save()

            images = request.FILES.getlist('project_profile')
            for img in images:
                ProjectImage.objects.create(project=project_obj, image=img)

            features = request.POST.getlist('feature_text')
            for f in features:
                if f.strip():
                    Feature.objects.create(project=project_obj, text=f)

            tech_names = request.POST.getlist('tech_name')
            tech_icons = request.FILES.getlist('tech_icon')

            for name, icon in zip(tech_names, tech_icons):
                if name.strip():
                    TechIcon.objects.create(project=project_obj, tech_name=name, icon=icon)

            tech_used_list = request.POST.getlist('tech_used')
            for t in tech_used_list:
                if t.strip():
                    TechUsed.objects.create(project=project_obj, name=t)

            return redirect('home')

    else:
        project_form = ProjectForm()

    return render(request, 'portfolio_app/add_project.html', {
        'project_form': project_form,
    })



def add_skill(request):
    if request.method == 'POST':
        skill_form = SkillForm(request.POST,request.FILES)

        if skill_form.is_valid():
            skill_form.save()

            return redirect('home')
    else:
        skill_form = SkillForm()

    return render(request,'portfolio_app/add_skill.html',{'skill_form':skill_form})


def dashboard(request):

    projects= Project.objects.all()
    skills = Skill.objects.all()

    exe = Experience.objects.all()
    cer = Certificate.objects.all()

    pro = Profile.objects.first()
    resume = Resume.objects.first()
    return render(request, 'portfolio_app/dashboard.html',{
        'projects' : projects,
        'skills' : skills,
        'exe' : exe,
        'cer' :cer,
        'pro' : pro,
        'resume' : resume,
    })


def update_project(request, id):
    project = get_object_or_404(Project, id=id)

    ImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=0)
    FeatureFormSet = modelformset_factory(Feature, form=FeatureForm, extra=0)
    IconFormSet = modelformset_factory(TechIcon, form=TechIconForm, extra=0)
    TechUsedFormSet = modelformset_factory(TechUsed, form=TechUsedForm, extra=0)

    if request.method == "POST":
        # Main form
        pro_form = ProjectForm(request.POST, request.FILES, instance=project)

        # Child formsets
        img_formset = ImageFormSet(request.POST, request.FILES,
                                   queryset=project.images.all(), prefix="images")
        fea_formset = FeatureFormSet(request.POST,
                                     queryset=project.features.all(), prefix="features")
        icon_formset = IconFormSet(request.POST, request.FILES,
                                   queryset=project.icons.all(), prefix="icons")
        tech_formset = TechUsedFormSet(request.POST,
                                       queryset=project.technologies.all(), prefix="tech")

        # Validate all forms
        if (pro_form.is_valid() and img_formset.is_valid() and
            fea_formset.is_valid() and icon_formset.is_valid() and tech_formset.is_valid()):

            pro_form.save()

            # IMAGES
            images = img_formset.save(commit=False)
            for img in images:
                img.project = project
                img.save()

            # FEATURES
            features = fea_formset.save(commit=False)
            for f in features:
                f.project = project
                f.save()

            # ICONS
            icons = icon_formset.save(commit=False)
            for ic in icons:
                ic.project = project
                ic.save()

            # TECH USED
            techs = tech_formset.save(commit=False)
            for t in techs:
                t.project = project
                t.save()

            return redirect("dashboard")

    else:
        # GET Request - Show pre-filled forms
        pro_form = ProjectForm(instance=project)
        img_formset = ImageFormSet(queryset=project.images.all(), prefix="images")
        fea_formset = FeatureFormSet(queryset=project.features.all(), prefix="features")
        icon_formset = IconFormSet(queryset=project.icons.all(), prefix="icons")
        tech_formset = TechUsedFormSet(queryset=project.technologies.all(), prefix="tech")

    return render(request, "portfolio_app/update.html", {
        "pro_form": pro_form,
        "img_formset": img_formset,
        "fea_formset": fea_formset,
        "icon_formset": icon_formset,
        "tech_formset": tech_formset,
    })




def update_skill(request, id): 
    skill = Skill.objects.get(id=id)

    if request.method == 'POST':
        pro_skill = SkillForm(request.POST, request.FILES, instance=skill)

        if pro_skill.is_valid():
            pro_skill.save()
            return redirect('dashboard')

    else:
        pro_skill = SkillForm(instance=skill)

    return render(request, 'portfolio_app/update_skill.html', {
        'skill': skill,
        'pro_skill': pro_skill,
    })


def delete_project(request,id):
    project = Project.objects.get(id = id)
    project.delete()
    return redirect('home')



def delete_skill(request,id):
    skill= Skill.objects.get(id = id)
    skill.delete()
    return redirect('home')


USERNAME = os.getenv('ADMIN_USERNAME')
PASSWORD = os.getenv('ADMIN_PASSWORD')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == USERNAME and password == PASSWORD:
            request.session["is_logged_in"] = True
            return redirect("dashboard")
        else:
            return render(request, "portfolio_app/home.html", {
                "login_error": "Invalid username or password",
                "open_login": True
            })

    return redirect("home")

def experience(request):

    if request.method == "POST":
        exe = ExperienceForm(request.POST, request.FILES)

        if exe.is_valid():
            exe.save()
        return redirect('home')
    else:
        exe =ExperienceForm()

    return render(request, 'portfolio_app/add_exp.html',{'exe':exe})


def delete_exp(request, id):
    expe = Experience.objects.get(id = id)
    expe.delete()
    return redirect('home')

def update_exe(request,id):
    exe = Experience.objects.get(id = id)
    if request.method == 'POST':
        com_exe = ExperienceForm(request.POST, request.FILES, instance=exe)

        if com_exe.is_valid():
            com_exe.save()
            return redirect('home')
    else:
        com_exe = ExperienceForm(instance=exe)

    return render(request, 'portfolio_app/update_exe.html',{
        'exe':exe,
        'com_exe':com_exe
    })


def certification(request):
    if request.method == 'POST':
        cer = CertificationForm(request.POST,request.FILES)
        if cer.is_valid():
            cer.save()
            return redirect('home')
    else:
        cer = CertificationForm()
    return render(request, 'portfolio_app/add_cer.html',{'cer':cer})



def update_cer(request,id):
    cer = Certificate.objects.get(id=id)
    if request.method == 'POST':
        class_cer = CertificationForm(request.POST, request.FILES, instance=cer)

        if class_cer.is_valid():
            class_cer.save()
            return redirect('home')
    else:
        class_cer = CertificationForm(instance=cer)
    return render(request, 'portfolio_app/update_cer.html',{
        'certificate':cer,
        'class_cer' :class_cer
    })


def delete_cer(request, id):
    cer = Certificate.objects.get(id = id)
    cer.delete()
    return redirect('home')


# send email
def send_email(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"""
        Name: {name}
        Email: {email}
        Message:
        {message}
        """

        send_mail(
            subject=f"Portfolio contact form from {name}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["saurabhwaghamare@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Message sent successfully!")

    return render(request, 'portfolio_app/home.html')


def profile_view(request):
    profile = Profile.objects.first()
    if request.method == 'POST':
        pro_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if pro_form.is_valid():
            pro_form.save()
            return redirect('home')
    else:
        pro_form = ProfileForm(instance=profile)
    return render(request, 'portfolio_app/profile.html',{'pro_form':pro_form})

def profile_update(request,id):
    profile = get_object_or_404(Profile, id = id)
    form = ProfileForm(request.POST or None, request.FILES or None , instance=profile)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'portfolio_app/update_profile.html',{'form':form,'profile':profile})


def add_resume(request):
    if Resume.objects.exists():
        return redirect('update_resume')
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ResumeForm()
    return render(request, 'portfolio_app/add_resume.html', {'form': form})

def update_resume(request):
    resume = get_object_or_404(Resume)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'portfolio_app/update_resume.html', {'form': form})
