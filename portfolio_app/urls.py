from django.urls import path
from portfolio_app.views import*
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('detail/<int:id>',project_detail, name='detail'),
    path('add/',add_project,name ='add'),
    path('skill/',add_skill,name='skill'),
    path('dashboard/',dashboard,name='dashboard'),
    
    path('project/<int:id>/update/', update_project, name='update_project'),
    path('skill<int:id>/update/',update_skill, name='update_skill'),
    path('project/<int:id>/delete/', delete_project, name='delete_project'),
    path('skill/<int:id>/delete/', delete_skill,name="delete_skill"),

    path('add_exp/',experience, name='add_exp'),
    path('add_cer/',certification, name='add_cer'),

    path('experience/<int:id>/update/',update_exe, name='experience_update'),
    path('certification<int:id>/update/',update_cer,name='certification_update'),

    path('experience/<int:id>/delete/',delete_exp, name='experience_delete'),
    path('certification/<int:id>/delete',delete_cer, name='certification_delete'),

    path('profile/',profile_view,name='profile'),
    path('profile/<int:id>/update/',profile_update, name='profile_update'),

    path('resume/',add_resume,name='resume'),
    path('resume/update/', update_resume, name='resume_update'), 

    path('send_email/', send_email, name='send_email'),

    path('login',login_view, name='login')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)