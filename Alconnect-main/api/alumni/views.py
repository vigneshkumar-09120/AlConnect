from django.forms import ValidationError
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Alumni,Job,Higherstudies,Category
from admin.models import Event
from student.models import Student
from posts.models import Post
from django.contrib.auth.models import User
from email.message import EmailMessage
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
import csv
from django.core import mail
import pandas as pd
from django.http import HttpResponse
from .models import Alumni, Category, Job, Higherstudies
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
#from .models import Event

from .forms import AlumniCreationForm, AlumniUploadForm,Catform,Jobform,Highform

from django.views.generic import ListView
from django.views.generic.base import TemplateView,View
from django.views.generic.edit import CreateView, FormView, DeleteView,UpdateView
from django.db.models import Q
from .handlers import handle_alumni_csv
from .parsers import parse_query
from django.contrib import messages
def response(request):
    return HttpResponse('Hello')

class AlumniHomeView(View):

    def get(self,request):
        data=Event.objects.all().order_by('-time_posted')[:2]
        posts=Post.objects.all().order_by('-time_posted')[:2]
        context={'event':data,'posts':posts}
        return render(request,"alumni/home.html",context)
    
    
    



def AlumniListView(request):
    if'q'in request.GET:
        q=request.GET['q']
        #data=Internship.objects.filter(Full_name__icontains=q)
        multiple_q=Q(Q(usn__icontains=q)|Q(name__icontains=q)|Q(branch__icontains=q)|Q(job__company_name__icontains=q)|Q(job__role__icontains=q)|Q(higherstudies__specialization__icontains=q)|Q(higherstudies__degree__icontains=q)|Q(higherstudies__college_name__icontains=q))
        data=Alumni.objects.filter(multiple_q).order_by('-usn')
    else:
        data=Alumni.objects.all().order_by('-usn')    
    context={'alumni':data}
    return render(request,"alumni/list.html",context)





class AlumniSearchView(ListView):
    model = Alumni
    template_name = 'alumni/list.html'
    context_object_name = 'alumni'
    arg = {}

    def get(self, request):
        self.__class__.arg = parse_query(request.GET['query'])
        return super().get(self, request)

    ordering = ['user']

    def get_queryset(self):
        return Alumni.objects.filter(**self.__class__.arg)

class AlumniPostView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    ordering = ['author']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.alumnus_details)

class AlumniCreateView(CreateView):
    model = Alumni
    form_class = AlumniCreationForm
    template_name = 'alumni/new.html'

    def get_success_url(self):
        
        connection = mail.get_connection()

# Manually open the connection
        connection.open()
        data=Alumni.objects.all().order_by('-time')[:1]
        context={'data':data}
        html_template='alumni/email.html'
        html_message = render_to_string(html_template,context )
        semail=Alumni.objects.values_list('email',flat=True).order_by('-time')[:1]
        message1 = EmailMessage('Registered in Alumni Connect ...!!', html_message,'isedepartment93@gmail.com',semail
        )
        message1.content_subtype = 'html' # this is required because there is no plain text email message
       
    
        connection.send_messages([message1])

        connection.close()



        return reverse('list_alumni')

class AlumniUploadView(FormView):
    form_class = AlumniUploadForm
    template_name = 'alumni/upload.html'

    def form_valid(self, form):
        status = handle_alumni_csv(self.request.FILES["file"])
        
        return super().form_valid(form)
    
    def get_success_url(self):
        
        connection = mail.get_connection()

        connection.open()
        data=Alumni.objects.all().order_by('-time')[:1]
        context={'data':data}
        html_template='alumni/email.html'
        html_message = render_to_string(html_template,context )
        semail=Alumni.objects.values_list('email',flat=True).order_by('-time')[:8]
        message1 = EmailMessage('Registered in Alumni Connect ...!!', html_message,'isedepartment93@gmail.com',semail
        )
        message1.content_subtype = 'html' # this is required because there is no plain text email message
       
    
        connection.send_messages([message1])

        connection.close()

        return reverse('list_alumni')

class AlumniDeleteView(DeleteView):
    model = User

    def get_success_url(self):
        return reverse('list_alumni')
    
class AlumniUpdateView(UpdateView):
    model=Alumni
    form_class = AlumniCreationForm
    template_name = 'alumni/update.html'


    def get_success_url(self):
        return reverse('list_alumni')

def CategoryView(request):
    if request.method == 'POST':
        form1=Catform(request.POST)
        form2=Jobform(request.POST)
        if form1.is_valid():
            instance=form1.save(commit=False)
            instance.alumnus=Alumni.objects.get(user = request.user)
            instance.save()
            messages.success(request,'added Succesfuly.')
        if form2.is_valid():
            instanc=form2.save(commit=False)
            instanc.alumnus=Alumni.objects.get(user = request.user)
            instanc.save()
            messages.success(request,'added Succesfuly.')

    else:        
        form1=Catform()
        form2=Jobform()

    return render(request,'alumni/job.html',{'form1':form1,'form2':form2}) 

