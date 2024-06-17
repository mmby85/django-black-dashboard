from django.shortcuts import render, redirect
from admin_black.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm, InvoiceForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Invoice

from .data_processing import custmers, custmers_count, CA, CAP, CAPMOIS , employee_sales , nombreFactures , nombreClient , chiffreaffaire ,revenu_produit 
from .data_processing import *
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
    xx = revenu_produit.product_name.to_list()[:2]
    xx[0] = xx[0][:10]
    xx[1] = xx[1][:10]
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
    "chiffre_affaire" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "chiffreAffaire" , "type" : "pie" },
    "client" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "clientNber" , "type" : "pie" },
    "chiffreaffaire" : chiffreaffaire.round(4) ,
    "nombreClient" : nombreClient ,
    "nombreFactures": nombreFactures,
    "employee_sales" : {"data" : employee_sales.total_revenue.tolist() , "labels" : employee_sales.index.to_list(), "id" : "Employee_sales" , "type" : "bar" },
    "ca_par_produit" : {"data" : CA_par_produit.total_quantity.to_list() , "labels" : CA_par_produit.index.to_list(), "id" : "CA_par_produit" , "type" : "bar" },

    "revenu_produit" : {"data" : revenu_produit.total_revenue.tolist() , "labels" : revenu_produit.product_name.to_list(), "id" : "revenu_produit" , "type" : "pie" },

 
  }
    return render(request, 'pages/dashboard.html', context)

def main(request):
    context = {
    'parent': 'pages',
    'segment': 'dashboard',
  }
    return render(request, 'pages/dashboard.html', context)

# @login_required(login_url='/accounts/auth-signin')
def factures(request):
    context = {
    'parent': 'pages',
    'segment': 'factures',
    }
    return render(request, 'pages/factures.html', context)

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
def clients(request):
    context = {
    'parent': 'pages',
    'segment': 'clients'
  }
    return render(request, 'pages/clients.html', context)

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
