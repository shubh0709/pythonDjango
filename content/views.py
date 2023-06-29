# user_content/views.py

from django.http import JsonResponse
from user_management.authentication import jwt_authenticate
from django.db import connections
from django.db.models import F
from user_content.models import Post

# recommendation_engine/views.py

from django.http import JsonResponse
from user_content.models import Post
from user_management.authentication import jwt_authenticate
from recommendation_engine.models import UserPreferences
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017')
mongodb = mongo_client['your_mongodb_database']

@jwt_authenticate
def get_recommendations(request):
    if request.method == 'GET':
        user = request.user
        preferences = UserPreferences.objects.get(user=user)
        interests = preferences.interests.all()

        # Query posts based on user's interests
        recommended_posts = Post.objects.filter(tags__in=interests).distinct()

        # Store recommended_posts in MongoDB
        collection = mongodb['recommended_posts']
        collection.insert_many([
            {
                'title': post.title,
                'content': post.content,
                'user_id': user.id
            } for post in recommended_posts
        ])

        data = [{
            'title': post.title,
            'content': post.content
        } for post in recommended_posts]

        return JsonResponse({'recommended_posts': data})

    return JsonResponse({'error': 'Invalid request method'})


@jwt_authenticate
def create_post(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')

        post = Post(user=user, title=title, content=content)
        post.save()

        return JsonResponse({'message': 'Post created successfully'})

    return JsonResponse({'error': 'Invalid request method'})

@jwt_authenticate
def get_posts(request):
    if request.method == 'GET':
        posts = Post.objects.filter(user=request.user)
        data = [{'title': post.title, 'content': post.content} for post in posts]
        return JsonResponse({'posts': data})

    return JsonResponse({'error': 'Invalid request method'})
