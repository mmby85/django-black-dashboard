from .db import get_costumers, count_customers, get_CA, get_CA_Potential, invoices_df, total_sales_by_period

custmers = get_costumers()
custmers_count = count_customers()
CA= get_CA()
CAP = get_CA_Potential()
CAPMOIS = total_sales_by_period(invoices_df, "month")
CAPMOIS.iloc[1] = 300
CAPMOIS.iloc[0] = 200