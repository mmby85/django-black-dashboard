import xmlrpc.client
import os 
from dotenv import load_dotenv
import pandas as pd
import numpy as np 

load_dotenv()  # take environment variables from .env.

url =  os.environ.get("URL")
db = os.environ.get("DB_ODOO")
username = os.environ.get("ODOO_USER")
password = os.environ.get("ODOO_PASS")

def odoo_auth(db=db, username=username, password=password):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if uid :
        return uid, common
    else:
        return "authentication failed"

def get_costumers(fields={'fields': ['id', 'name','phone','email']}):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
    record = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids] ,  fields)
    return record

def research(model):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    data = models.execute_kw(db, uid, password, model, 'search_read', [[]] )
    return data

def get_invoice_info():
    data = research("account.move")
    return [ { k : v for k, v in data[i].items() if  "invoice" in k } for i in range(len(data)) ]
    # return [ [(k,v) for k, v in data[i].items() if  "invoice" in k ] for i in range(len(data)) ]

def get_filtred_data(model):
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  data = models.execute_kw(db, uid, password, model, 'search_read', [] )
#   filtered_data = {k: v for k, v in data[0].items() if v is not False}
  return data

def count_customers():
    data = get_filtred_data("account.move")
    df = pd.DataFrame(data)
    return len(df[df['state'] == 'posted']['partner_id'].map(lambda s : s[1] if s else "-").unique())

def get_CA():
    data = get_filtred_data("account.move")
    df = pd.DataFrame(data)
    return df['amount_total'].sum()

def get_CA_Potential():
    data = get_filtred_data("account.move")
    df = pd.DataFrame(data)
    return df[df['payment_state'] == 'paid']['amount_total'].sum()


uid, common = odoo_auth()


data = get_invoice_info()
get_costumers()


#New Code 



def total_sales_by_period(df, period):
    if period == "month":
        return df.groupby(df["date"].dt.month)["amount_total"].sum()
    elif period == "quarter":
        return df.groupby(df["date"].dt.quarter)["amount_total"].sum()
    elif period == "year":
        return df.groupby(df["date"].dt.year)["amount_total"].sum()
    else:
        raise ValueError("Invalid period. Please choose from 'month', 'quarter', or 'year'.")

def connect(url,db,username,password):
  common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  uid = common.authenticate(db, username, password, {})
  return uid,models,common

uid,models,common = connect(url,db,username,password)

def extract_invoices(url,db,username,password):
  uid,models,common = connect(url,db,username,password)
  factures = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[['state', '=', 'posted']], ['id', 'name', 'date', 'amount_total', 'partner_id', 'invoice_line_ids']])

  invoices_data = []
  invoice_lines_data = []

  for invoice in factures:
    # Access invoice line IDs
    invoice_line_ids = invoice['invoice_line_ids']
    # Extract details for each invoice line ID
    for line_id in invoice_line_ids:
        line_data = models.execute_kw(db, uid, password, 'account.move.line', 'search_read', [[['id', '=', line_id]], ['name', 'price_unit', 'quantity', 'product_id', 'account_id']])
        # Append line data to a list
        invoice_lines_data.append(line_data[0])
    invoice_data = {
        'id_invoice': invoice['id'],
        'name': invoice['name'],
        'date': invoice['date'],
        'amount_total': invoice['amount_total'],
        'partner_id': invoice['partner_id'],
        'invoice_line_ids': invoice_lines_data,
    }
    invoices_data.append(invoice_data)
    invoice_lines_data = []

  # Convert invoice data list to pandas DataFrames
  invoices_df = pd.DataFrame(invoices_data)
  # data processing :
  def convert_partner_id(x: pd.Series) -> pd.Series:
    partner_id = str(x['partner_id'])

    if partner_id[0] == ('[') and partner_id[-1] == (']') :
      partner_id = partner_id[1:-1]
    elif partner_id == ('(') and partner_id == (')'):
      partner_id = partner_id[1:-1]

    partner_id = partner_id.split(',')
    return partner_id

  invoices_df['partner_id'] = invoices_df.apply(convert_partner_id, axis=1)

  # invoices_df['partner_name'] = invoices_df['partner_id'].apply(lambda x: x[0])
  invoices_df['partner_name'] = invoices_df['partner_id'].apply(lambda x: x[1] if x[0]!='False' else None)
  invoices_df['partner_id'] = invoices_df['partner_id'].apply(lambda x: x[0] if x[0]!='False' else None)
  invoices_df['date'] = pd.to_datetime(invoices_df['date'], format='%Y-%m-%d')
  invoices_df['partner_name'] = invoices_df['partner_name'].fillna('MISSING_NAME')
  invoices_df['partner_id'] = invoices_df['partner_id'].replace(np.nan, '00', regex=True)

  return invoices_df

invoices_df = extract_invoices(url,db,username,password)