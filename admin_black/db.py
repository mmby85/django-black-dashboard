import xmlrpc.client
import os 
from dotenv import load_dotenv
import pandas as pd

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