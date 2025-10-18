import uuid
from django.db import models
from django.core.exceptions import ValidationError

def validate_image(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image size should not exceed 5 MB.")

    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = image.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: .{ext}. Allowed: {', '.join(valid_extensions)}")


def category_image_upload_path(instance, filename):
    return f"categories/{instance.id}/{filename}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Category Name", max_length=255, unique=True)
    image = models.ImageField(
        upload_to=category_image_upload_path,
        validators=[validate_image],
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']

    def __str__(self):
        return self.name
