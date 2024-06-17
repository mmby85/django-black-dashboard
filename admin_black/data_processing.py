from .db import get_costumers, count_customers, get_CA, get_CA_Potential, invoices_df, total_sales_by_period
from .KPIs import *
custmers = get_costumers()
custmers_count = count_customers()
CA= get_CA()
CAP = get_CA_Potential()
CAPMOIS = total_sales_by_period(invoices_df, "month")
CAPMOIS.iloc[1] = 300
CAPMOIS.iloc[0] = 200

chiffreaffaire = Chiffreaffaire(invoices_df)
nombreClient = NombreClient(invoices_df)
nombreFactures = NombreFactures(invoices_df)
employee_sales = ventes_par_client(invoices_df)

CA_par_produit = top_products_sold(product_details_df)
revenu_produit = Revenu_par_produit(product_details_df)