from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser

from .models import RecipeCategory, Recipe
#RecipeListAPIView:
class RecipeListAPIViewTestCase(TestCase):

   def setUp(self):
    self.client = APIClient()
    self.category = RecipeCategory.objects.create(name='Test Category')

    # Register a user and extract relevant data from the response
    registration_response = self.client.post('/api/user/register/', data={
        'email': 'test1@example.com',
        'username': 'testuser1',
        'password': 'strongpassword'
    })
    self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)  # Assert successful registration

    user_data = registration_response.json()
    self.user_id = user_data['id']
    self.access_token = user_data['tokens']['access']

    # Include required fields and provide appropriate values
    self.recipe1 = Recipe.objects.create(
        author_id=self.user_id,  # Use user ID from registration response
        category=self.category,
        title='Test Recipe 1',
        desc='Description 1',
        picture='path/to/image1.jpg',  # Assuming picture is required
        cook_time='01:30:00',  # Example cook time
        ingredients='Ingredient 1, Ingredient 2',
        procedure='Cooking steps 1...'
    )
    self.recipe2 = Recipe.objects.create(
        author_id=self.user_id,  # Use user ID from registration response
        category=self.category,
        title='Test Recipe 2',
        desc='Description 2',
        picture='path/to/image2.jpg',  # Assuming picture is required
        cook_time='00:45:00',  # Example cook time
        ingredients='Ingredient 3, Ingredient 4',
        procedure='Cooking steps 2...'
    )
    self.client = APIClient()
    self.category = RecipeCategory.objects.create(name='Test Category')

    # Create a single user and reuse it for both recipes
    self.user = self.client.post('/api/user/register/', data={
        'email': 'test1@example.com',
        'username': 'testuser1',
        'password': 'strongpassword'
    }).json()['user']

    # Include required fields and provide appropriate values
    self.recipe1 = Recipe.objects.create(
        author=self.user,
        category=self.category,
        title='Test Recipe 1',
        desc='Description 1',
        picture='path/to/image1.jpg',  # Assuming picture is required
        cook_time='01:30:00',  # Example cook time
        ingredients='Ingredient 1, Ingredient 2',
        procedure='Cooking steps 1...'
    )
    self.recipe2 = Recipe.objects.create(
        author=self.user,
        category=self.category,
        title='Test Recipe 2',
        desc='Description 2',
        picture='path/to/image2.jpg',  # Assuming picture is required
        cook_time='00:45:00',  # Example cook time
        ingredients='Ingredient 3, Ingredient 4',
        procedure='Cooking steps 2...'
    )

        
 #RecipeCreateAPIView:
class RecipeCreateAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = CustomUser.objects.create_user(email='test1@example.com', username='testuser1', password='strongpassword')
        user.save()        # Create a category object (assuming it's required)
        self.category = RecipeCategory.objects.create(name='Test Category')

    def test_create_recipe_authenticated(self):
    # Login the user and extract access token
        data = {
        'email': 'test1@example.com',
        'password': 'strongpassword'
        }
        response = self.client.post('/api/user/login/', data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tokens', response.data) # Assert successful login

        login_data = response.data
        # print(login_data,"kjhkjjkh")
        access_token = login_data['tokens']['access']

        # Set the Authorization header with Bearer token for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        RecipeCategory.objects.get_or_create(name="Paneer")
        print(RecipeCategory)
        test_category = RecipeCategory.objects.filter(name="Paneer")[0]
        # Prepare recipe data
        data = {
            "category": test_category,
            "picture": "https://fastly.picsum.photos/id/1069/200/300.jpg?hmac=z7ef02jy_-2I0_UTVob-AN6AWxP7-4bTJmZZnnLKMgk",
            "title": "Paneer Handi masala gdfgddd",
            "desc": "Chicken masala with butter",
            "cook_time": "15:21:37.123456",
            "ingredients": "Butter,Chicken,onion,ginger",
            "procedure": "testing",
            "author":"testuser1",
            "username":"testuser1"
            }

        # Send the POST request to create a recipe
        response = self.client.post('/api/recipe/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_create_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.post('/api/recipe/create/', data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
