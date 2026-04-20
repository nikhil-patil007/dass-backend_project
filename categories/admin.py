from django.contrib import admin
from django.urls import path
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category
import zipfile
import csv
from io import TextIOWrapper
from django.core.files.base import ContentFile


class ZipImportForm(forms.Form):
	zip_file = forms.FileField(label="ZIP file containing CSV and images")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)

	def get_urls(self):
		urls = super().get_urls()
		custom = [
			path("import-zip/", self.admin_site.admin_view(self.import_zip_view), name="categories_import_zip"),
		]
		return custom + urls

	def import_zip_view(self, request):
		if request.method == "POST":
			form = ZipImportForm(request.POST, request.FILES)
			if form.is_valid():
				z = zipfile.ZipFile(request.FILES["zip_file"])
				# look for categories.csv
				try:
					with z.open("categories.csv") as catf:
						reader = csv.DictReader(TextIOWrapper(catf, "utf-8"))
						created = 0
						for row in reader:
							name = row.get("name")
							image_name = row.get("image")
							if not name:
								continue
							obj, created_flag = Category.objects.get_or_create(name=name)
							if image_name and image_name in z.namelist():
								data = z.read(image_name)
								obj.image.save(image_name, ContentFile(data), save=True)
							if created_flag:
								created += 1
					messages.success(request, f"Imported categories. Created: {created}")
				except KeyError:
					messages.error(request, "categories.csv not found in the ZIP archive")
				return redirect("..")
		else:
			form = ZipImportForm()
		context = {
			"form": form,
			"title": "Import Categories from ZIP",
		}
		return render(request, "admin/import_zip.html", context)