from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

class Invoice(models.Model):
    customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()

    def __str__(self) -> str:
        return f"invoice {self.id}-{self.date}"

 # new ones : 
'''
class Invoice(models.Model):
    id_invoice = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    partner_id = models.IntegerField()
    partner_name = models.CharField(max_length=255)
    invoice_line_ids = models.TextField() 

class ProductDetail(models.Model):
    invoice_id = models.IntegerField()
    invoice_name = models.CharField(max_length=255)
    product_name = models.TextField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.IntegerField()
'''
