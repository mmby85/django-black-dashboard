import os 
import pandas as pd
import numpy as np
from .importing import invoices_df , product_details_df ,joined_df, products_df


# chiffre d'affaire globale : 
def Chiffreaffaire(invoices_df):
    return invoices_df['amount_total'].sum()
# nombre de client : 
def NombreClient(invoices_df):
    return invoices_df['partner_id'].nunique()    

# nombre de factures :
def NombreFactures(invoices_df):
    return len(invoices_df)


# CA par mois : 

def visualize_total_sales_months(df):
  unique_months = df["date"].dt.month.unique()
  month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  sales_by_month = pd.DataFrame({
      "month": month_names,
      "total_sales": 0
  })
  for month in unique_months:
    sales_by_month.loc[month - 1, "total_sales"] = df[df["date"].dt.month == month]["amount_total"].sum()
  x = sales_by_month["total_sales"]
  x.index = month_names
  return x

# CA par semestre :
def visualize_total_sales_quarter(df):
  unique_quarter = df["date"].dt.quarter.unique()
  sales_by_quarter = pd.DataFrame({
      "month": range(1, 5),
      "total_sales": 0
  })
  for quarter in unique_quarter:
    sales_by_quarter.loc[quarter - 1, "total_sales"] = df[df["date"].dt.quarter == quarter]["amount_total"].sum()
  x = sales_by_quarter["total_sales"]
  x.index = ["Q1", "Q2", "Q3", "Q4"]
  return x

# CA par annee :
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

# CA par client :
def ventes_par_client(invoices_df):
  employee_sales = invoices_df.groupby('partner_name').agg(total_revenue=('amount_total', 'sum')).reset_index()
  employee_sales = employee_sales.sort_values(by='total_revenue', ascending=False).set_index('partner_name')
  return employee_sales

# CA par produit : 
def top_products_sold(product_details_df):
    product_sales = product_details_df.groupby('product_name').agg(total_quantity=('quantity', 'sum'))
    top_selling_products = product_sales.sort_values(by='total_quantity', ascending=False).head(10)
    return top_selling_products

# revenu par produit
def Revenu_par_produit(product_details_df):
    product_details_df['price_unit'] = product_details_df['price_unit'].astype(float)
    product_revenue = product_details_df.groupby('product_name').agg(total_revenue=('price_unit', lambda x: sum(x * product_details_df.loc[x.index, 'quantity']))).reset_index()
    product_revenue = product_revenue.sort_values(by='total_revenue', ascending=False)
    return product_revenue

