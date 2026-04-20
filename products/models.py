import uuid
from django.db import models
from django.core.exceptions import ValidationError
from categories.models import Category

def validate_image(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image size should not exceed 5 MB.")

    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = image.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f"Unsupported file extension: .{ext}. Allowed: {', '.join(valid_extensions)}"
        )

def product_image_upload_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_by_category')
    name = models.CharField("Jewellery Name", max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Weight in grams")
    policy1 = models.CharField(max_length=100, blank=True, null=True)
    policy2= models.CharField(max_length=100, blank=True, null=True)
    policy3 = models.CharField(max_length=100, blank=True, null=True)
    policy4 = models.CharField(max_length=100, blank=True, null=True)
    inStock = models.BooleanField(blank=True, null=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to=product_image_upload_path, validators=[validate_image])
    is_primary = models.BooleanField(default=False, help_text="Set this image as the primary display image")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f"{self.product.name} Image ({'Primary' if self.is_primary else 'Secondary'})"

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
