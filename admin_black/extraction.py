import numpy as np
import xmlrpc.client
import pandas as pd
from dotenv import load_dotenv
import numpy as np
import os
load_dotenv()

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

def extract_invoices(url, db, username, password):
    uid, models, common = connect(url, db, username, password)
    factures = models.execute_kw(
        db, uid, password, 'account.move', 'search_read', 
        [[['state', '=', 'posted']], ['id', 'name', 'date', 'amount_total', 'partner_id', 'invoice_line_ids', 'user_id']]
    )

    invoices_data = []
    invoice_lines_data = []

    for invoice in factures:
        # Access invoice line IDs
        invoice_line_ids = invoice['invoice_line_ids']
        # Extract details for each invoice line ID
        for line_id in invoice_line_ids:
            line_data = models.execute_kw(
                db, uid, password, 'account.move.line', 'search_read', 
                [[['id', '=', line_id]], ['name', 'price_unit', 'quantity', 'product_id', 'account_id']]
            )
            # Append line data to a list
            invoice_lines_data.append(line_data[0])
        
        # Extract user_id information
        user_id = invoice['user_id'][0] if invoice['user_id'] else None
        user_name = invoice['user_id'][1] if invoice['user_id'] else 'MISSING_USER'

        invoice_data = {
            'id_invoice': invoice['id'],
            'name': invoice['name'],
            'date': invoice['date'],
            'amount_total': invoice['amount_total'],
            'partner_id': invoice['partner_id'],
            'invoice_line_ids': invoice_lines_data,
            'employee_id': user_id,
            'employee_name': user_name,
        }
        invoices_data.append(invoice_data)
        invoice_lines_data = []

    # Convert invoice data list to pandas DataFrame
    invoices_df = pd.DataFrame(invoices_data)

    # Data processing:
    def convert_partner_id(x: pd.Series) -> pd.Series:
        partner_id = str(x['partner_id'])
        if partner_id[0] == '[' and partner_id[-1] == ']':
            partner_id = partner_id[1:-1]
        elif partner_id == '(' and partner_id[-1] == ')':
            partner_id = partner_id[1:-1]
        partner_id = partner_id.split(',')
        return partner_id

    invoices_df['partner_id'] = invoices_df.apply(convert_partner_id, axis=1)
    invoices_df['partner_name'] = invoices_df['partner_id'].apply(lambda x: x[1] if x[0] != 'False' else None)
    invoices_df['partner_id'] = invoices_df['partner_id'].apply(lambda x: x[0] if x[0] != 'False' else None)
    invoices_df['date'] = pd.to_datetime(invoices_df['date'], format='%Y-%m-%d')
    invoices_df['partner_name'] = invoices_df['partner_name'].fillna('MISSING_NAME')
    invoices_df['partner_id'] = invoices_df['partner_id'].replace(np.nan, '00', regex=True)

    return invoices_df
invoices_df = extract_invoices(url,db,username,password)


def extract_product_details(db, uid, password):

  factures = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[['state', '=', 'posted']], ['id', 'name', 'date', 'amount_total', 'partner_id', 'invoice_line_ids']])

  invoices_data = []
  product_details = []

  for invoice in factures:
      invoice_line_ids = invoice['invoice_line_ids']

      for line_id in invoice_line_ids:
                  line_data = models.execute_kw(db, uid, password, 'account.move.line', 'search_read',
                   [[['id', '=', line_id]], ['name', 'price_unit', 'quantity', 'product_id', 'account_id']])
                  product_id = line_data[0]['product_id']
                  if product_id:  # Check if product_id is not false or empty
                      # Extract only the first number from the list (assuming list structure)
                      product_id = product_id[0]

                      product_details.append({
                          'invoice_id': invoice['id'],
                          'invoice_name': invoice['name'],
                          'product_name': line_data[0]['name'],
                          'price_unit': line_data[0]['price_unit'],
                          'quantity': line_data[0]['quantity'],
                          'product_id': product_id,
                          # Add other relevant details from invoice or line data here
                      })



  # Create DataFrame containing all product details
  product_details_df = pd.DataFrame(product_details)

  return product_details_df


product_details_df = extract_product_details(db, uid, password)

product_details_df
product_details_df_copy = product_details_df.copy()
invoices_df_copy = invoices_df.copy()
product_details_df_copy.rename(columns={'invoice_id': 'id_invoice'}, inplace=True)
joined_df = pd.merge(product_details_df_copy, invoices_df_copy, on='id_invoice', how='inner')
joined_df = joined_df.drop(['name', 'invoice_line_ids'], axis=1)


def extract_products(db, username, password, url):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Search for all product templates
    product_templates = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]], )

    # Extract product details
    products_data = []
    for product in product_templates:
        product_data = {
            'id_product': product['id'],
            'name': product['name'],
            'list_price': product['list_price'],
            'standard_price': product['standard_price'],
            'uom_id': product['uom_id'][1],
            'categ_id': product['categ_id'][1],
        }
        products_data.append(product_data)

    # Convert data to DataFrame
    products_df = pd.DataFrame(products_data)
    products_df['quantity_sold'] = joined_df.groupby('product_id')['quantity'].sum()
    products_df.fillna(0, inplace=True)
    return products_df

