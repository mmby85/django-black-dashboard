from .KPIs import *
from .importing import *

facturess = factures(invoices_df)
CAPMOIS = total_sales_by_period(invoices_df, "month")


chiffreaffaire = Chiffreaffaire(invoices_df)
nombreClient = NombreClient(invoices_df)
nombreFactures = NombreFactures(invoices_df)
employee_sales = ventes_par_client(invoices_df)

CA_mois = visualize_total_sales_months(invoices_df)
CA_year = visualize_total_sales_year(invoices_df)
CA_quarter = visualize_total_sales_quarter(invoices_df)


CA_quarter = visualize_total_sales_quarter(invoices_df)
CA_year = visualize_total_sales_year(invoices_df)

CA_par_produit = top_products_sold(product_details_df)
revenu_produit = Revenu_par_produit(product_details_df)

CRM_statut = CRM_statut(CRM_Stage)
CA_par_employee = sales_per_employee(invoices_df)

#------------------------------------------------------------------------------
#-------------------KPIs Page FACTURES-----------------------------------------

alldevis = len(quotes_ids)
sent_devis = len(quotes_id)
sale_orders = len(sale_orders_ids)
done_saleorders = len(done_sale_orders_ids)
cancelled_sale_orders = len(cancelled_sale_orders_ids)
sale_orders_with_invoice = len(invoiced_sale_orders_ids)
sale_orders_to_invoiced = len(to_invoice_sale_orders_ids)


facture_par_mois = nombre_factures("month")
facture_par_semestre =nombre_factures("quarter")
facture_par_annee = nombre_factures("year")
CA_client = ventes_par_clients(invoices_df)
client_name = 'Client X' # must be givin as an input 
client_sales = client_sales_details(client_name, start_date=None, end_date=None, period="month")
# nombre de transaction par clients :
nb_fac_par_client = invoices_df.groupby('partner_name').size()
#Top 10 Clients générant le moins revenue :
partner_sales = ventes_par_clients(invoices_df)
top_revenue_par_client= partner_sales.sort_values(by="total_revenue", ascending=False).head(10)
#Top 10 Clients générant le plus revenue :
moins_revenue_par_client = partner_sales.sort_values(by="total_revenue" , ascending=True).head(10)
# retention rate detailed : 
retention_mois = retention_rate_over_time(invoices_df, period='month')
retention_semstre = retention_rate_over_time(invoices_df, period='quarter')
retention_annee = retention_rate_over_time(invoices_df, period='year')

rt_mois = calculate_client_retention_rate(invoices_df, period='month')
rt_semestre = calculate_client_retention_rate(invoices_df, period ='quarter')
rt_annee = calculate_client_retention_rate(invoices_df, period ='year')


#-------------------KPIs Page PRODUCTS (formations ) -----------------------------------------
CA_par_produit1 = top_products_sold(product_details_df)
revenu_produit1 = Revenu_par_produit(product_details_df)