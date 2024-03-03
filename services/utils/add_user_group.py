from random import shuffle
from django.db import transaction
from django.db.models import Count

from courses.models import Product, Group, GroupMembership


def choose_group_for_user(product):
    group = (
        Group.objects.annotate(num_users=Count("group")).order_by("num_users").first()
    )
    return group


def distribute_users_to_group(product_id, users):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None, "Продукт с указанным ID не найден"

    groups = Group.objects.filter(product=product)

    sh_lst = [product.author] + list(users)
    shuffle(sh_lst)

    user_per_group = len(users) // len(groups)
    remainder = len(users) % len(groups)

    index = 0
    with transaction.atomic():
        for group in groups:
            group_members = sh_lst[index : index + user_per_group]
            index += user_per_group
            if remainder > 0:
                group_members.append(sh_lst[index])
                index += 1
                remainder -= 1

            for user in group_members:
                GroupMembership.objects.create(group=group, user=user)

    return groups, "Пользователи успешно распределены"
