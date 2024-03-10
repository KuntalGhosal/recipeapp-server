from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import RecipeCategory, Recipe
#RecipeListAPIView:
class RecipeListAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = RecipeCategory.objects.create(name='Test Category')
        self.recipe1 = Recipe.objects.create(
            author=self.client.post('/api/user/register/', data={'email':'test1@example.com', 'username':'testuser1', 'password':'strongpassword'}).json()['user'],
            category=self.category,
            title='Test Recipe 1',
            desc='Description 1'
        )
        self.recipe2 = Recipe.objects.create(
            author=self.client.post('/api/user/register/',data={'email':'test1@example.com', 'username':'testuser1', 'password':'strongpassword'}).json()['user'],
            category=self.category,
            title='Test Recipe 2',
            desc='Description 2'
        )

    def test_get_recipe_list_unauthenticated(self):
        response = self.client.get('/api/recipe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_category(self):
        response = self.client.get('/api/recipe/', data={'category__name': 'Test Category'})
        self.assertEqual(len(response.data), 2)

    def test_filter_by_author(self):
        response = self.client.get('/api/recipe/', data={'author__username': 'testuser'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.recipe1.title)
        
 #RecipeCreateAPIView:
class RecipeCreateAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='testuser', password='password')
        # Create a category object (assuming it's required)
        self.category = RecipeCategory.objects.create(name='Test Category')

    def test_create_recipe_authenticated(self):
        data = {
            'category': self.category.pk,  # Use category ID instead of assuming it exists
            'title': 'New Recipe',
            'desc': 'Description for new recipe',
            'picture': 'path/to/image.jpg',  # Add picture field (assuming required)
            'cook_time': '00:30:00',  # Cook time in HH:MM:SS format (assuming required)
            'ingredients': 'Ingredient 1, Ingredient 2',  # Add ingredients field (assuming required)
            'procedure': 'Cooking steps...',  # Add procedure field (assuming required)
        }
        response = self.client.post('/api/recipe/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)  # Assuming no existing recipes

    def test_create_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.post('/api/recipe/create/', data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
