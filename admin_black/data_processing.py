from .db import get_costumers, count_customers, get_CA, get_CA_Potential, invoices_df, total_sales_by_period
from .KPIs import *
from .KPIs import ventes_par_client , NombreFactures 
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