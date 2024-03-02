from django.contrib import admin
from .models import Product, Lesson, Group, GroupMembership


@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ("product_name", "start_time", "price", "author", "lesson_count")


@admin.register(Lesson)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", "link")


@admin.register(Group)
class UserAdmin(admin.ModelAdmin):
    list_display = ("group_name",)


@admin.register(GroupMembership)
class UserAdmin(admin.ModelAdmin):
    list_display = ("group", "user")
