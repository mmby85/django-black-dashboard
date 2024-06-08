from django.shortcuts import render, redirect
from admin_black.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm, InvoiceForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Invoice

from .data_processing import custmers, custmers_count, CA, CAP

def auth_signup(request):
  if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
        form.save()
        print('Account created successfully!')
        return redirect('/accounts/auth-signin/')
      else:
        print("Registration failed!")
  else:
    form = RegistrationForm()
  context = {'form': form}
  return render(request, 'accounts/auth-signup.html', context)

class AuthSignin(auth_views.LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm
  success_url = '/'

class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/recover-password.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/recover-password.html'
  form_class = UserSetPasswordForm

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/auth-signin/')

# Pages -- Dashboard
def dashboard(request):
    context = {
    'parent': 'pages',
    'segment': 'dashboard',
    'odoo' : 'DASHBOARD GROUPAXION',
    'contacts' : custmers[:4],
    'test' : 
    [{ "Name" : "Dakota Rice", "Country" : "Niger","City" : "Oud-Turnhout","SALARY": "36,738" } , 
    { "Name" : "Dakota Rice", "Country" : "Tunisia","City" : "Oud-Turnhout","SALARY": "36,738" } , 
    { "Name" : "Dakota Rice", "Country" : "France","City" : "Oud-Turnhout","SALARY": "36,738" }],
    'labels' : [ name['name'] for name in custmers[:5] ],
    'customers_count' : "{:,}".format(custmers_count).replace(',' , ' '),
    "CAP" : "{:,}".format(CAP.round(4)).replace(',' , ' '),
    "CA" : "{:,}".format(CA.round(4)).replace(',' , ' '),

  }
    return render(request, 'pages/dashboard.html', context)

def main(request):
    context = {
    'parent': 'pages',
    'segment': 'dashboard',
  }
    return render(request, 'pages/dashboard.html', context)

# @login_required(login_url='/accounts/auth-signin')
def icons(request):
    context = {
    'parent': 'pages',
    'segment': 'icons'
  }
    return render(request, 'pages/icons.html', context)

# @login_required(login_url='/accounts/auth-signin')
def map(request):
    context = {
    'parent': 'pages',
    'segment': 'map'
  }
    return render(request, 'pages/map.html', context)

# @login_required(login_url='/accounts/auth-signin')
def notifications(request):
    context = {
    'parent': 'pages',
    'segment': 'notifications'
  }
    return render(request, 'pages/notifications.html', context)

# @login_required(login_url='/accounts/auth-signin')
def user_profile(request):
    context = {
    'parent': 'pages',
    'segment': 'user_profile'
  }
    return render(request, 'pages/user.html', context)

# @login_required(login_url='/accounts/auth-signin')
def tables(request):
    context = {
    'parent': 'pages',
    'segment': 'tables'
  }
    return render(request, 'pages/tables.html', context)

# @login_required(login_url='/accounts/auth-signin')
def typography(request):
    context = {
    'parent': 'pages',
    'segment': 'typography'
  }
    return render(request, 'pages/typography.html', context)

# @login_required(login_url='/accounts/auth-signin')
def rtl(request):
    context = {
    'parent': 'pages',
    'segment': 'rtl'
  }
    return render(request, 'pages/rtl.html', context)
  
# @login_required(login_url='/accounts/auth-signin')
def upgrade(request):
    context = {
    'parent': 'pages',
    'segment': 'upgrade'
  }
    return render(request, 'pages/upgrade.html', context)


def all_invoices(request):
  if request.method == "GET" :
     print(request.GET)

  form = InvoiceForm()
  invoices= Invoice.objects.all()
  print(invoices[0].customer.first_name)
  return render(request, 'get_invoices.html', context={'invoices' : invoices, 'form': form})
