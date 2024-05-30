from django.contrib import admin

from .models import About, News, Vacancy, FAQEntry, Company, Review


admin.site.register(About)
admin.site.register(News)
admin.site.register(Vacancy)
admin.site.register(FAQEntry)
admin.site.register(Company)
admin.site.register(Review)

