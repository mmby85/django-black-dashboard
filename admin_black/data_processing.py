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

employee_sales1 = ventes_par_client(invoices_df)

facture_par_mois = nombre_factures("month")
facture_par_semestre =nombre_factures("quarter")
facture_par_annee = nombre_factures("year")