def HigherView(request):
    if request.method == 'POST':
        form=Highform(request.POST)
        
        if form.is_valid():
            instance=form.save(commit=False)
            instance.alumnus=Alumni.objects.get(user = request.user)
            instance.save()
            messages.success(request,'added Succesfuly.')
       

    else:        
        form=Highform()
        

    return render(request,'alumni/higher.html',{'form':form}) 

def Profile(request):
    data=Alumni.objects.get(user=request.user)
    return render(request,'alumni/profile.html',{'data':data})    

def update(request):
    if request.method=='POST':
      Al=Alumni.objects.get(user=request.user)
      try:
          Place=Job.objects.get(alumnus=Al)
          form2=Jobform(request.POST,instance=Place)   
          if form2.is_valid():
            instance=form2.save(commit=False)
            instance.alumnus=Alumni.objects.get(user = request.user)
            instance.save()
      except:
        form2=Jobform()

        return render(request,'alumni/job.html',{'form2':form2})
             

        
      return redirect('/alumni/profile')
    else:
        Al=Alumni.objects.get(user=request.user)
        Place=Job.objects.get(alumnus=Al)
        form2=Jobform(instance=Place)
        return render(request, "alumni/job.html",{'form2':form2})

def update2(request):
    Al =  Alumni.objects.get(user=request.user)
    if request.method=='POST':
        try:
            H=Higherstudies.objects.get(alumnus=Al)
            form=Highform(request.POST,instance=H)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
        except:
            form=Highform(request.POST)
        
            if form.is_valid():
                instance=form.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
    else:
        try:
           
            H=Higherstudies.objects.get(alumnus=Al)
            form=Highform(instance=H)
            return render(request, "alumni/higher.html",{'form':form})
        except:
            form=Highform()
            return render(request, "alumni/higher.html",{'form':form})

def update(request):
    Al =  Alumni.objects.get(user=request.user)
    if request.method=='POST':
        try:
            H=Job.objects.get(alumnus=Al)
            form2=Jobform(request.POST,instance=H)
            if form2.is_valid():
                instance=form2.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
        except:
            form2=Jobform(request.POST)
        
            if form2.is_valid():
                instance=form2.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
    else:
        try:
           
            H=Job.objects.get(alumnus=Al)
            form2=Jobform(instance=H)
            return render(request, "alumni/job.html",{'form2':form2})
        except:
            form2=Jobform()
            return render(request, "alumni/job.html",{'form2':form2})            


def update3(request):
    Al =  Alumni.objects.get(user=request.user)
    if request.method=='POST':
        try:
            H=Category.objects.get(alumnus=Al)
            form=Catform(request.POST,instance=H)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
        except:
            form=Catform(request.POST)
        
            if form.is_valid():
                instance=form.save(commit=False)
                instance.alumnus=Alumni.objects.get(user = request.user)
                instance.save()
                return redirect('/alumni/profile')
    else:
        try:
           
            H=Category.objects.get(alumnus=Al)
            form=Catform(instance=H)
            return render(request, "alumni/current_status.html",{'form':form})
        except:
            form=Catform()
            return render(request, "alumni/current_status.html",{'form':form})

           
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumni_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['USN', 'Name', 'Phone', 'Email', 'RV Email', 'Branch', 'Year Joined', 'Year Passed', 'Category', 'Description', 'Company Name', 'Role', 'Salary', 'Location', 'College Name', 'Specialization', 'Degree', 'Location', 'Year of Grad'])

    alumni_data = Alumni.objects.all()

    for alumni in alumni_data:
        
        category = alumni.category.Category if hasattr(alumni, 'category') and alumni.category else None
        description = alumni.category.description if hasattr(alumni, 'category') and alumni.category else None
        job = alumni.job if hasattr(alumni, 'job') and alumni.job else None
        higherstudies = alumni.higherstudies if hasattr(alumni, 'higherstudies') and alumni.higherstudies else None


        writer.writerow([
            alumni.usn,
            alumni.name,
            alumni.phone,
            alumni.email,
            alumni.rv_email,
            alumni.branch,
            alumni.year_joined,
            alumni.year_passed,
            category,
            description,
            job.company_name if job else None,
            job.role if job else None,
            job.salary if job else None,
            job.location if job else None,
            higherstudies.college_name if higherstudies else None,
            higherstudies.specialization if higherstudies else None,
            higherstudies.degree if higherstudies else None,
            higherstudies.location if higherstudies else None,
            higherstudies.yearofgrad if higherstudies else None,
        ])

    return response

def increment_interested(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.interested += 1
    event.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    





    


    