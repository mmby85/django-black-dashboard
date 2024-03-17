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


