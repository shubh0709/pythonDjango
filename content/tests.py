from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_content.models import Post

User = get_user_model()

class RecommendationEngineTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.preferences = UserPreferences.objects.create(user=self.user)

        self.mongo_client = MongoClient('mongodb://localhost:27017')
        self.mongodb = self.mongo_client['your_mongodb_database']
        self.collection = self.mongodb['recommended_posts']

    def tearDown(self):
        self.collection.delete_many({})
        self.mongo_client.close()

    def test_get_recommendations(self):
        post1 = Post.objects.create(title='Post 1', content='Content 1')
        post2 = Post.objects.create(title='Post 2', content='Content 2')
        post3 = Post.objects.create(title='Post 3', content='Content 3')

        self.preferences.interests.add('interest1', 'interest2')

        url = reverse('get_recommendations')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recommended_posts']), 2)

        # Verify the stored documents in MongoDB
        documents = self.collection.find({'user_id': self.user.id})
        self.assertEqual(documents.count(), 2)
        self.assertEqual(documents[0]['title'], 'Post 1')
        self.assertEqual(documents[1]['content'], 'Content 2')

class UserContentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_post(self):
        url = reverse('create_post')
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'Test Post')
        self.assertEqual(Post.objects.first().content, 'This is a test post.')

    def test_get_posts(self):
        post1 = Post.objects.create(user=self.user, title='Post 1', content='Content 1')
        post2 = Post.objects.create(user=self.user, title='Post 2', content='Content 2')

        url = reverse('get_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['posts']), 2)
        self.assertEqual(response.json()['posts'][0]['title'], 'Post 1')
        self.assertEqual(response.json()['posts'][1]['title'], 'Post 2')
        self.assertEqual(response.json()['posts'][0]['content'], 'Content 1')
        self.assertEqual(response.json()['posts'][1]['content'], 'Content 2')
