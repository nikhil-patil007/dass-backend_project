from django.contrib import admin
from django.urls import path
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, ProductImage
import zipfile
import csv
from io import TextIOWrapper
from django.core.files.base import ContentFile
from categories.models import Category


class ZipImportForm(forms.Form):
	zip_file = forms.FileField(label="ZIP file containing CSV and images")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "inStock")

	def get_urls(self):
		urls = super().get_urls()
		custom = [
			path("import-zip/", self.admin_site.admin_view(self.import_zip_view), name="products_import_zip"),
		]
		return custom + urls

	def import_zip_view(self, request):
		if request.method == "POST":
			form = ZipImportForm(request.POST, request.FILES)
			if form.is_valid():
				z = zipfile.ZipFile(request.FILES["zip_file"])
				try:
					with z.open("products.csv") as prodf:
						reader = csv.DictReader(TextIOWrapper(prodf, "utf-8"))
						created = 0
						for row in reader:
							name = row.get("name")
							category_name = row.get("category")
							price = row.get("price") or 0
							description = row.get("description", "")
							images = row.get("images", "")
							if not name or not category_name:
								continue
							category, _ = Category.objects.get_or_create(name=category_name)
							product, created_flag = Product.objects.get_or_create(
								name=name,
								defaults={
									"category": category,
									"price": price,
									"description": description,
								},
							)
							# update fields if already existed
							if not created_flag:
								product.category = category
								product.price = price
								product.description = description
								product.save()

							if images:
								for img_name in [i.strip() for i in images.split(";") if i.strip()]:
									if img_name in z.namelist():
										data = z.read(img_name)
										pi = ProductImage(product=product)
										pi.image.save(img_name, ContentFile(data), save=True)
                        
					messages.success(request, "Products imported from ZIP archive")
				except KeyError:
					messages.error(request, "products.csv not found in the ZIP archive")
				return redirect("..")
		else:
			form = ZipImportForm()
		context = {"form": form, "title": "Import Products from ZIP"}
		return render(request, "admin/import_zip.html", context)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "is_primary", "uploaded_at")