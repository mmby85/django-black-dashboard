import os 
import pandas as pd
import numpy as np
from .importing import *


# ---- a revoir et ne pas toucher pour le moment : 
def factures(invoices_df):
  var = invoices_df[['name', 'date', 'amount_total', 'partner_name']].to_dict('records')
  return var


def total_sales_by_period(df, period):
    if period == "month":
        return df.groupby(df["date"].dt.month)["amount_total"].sum()
    elif period == "quarter":
        return df.groupby(df["date"].dt.quarter)["amount_total"].sum()
    elif period == "year":
        return df.groupby(df["date"].dt.year)["amount_total"].sum()
    else:
        raise ValueError("Invalid period. Please choose from 'month', 'quarter', or 'year'.")




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

''' CA par annee :'''
def visualize_total_sales_year(df):
    unique_years = df["date"].dt.year.unique()
    all_years = range(min(unique_years), max(unique_years) + 1)
    sales_by_year = pd.DataFrame({
        "year": all_years,
        "total_sales": 0
    })
    for year in unique_years:
        sales_by_year.loc[sales_by_year["year"] == year, "total_sales"] = df[df["date"].dt.year == year]["amount_total"].sum()
    x = sales_by_year["total_sales"]
    x.index = sales_by_year["year"]
    return x
# CA par client :
def ventes_par_client(invoices_df):
  employee_sales = invoices_df.groupby('partner_name').agg(total_revenue=('amount_total', 'sum')).reset_index()
  employee_sales = employee_sales.sort_values(by='total_revenue', ascending=False).set_index('partner_name')
  return employee_sales

# CA par produit : 
def top_products_sold(product_details_df):
    product_sales = product_details_df.groupby('product_name').agg(total_quantity=('quantity', 'sum'))
    top_selling_products = product_sales.sort_values(by='total_quantity', ascending=False)
    top_selling_products =top_selling_products
    return top_selling_products

# revenu par produit
def Revenu_par_produit(product_details_df):
    product_details_df['price_unit'] = product_details_df['price_unit'].astype(float)
    product_revenue = product_details_df.groupby('product_name').agg(total_revenue=('price_unit', lambda x: sum(x * product_details_df.loc[x.index, 'quantity']))).reset_index()
    product_revenue = product_revenue.sort_values(by='total_revenue', ascending=False)
    return product_revenue

# Operations statut : 
def CRM_statut(CRM_Stage):
  grouped_df = CRM_Stage.groupby('name')['team_count'].sum()
  return grouped_df

# Vente par employé :
def sales_per_employee(invoices_df):
    performance_df = invoices_df.groupby('employee_name')['amount_total'].sum().reset_index()
    performance_df = performance_df.rename(columns={'amount_total': 'total_sales'})
    performance_df = performance_df.sort_values(by='total_sales', ascending=False).reset_index(drop=True)
    return performance_df

#------------------------------------------------------------------------------
#-------------------KPIs Page FACTURES-----------------------------------------

# nombre de factures par mois , annee , semestre :
def nombre_factures(group_by):
    freq_map = {"month": "M", "quarter": "Q", "year": "A"}
    grouped_df = invoices_df.groupby(pd.Grouper(key="date", freq=freq_map[group_by])).size().reset_index(name="number_of_invoices")
    return grouped_df

# CA par client :
def ventes_par_clients(invoices_df):
  employee_sales = invoices_df.groupby('partner_name').agg(total_revenue=('amount_total', 'sum')).reset_index()
  employee_sales = employee_sales.sort_values(by='total_revenue', ascending=False).set_index('partner_name')
  return employee_sales

# client sales :
def client_sales_details(client_name, start_date=None, end_date=None, period="month"):

    if period not in ["month", "quarter", "year"]:
        raise ValueError("Invalid period. Please choose from 'month', 'quarter', or 'year'.")

    filtered_df = invoices_df.loc[invoices_df["partner_name"] == client_name]
    if start_date is not None:
        filtered_df = filtered_df.loc[filtered_df["date"] >= start_date]
    if end_date is not None:
        filtered_df = filtered_df.loc[filtered_df["date"] <= end_date]

    freq_map = {"month": "M", "quarter": "Q", "year": "A"}
    grouped_df = filtered_df.groupby(pd.Grouper(key="date", freq=freq_map[period])).agg({"amount_total": "sum"})
    grouped_df.columns = ["sales"]
    grouped_df = grouped_df.reset_index()
    return grouped_df
# retation rate for periode 
def calculate_client_retention_rate(invoices_df, period):

    # Ensure the 'date' column is in datetime format
    invoices_df['date'] = pd.to_datetime(invoices_df['date'])

    # Extract the period from the date column
    if period == 'year':
        invoices_df['period'] = invoices_df['date'].dt.year
    elif period == 'quarter':
        invoices_df['period'] = invoices_df['date'].dt.to_period('Q')
    elif period == 'month':
        invoices_df['period'] = invoices_df['date'].dt.to_period('M')
    else:
        raise ValueError("Invalid period. Choose from 'year', 'quarter', or 'month'.")
    period_partner_counts = invoices_df.groupby('period')['partner_id'].nunique()
    repeat_clients = invoices_df.groupby('period')['partner_id'].apply(lambda x: x.duplicated().sum())
    retention_rate = (repeat_clients / period_partner_counts).mean() * 100
    return retention_rate


# retention rate over time:
def retention_rate_over_time(invoices_df, period):
    invoices_df['date'] = pd.to_datetime(invoices_df['date'])

    # Extract the period from the date column
    if period == 'year':
        invoices_df['period'] = invoices_df['date'].dt.year
        all_periods = pd.Series(range(invoices_df['period'].min(), invoices_df['period'].max() + 1)) # Use 'period' here

    elif period == 'quarter':
        invoices_df['period'] = invoices_df['date'].dt.to_period('Q')
        all_periods = pd.period_range(invoices_df['period'].min(), invoices_df['period'].max(), freq='Q')

    elif period == 'month':
        invoices_df['period'] = invoices_df['date'].dt.to_period('M')
        all_periods = pd.period_range(invoices_df['period'].min(), invoices_df['period'].max(), freq='M') 

    else:
        raise ValueError("Invalid period. Choose from 'year', 'quarter', or 'month' ")

    
    # Group by period and partner_id, and count the number of unique partner_ids
    period_partner_counts = invoices_df.groupby('period')['partner_id'].nunique()

    # Calculate the number of repeat clients in each period
    repeat_clients = invoices_df.groupby('period')['partner_id'].apply(lambda x: x.duplicated().sum())

    # Calculate the Client Retention Rate for each period
    retention_rate_series = (repeat_clients / period_partner_counts) * 100

    # Fill missing periods with 0 retention rate
    retention_rate_series = retention_rate_series.reindex(all_periods, fill_value=0)

    return retention_rate_series


