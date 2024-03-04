from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    COLOR_CHOICES = [
        ('pink', 'Pink'),
        ('white', 'White'),
        ('beige', 'Beige'),
        ('red', 'Red'),
    ]

    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name="variants")

    def __str__(self):
        return f"{self.color} {self.price} {self.size}"
