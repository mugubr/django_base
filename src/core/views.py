"""
API views using Ormar ORM for async database operations.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, User


@api_view(["GET"])
def hello_api(request):
    """
    Um endpoint de exemplo que retorna uma mensagem de boas-vindas.
    """
    data = {"message": "Hello! Now using Ormar ORM!"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
async def list_users(request):
    """
    List all users using Ormar async queries.
    """
    users = await User.objects.all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        for user in users
    ]
    return Response(users_data, status=status.HTTP_200_OK)


@api_view(["POST"])
async def create_user(request):
    """
    Create a new user using Ormar.
    """
    user = await User.objects.create(
        username=request.data.get("username"),
        email=request.data.get("email"),
        first_name=request.data.get("first_name"),
        last_name=request.data.get("last_name"),
    )
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
async def list_posts(request):
    """
    List all posts with their authors using Ormar prefetch.
    """
    posts = await Post.objects.select_related("author").all()
    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
            },
            "published": post.published,
        }
        for post in posts
    ]
    return Response(posts_data, status=status.HTTP_200_OK)


@api_view(["POST"])
async def create_post(request):
    """
    Create a new post using Ormar.
    """
    author = await User.objects.get(id=request.data.get("author_id"))
    post = await Post.objects.create(
        title=request.data.get("title"),
        content=request.data.get("content"),
        author=author,
        published=request.data.get("published", False),
    )
    return Response(
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author.id,
        },
        status=status.HTTP_201_CREATED,
    )
