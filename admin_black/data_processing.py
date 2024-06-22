from .KPIs import *
from .importing import invoices_df , product_details_df ,joined_df, products_df , CRM_tag, CRM_Stage, CRM_Team, CRM_lead , employee_data
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