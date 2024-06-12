import numpy as np
import xmlrpc.client
import pandas as pd
from dotenv import load_dotenv
import numpy as np
import os
load_dotenv()  # take environment variables from .env.

url =  os.environ.get("URL")
db = os.environ.get("DB_ODOO")
username = os.environ.get("ODOO_USER")
password = os.environ.get("ODOO_PASS")

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

