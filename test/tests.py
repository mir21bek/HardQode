from django.test import TestCase
from courses.models import GroupMembership
from services.utils.add_user_group import distribute_users_to_group
from users.models import CustomUser
from Factory.users.factory_user import CustomUserFactory
from Factory.users.courses_factory import GroupFactory, ProductFactory


class DistributeUsersToGroupTestCase(TestCase):
    def setUp(self):
        author = CustomUser.objects.create(user_name="author_user")
        self.product = ProductFactory()
        self.group1 = GroupFactory(product=self.product)
        self.group2 = GroupFactory(product=self.product)
        self.user1 = CustomUserFactory()
        self.user2 = CustomUserFactory()
        self.user3 = CustomUserFactory()
        self.user4 = CustomUserFactory()

    def test_distribute_users_to_group(self):
        groups, _ = distribute_users_to_group(
            self.product.id, [self.user1, self.user2, self.user3, self.user4]
        )

        for group in groups:
            group_has_users = GroupMembership.objects.filter(group=group).exists()
            self.assertTrue(group_has_users)
