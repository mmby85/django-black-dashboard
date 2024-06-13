import xmlrpc.client
import os 
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from .extraction import *
load_dotenv() 

url =  os.environ.get("URL")
db = os.environ.get("DB_ODOO")
username = os.environ.get("ODOO_USER")
password = os.environ.get("ODOO_PASS")

# chiffre d'affaire globale : 
def Chiffreaffaire(invoices_df):
    return invoices_df['amount_total'].sum()
# nombre de client : 
def NombreClient(invoices_df):
    return invoices_df['partner_id'].nunique()    

# nombre de factures :
def NombreFactures(invoices_df):
    return len(invoices_df)

def visualize_total_sales_months(df):

  unique_months = df["date"].dt.month.unique()
  sales_by_month = pd.DataFrame({
      "month": range(1, 13),
      "total_sales": 0
  })
  for month in unique_months:
    sales_by_month.loc[month - 1, "total_sales"] = df[df["date"].dt.month == month]["amount_total"].sum()
  x = sales_by_month["total_sales"]
  return x
def visualize_total_sales_quarter(df):

  unique_quarter = df["date"].dt.quarter.unique()
  sales_by_quarter = pd.DataFrame({
      "month": range(1, 5),
      "total_sales": 0
  })
  for quarter in unique_quarter:
    sales_by_quarter.loc[quarter - 1, "total_sales"] = df[df["date"].dt.quarter == quarter]["amount_total"].sum()
  x = sales_by_quarter["total_sales"]
  return x
def visualize_total_sales_year(df):

  unique_year = df["date"].dt.year.unique()
  sales_by_year = pd.DataFrame({
      "month": range(1, len(unique_year)+1),
      "total_sales": 0
  })
  for year in unique_year:
    sales_by_year.loc[year - 2019, "total_sales"] = df[df["date"].dt.year == year]["amount_total"].sum()
  sales_by_year.set_index("month", inplace=True)
  x = sales_by_year["total_sales"]
  return x
visualize_total_sales_year(invoices_df)

def ventes_par_client(invoices_df):
  employee_sales = invoices_df.groupby('partner_name').agg(total_revenue=('amount_total', 'sum')).reset_index()
  employee_sales = employee_sales.sort_values(by='total_revenue', ascending=False).set_index('partner_name')
  return employee_sales
