from django.db import models


class BoxCategory(models.TextChoices):
    STANDARD = "STANDARD", "Standard Goods"
    FRAGILE = "FRAGILE", "Fragile / Glassware"
    APPAREL = "APPAREL", "Clothing / Soft Goods"
    HEAVY_DUTY = "HEAVY_DUTY", "Heavy Machinery / Tools"
    LIQUID = "LIQUID", "Bottles / Liquids"


class Box(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField(help_text="Internal length in cm")
    width = models.FloatField(help_text="Internal width in cm")
    height = models.FloatField(help_text="Internal height in cm")
    max_weight = models.FloatField(help_text="Max weight capacity in kg")
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    allowed_categories = models.JSONField(default=list, help_text="List of compatible BoxCategory strings")

    @property
    def volume(self):
        return self.length * self.width * self.height

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    length = models.FloatField(help_text="Length in cm")
    width = models.FloatField(help_text="Width in cm")
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    category = models.CharField(max_length=50, choices=BoxCategory.choices, blank=True)

    def __str__(self):
        return self.title
