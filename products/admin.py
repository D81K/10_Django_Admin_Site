from django.contrib import admin
from .models import Product, Review
from django.utils import timezone


# Register your models here.

admin.site.site_title = 'Clarusway Title'
admin.site.site_header = 'Clarusway Admin Portal'
admin.site.index_title = 'Welcome to Clarusway Admin Portal'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    classes = ('collapse',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'is_in_stock', 'update_date', 'added_days_ago')
    list_editable = ('is_in_stock', )
    list_filter = ('is_in_stock', 'create_date')
    ordering = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    list_per_page = 25
    date_hierarchy = 'update_date'
    # fields = (('name', 'slug'), 'description', 'is_in_stock')

    inlines = (ReviewInline, )

    fieldsets = (
        (None, {
            "fields" : (
                ('name','slug') , 'is_in_stock'
            ),
        }),
        ('Optional Settings', {
            "classes" : ("collapse",),
            "fields" : ("description",),
            'description' : "You can use this section for optional settings"
        })
    )


    # Actions

    actions = ('is_in_stock', )

    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} product(s) added to stock.")

    is_in_stock.short_description = 'Selected product(s) will be added to stock'


    # Methods

    def added_days_ago(self,product):
        difference = timezone.now() - product.create_date
        return difference.days


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50


admin.site.register(Product, ProductAdmin)