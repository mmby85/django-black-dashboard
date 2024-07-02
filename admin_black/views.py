from django.shortcuts import render, redirect
from admin_black.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm, InvoiceForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Invoice
from .data_processing import *
from .data_processing import CA_mois , CA_quarter , CA_year
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
    'facturess' : facturess[:4],
    'test' : 
    [{ "Name" : "Dakota Rice", "Country" : "Niger","City" : "Oud-Turnhout","SALARY": "36,738" } , 
    { "Name" : "Dakota Rice", "Country" : "Tunisia","City" : "Oud-Turnhout","SALARY": "36,738" } , 
    { "Name" : "Dakota Rice", "Country" : "France","City" : "Oud-Turnhout","SALARY": "36,738" }],
    'labels' : [ name['name'] for name in facturess[:5] ],
    # "chiffre_affaire" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "chiffreAffaire" , "type" : "pie" },
    # "client" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "clientNber" , "type" : "pie" },
    "chiffreaffaire" : chiffreaffaire.round(4) ,
    "nombreClient" : nombreClient ,
    "nombreFactures": nombreFactures,

    "ca_mois" : {"data" : CA_mois.tolist() , "labels" : CA_mois.index.to_list(), "id" : "ca_mois" , "type" : "line"},
    "ca_year" : {"data" : CA_year.tolist() , "labels" : CA_year.index.to_list()},
    "ca_quarter" : {"data" : CA_quarter.tolist() , "labels" : CA_quarter.index.to_list()},

    "employee_sales" : {"data" : employee_sales.total_revenue.tolist() , "labels" : employee_sales.index.to_list(), "id" : "employee_sales" , "type" : "bar" },
    "ca_par_produit" : {"data" : CA_par_produit.total_quantity.to_list() , 
                        "labels" :  CA_par_produit.index.to_list(),  "id" : "CA_par_produit" , "type" : "bar" }, 
    "revenu_produit" : {"data" : revenu_produit.total_revenue.tolist() , "labels" : revenu_produit.product_name.to_list(), "id" : "revenu_produit" , "type" : "pie" },
    "crm_statut" : {"data" : CRM_statut.values.tolist() , "labels" : CRM_statut.index.tolist(), "id" : "crm_statut" , "type" : "pie"},
    "ca_par_employee" : {"data" :CA_par_employee.total_sales.tolist()  , "labels" : CA_par_employee.employee_name.tolist(), "id" : "ca_par_employee" , "type" : "bar"},
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
    'facturess' : facturess[:4],
    'labels' : [ name['name'] for name in facturess[:5] ],
    # "chiffre_affaire" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "chiffreAffaire" , "type" : "pie" },
    # "client" : {"data" : CAPMOIS.tolist() , "labels" : CAPMOIS.index.tolist(), "id" : "clientNber" , "type" : "pie" },
    "chiffreaffaire" : chiffreaffaire.round(4),
    "nombreClient" : nombreClient ,
    "nombreFactures": nombreFactures,
    "employee_sales" : {"data" : employee_sales.total_revenue.tolist() , "labels" : employee_sales.index.to_list(), "id" : "employee_sales" , "type" : "bar" },
    "ca_par_produit" : {"data" : CA_par_produit.total_quantity.to_list() , 
                        "labels" :  CA_par_produit.index.to_list(),  "id" : "CA_par_produit" , "type" : "bar" }, 
    "revenu_produit" : {"data" : revenu_produit.total_revenue.tolist() , "labels" : revenu_produit.product_name.to_list(), "id" : "revenu_produit" , "type" : "pie" },
    "crm_statut" : {"data" : CRM_statut.values.tolist() , "labels" : CRM_statut.index.tolist(), "id" : "crm_statut" , "type" : "pie"},
    "ca_par_employee" : {"data" :CA_par_employee.total_sales.tolist()  , "labels" : CA_par_employee.employee_name.tolist(), "id" : "ca_par_employee" , "type" : "bar"},
    "ca_mois" : {"data" : CA_mois.tolist() , "labels" : CA_mois.index.to_list(), "id" : "ca_mois" , "type" : "line"},
    "ca_year" : {"data" : CA_year.tolist() , "labels" : CA_year.index.to_list()},
    "ca_quarter" : {"data" : CA_quarter.tolist() , "labels" : CA_quarter.index.to_list()},
# --------------------------------------------------------     
    'alldevis': alldevis,
    'sent_devis': sent_devis,
    'sale_orders': sale_orders,
    'done_saleorders': done_saleorders,
    'cancelled_sale_orders': cancelled_sale_orders,
    'sale_orders_with_invoice': sale_orders_with_invoice,
    'sale_orders_to_invoiced': sale_orders_to_invoiced,

    "facture_mois" : {"data" : facture_par_mois.number_of_invoices.tolist() , "labels" : facture_par_mois.date.tolist(), "id" : "nb_factures" , "type" : "bar"},
    "facture_annee" : {"data" : facture_par_annee.number_of_invoices.tolist() , "labels" : facture_par_annee.date.tolist()},
    "facture_semestre" : {"data" : facture_par_semestre.number_of_invoices.tolist() , "labels" : facture_par_semestre.date.tolist()},
    "ca_client" : {"data" : CA_client.total_revenue.tolist() , "labels" : CA_client.index.to_list(), "id" : "ca_client" , "type" : "bar"},
    "client_saless" : {"data" : client_sales.sales.tolist() , "labels" : client_sales.date.to_list(), "id" : "client_saless" , "type" : "bar"},
    "NB_fac_par_client" : {"data" : nb_fac_par_client.values.tolist() , "labels" : client_sales.index.to_list(), "id" : "NB_fac_par_client" , "type" : "bar"},
    #"TOP_revenue_par_client" : {"data" : top_revenue_par_client.values.tolist() , "labels" : top_revenue_par_client.index.to_list(), "id" : "TOP_revenue_par_client" , "type" : "bar"},
    "MOINS_revenue_par_client" : {"data" : moins_revenue_par_client.values.tolist() , "labels" : moins_revenue_par_client.index.to_list(), "id" : "MOINS_revenue_par_client" , "type" : "bar"},
    "retention_MOIS" : {"data" : retention_mois.values.tolist() , "labels" : retention_mois.index.to_list(), "id" : "retention_MOIS" , "type" : "line"},
    "retention_ANNEE" : {"data" : retention_annee.values.tolist() , "labels" : retention_annee.index.to_list()},
    "retention_SEMESTRE" : {"data" : retention_semstre.values.tolist() , "labels" : retention_semstre.index.to_list()},
    'rt_mois': rt_mois,
    'rt_semestre': rt_semestre,
    'alldevis': rt_annee,    
    "ca_par_produit1" : {"data" : CA_par_produit1.total_quantity.to_list() , 
                        "labels" :  CA_par_produit1.index.to_list(),  "id" : "CA_par_produit1" , "type" : "bar" }, 
    "revenu_produit1" : {"data" : revenu_produit1.total_revenue.tolist() , "labels" : revenu_produit1.product_name.to_list(), "id" : "revenu_produit1" , "type" : "pie" },
    "to_draw" : [
      {"data" : top_revenue_par_client.values.tolist() , "labels" : top_revenue_par_client.index.to_list(), "id" : "TOP_revenue_par_client" , "type" : "bar"},
    ]
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