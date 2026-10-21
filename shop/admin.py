from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (Article, GalleryPhoto, GiftPerfume, Manager, Note, Order, OrderItem, Product, Review,
                     SiteSettings, Variant)

admin.site.site_header = 'MONA — управление магазином'
admin.site.site_title = 'MONA'
admin.site.index_title = 'Магазин'


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0
    fields = ['label', 'sublabel', 'price', 'old_price', 'gift_type', 'gift_count', 'gift', 'gift_en', 'gift_kk',
              'position']


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'position', 'is_active']
    list_editable = ['position', 'is_active']
    prepopulated_fields = {'slug': ['name']}
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'tagline', 'traits', 'lead', 'description', 'image', 'theme',
                           'subtitle', 'rating', 'position', 'is_active']}),
        ('English', {'classes': ['collapse'],
                     'fields': ['name_en', 'tagline_en', 'traits_en', 'lead_en', 'description_en']}),
        ('Қазақша', {'classes': ['collapse'],
                     'fields': ['name_kk', 'tagline_kk', 'traits_kk', 'lead_kk', 'description_kk']}),
    ]
    inlines = [VariantInline, NoteInline]


@admin.register(GiftPerfume)
class GiftPerfumeAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'gender', 'position', 'is_active']
    list_editable = ['position', 'is_active']
    prepopulated_fields = {'slug': ['brand', 'name']}
    fieldsets = [
        (None, {'fields': ['brand', 'name', 'slug', 'image', 'gender', 'notes', 'description', 'position',
                           'is_active']}),
        ('English', {'classes': ['collapse'], 'fields': ['notes_en', 'description_en']}),
        ('Қазақша', {'classes': ['collapse'], 'fields': ['notes_kk', 'description_kk']}),
    ]


class ReplyInline(admin.TabularInline):
    model = Review
    fk_name = 'parent'
    extra = 1
    fields = ['name', 'text', 'is_staff_reply', 'is_published']
    verbose_name = 'Ответ'
    verbose_name_plural = 'Ответы (поставьте галочку «Удалить», чтобы стереть ответ; «Ответ магазина» — ответить от имени MONA)'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_text', 'stars', 'kind', 'product', 'is_published', 'created', 'delete_link']
    list_display_links = ['name', 'short_text']
    list_editable = ['is_published']
    list_filter = ['is_published', ('parent', admin.EmptyFieldListFilter), 'rating', 'product']
    search_fields = ['name', 'text']
    inlines = [ReplyInline]
    actions = ['hide', 'publish', 'delete_selected']
    list_per_page = 50

    @admin.display(description='Текст')
    def short_text(self, obj):
        return obj.text[:80]

    @admin.display(description='Оценка', ordering='rating')
    def stars(self, obj):
        return '★' * obj.rating if obj.rating else '—'

    @admin.display(description='Тип')
    def kind(self, obj):
        return f'ответ → {obj.parent.name}' if obj.parent_id else 'отзыв'

    @admin.display(description='')
    def delete_link(self, obj):
        url = reverse('admin:shop_review_delete', args=[obj.pk])
        return format_html('<a href="{}" style="color:#ba2121;font-weight:600">🗑 Удалить</a>', url)

    @admin.action(description='Скрыть с сайта выбранные')
    def hide(self, request, queryset):
        n = queryset.update(is_published=False)
        self.message_user(request, f'Скрыто: {n}')

    @admin.action(description='Показать на сайте выбранные')
    def publish(self, request, queryset):
        n = queryset.update(is_published=True)
        self.message_user(request, f'Опубликовано: {n}')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['variant', 'price', 'old_price', 'gift', 'gift_color', 'engraving', 'gift_perfumes']
    filter_horizontal = ['gift_perfumes']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'name', 'phone', 'city', 'items_list', 'total_display', 'delivery', 'payment',
                    'manager', 'status']
    list_editable = ['manager', 'status']
    list_filter = ['status', 'manager', 'payment', 'delivery', 'created']
    search_fields = ['name', 'phone', 'city']
    readonly_fields = ['created']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items__variant__product', 'items__gift_perfumes')

    @admin.display(description='Товары и подарки')
    def items_list(self, obj):
        return '; '.join(f'{i.variant} ({i.gift_summary()})' if i.gift else str(i.variant) for i in obj.items.all())

    @admin.display(description='Сумма, ₸')
    def total_display(self, obj):
        return obj.total


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'is_published']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ['title']}
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'emoji', 'image', 'excerpt', 'body', 'published', 'is_published']}),
        ('English', {'classes': ['collapse'], 'fields': ['title_en', 'excerpt_en', 'body_en']}),
        ('Қазақша', {'classes': ['collapse'], 'fields': ['title_kk', 'excerpt_kk', 'body_kk']}),
    ]


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'position']
    list_editable = ['position']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'languages', 'hours', 'in_rotation', 'is_active', 'orders_count', 'chats',
                    'position']
    list_editable = ['in_rotation', 'is_active', 'position']
    readonly_fields = ['last_order', 'last_chat', 'chats']

    @admin.display(description='Заказов')
    def orders_count(self, obj):
        return obj.orders.count()
