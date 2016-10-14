from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.shopping_list = ShoppingList.objects.create(
            name='Grocery', owner=user, budget=400)
        self.item = ShoppingListItem.objects.create(
            name='milk', shopping_list=self.shopping_list, price=50)
        self.client = Client()
        self.client.login(username='admin', password='admin')


class ShoppingListTestSuite(Base):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Grocery', response.content)

    def test_create_new_shopping_list(self):
        url = reverse('index')
        data = {'name': 'Grocery', 'budget': 400}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list_route(self):
        url = reverse(
            'edit-shopping-list', kwargs={'id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list(self):
        url = reverse(
            'edit-shopping-list', kwargs={'id': self.shopping_list.id})
        data = {'name': 'Luxury', 'budget': 20000000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        item = ShoppingList.objects.get(pk=self.shopping_list.id)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.budget, data['budget'])


class ShoppingListItemTestSuite(Base):
    def test_view_shopping_list_items(self):
        url = reverse(
            'items', kwargs={'shopping_list_id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item.name, response.content)
        self.assertIn(str(self.item.price), response.content)

    def test_create_new_shopping_list_item(self):
        url = reverse(
            'items', kwargs={'shopping_list_id': self.shopping_list.id})
        data = {'name': 'sugar', 'price': 20}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_edit_shopping_list_item_route(self):
        url = reverse(
            'edit-item', kwargs={'id': self.item.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list_item(self):
        url = reverse(
            'edit-item', kwargs={'id': self.item.id}
        )
        data = {'name': 'Sugar', 'price': 330}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        item = ShoppingListItem.objects.get(pk=self.item.id)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.price, data['price'])

        
    def test_delete_shopping_list_item_route(self):
        url = reverse(
            'delete-item', kwargs={'id': self.item.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_shopping_list_item_name(self):
        url = reverse(
            'delete-item', kwargs={'id': self.item.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