products_df = extract_products(db, username, password, url)
def extract_employee_data(url, db, username, password):
    uid,models,common = connect(url,db,username,password)
    model = 'hr.employee'
    fields = ['id', 'name', 'work_email', 'job_id', 'job_title', 'department_id']
    employees = models.execute_kw(
        db, uid, password,
        model, 'search_read',
        [[]],  
        {'fields': fields}
    )
    processed_data = []
    for employee in employees:
        employee['job_id'] = employee['job_id'][0]
        employee['department_id'], employee['department_name'] = employee['department_id']
        processed_data.append(employee)   
    df = pd.DataFrame(processed_data)
    
    return df
employee_data = extract_employee_data(url, db, username, password)
def extract_CRM_data(url, dbname, username, password):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(dbname, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    def extract_model_data(model_name, important_fields=None):
        fields = models.execute_kw(dbname, uid, password, model_name, 'fields_get', [[]])
        if important_fields is None:
            important_fields = list(fields.keys())
        records = models.execute_kw(dbname, uid, password, model_name, 'search_read', [[], important_fields])
        return pd.DataFrame(records)

    CRM_tag = extract_model_data("crm.tag")
    CRM_Stage = extract_model_data("crm.stage")
    CRM_Team = extract_model_data("crm.team")
    CRM_lead = extract_model_data("crm.lead", important_fields=['id', 'campaign_id', 'source_id', 'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_date_deadline', 'message_is_follower', 'message_follower_ids', 'message_partner_ids', 'message_ids', 'has_message'])

    # List of important columns to retain in CRM_Team
    important_columns = [
    "id", "name", "sequence", "active", "company_id",
    "message_is_follower", "message_follower_ids", "message_partner_ids",
    "message_ids", "has_message", "message_unread", "message_unread_counter",
    "message_needaction", "message_needaction_counter", "message_has_error",
    "message_has_error_counter", "message_attachment_count",
    "message_main_attachment_id", "website_message_ids", "message_has_sms_error"
          ]
    CRM_Team = CRM_Team[important_columns]
    return CRM_tag, CRM_Stage, CRM_Team, CRM_lead

CRM_tag, CRM_Stage, CRM_Team, CRM_lead = extract_CRM_data(url, db, username, password)




with pd.ExcelWriter('data.xlsx') as writer:
    invoices_df.to_excel(writer, sheet_name='invoices_df')
    product_details_df.to_excel(writer, sheet_name='product_details_df')
    joined_df.to_excel(writer, sheet_name='joined_df')
    products_df.to_excel(writer, sheet_name='products_df')
    CRM_tag.to_excel(writer, sheet_name='CRM_tag')
    CRM_Stage.to_excel(writer, sheet_name='CRM_Stage')
    CRM_Team.to_excel(writer, sheet_name='CRM_Team')
    CRM_lead.to_excel(writer, sheet_name='CRM_lead')
    employee_data.to_excel(writer, sheet_name='employee_data')

def extract_types_orders():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    quotes_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('state', '=', 'draft')]})

    # all sent devis
    quotes_id = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('state', '=', 'ent')]})

    #  all sale orders
    sale_orders_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('state', '=', 'ale')]})

    #  all done sale orders
    done_sale_orders_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('state', '=', 'done')]})

    #  all cancelled sale orders
    cancelled_sale_orders_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('state', '=', 'cancel')]})

    #  all sale orders with an invoice
    invoiced_sale_orders_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('invoice_status', '=', 'invoiced')]})


    #  all sale orders that need to be invoiced
    to_invoice_sale_orders_ids = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [],
      {'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'domain': [('invoice_status', '=', 'to invoice')]})
    quotes_ids = pd.DataFrame(quotes_ids)
    quotes_id = pd.DataFrame(quotes_id)
    sale_orders_ids = pd.DataFrame(sale_orders_ids)
    done_sale_orders_ids= pd.DataFrame(done_sale_orders_ids)
    cancelled_sale_orders_ids = pd.DataFrame(cancelled_sale_orders_ids)
    invoiced_sale_orders_ids= pd.DataFrame(invoiced_sale_orders_ids)
    to_invoice_sale_orders_ids= pd.DataFrame(to_invoice_sale_orders_ids)
    return quotes_ids,quotes_id,sale_orders_ids,done_sale_orders_ids,cancelled_sale_orders_ids,invoiced_sale_orders_ids,to_invoice_sale_orders_ids

quotes_ids,quotes_id,sale_orders_ids,done_sale_orders_ids,cancelled_sale_orders_ids,invoiced_sale_orders_ids,to_invoice_sale_orders_ids=extract_types_orders()
quotes_ids,quotes_id,sale_orders_ids,done_sale_orders_ids,cancelled_sale_orders_ids,invoiced_sale_orders_ids,to_invoice_sale_orders_ids=extract_types_orders()

with pd.ExcelWriter('orders.xlsx') as writer:
    quotes_ids.to_excel(writer, sheet_name='quotes_ids')
    quotes_id.to_excel(writer, sheet_name='quotes_id')
    sale_orders_ids.to_excel(writer, sheet_name='sale_orders_ids')
    done_sale_orders_ids.to_excel(writer, sheet_name='done_sale_orders_ids')
    cancelled_sale_orders_ids.to_excel(writer, sheet_name='cancelled_sale_orders_ids')
    invoiced_sale_orders_ids.to_excel(writer, sheet_name='invoiced_sale_orders_ids')
    to_invoice_sale_orders_ids.to_excel(writer, sheet_name='to_invoice_sale_orders_ids')

