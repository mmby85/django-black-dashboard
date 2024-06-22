import pandas as pd

def dataimporting():
  invoices_df = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='invoices_df')
  product_details_df = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='product_details_df')
  joined_df = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='joined_df')
  products_df = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='products_df')
  CRM_tag = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='CRM_tag')
  CRM_Stage = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='CRM_Stage')
  CRM_Team = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='CRM_Team')
  CRM_lead = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='CRM_lead')
  employee_data = pd.read_excel(open('admin_black\\data.xlsx', 'rb'),sheet_name='employee_data')

  return invoices_df , product_details_df ,joined_df, products_df , CRM_tag, CRM_Stage, CRM_Team, CRM_lead , employee_data

invoices_df , product_details_df ,joined_df, products_df , CRM_tag, CRM_Stage, CRM_Team, CRM_lead , employee_data = dataimporting()