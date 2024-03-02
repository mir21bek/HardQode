from django.db import models
from users.models import CustomUser


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Название продукта")
    description = models.TextField(
        max_length=500, verbose_name="Описание", null=True, blank=True
    )
    start_time = models.DateTimeField(verbose_name="Дата начало")
    price = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Цена")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор",
    )
    lesson_count = models.PositiveIntegerField(
        null=True, verbose_name="Количество уроков"
    )
    available = models.BooleanField(default=True)
    is_buying = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукт"

    def __str__(self):
        return self.product_name


class Lesson(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_lesson"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    link = models.CharField(max_length=255, unique=True, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Уроки"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Group(models.Model):
    group_name = models.CharField(max_length=255, verbose_name="Название группы")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="group_product"
    )
    min_users = models.PositiveIntegerField(verbose_name="мин. количество участников")
    max_users = models.PositiveIntegerField(verbose_name="макс. количество участников")

    class Meta:
        verbose_name = "Группы"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.group_name


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="group_user"
    )

    class Meta:
        verbose_name = "Участники группы"
        verbose_name_plural = "Участники группы"

    def __str__(self):
        return self.group.group_name
