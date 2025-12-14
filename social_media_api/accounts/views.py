from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    User registration endpoint.
    Returns a token upon successful registration.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint.
    Returns a token upon successful login.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    User profile management endpoint.
    GET: Retrieve user profile
    PUT/PATCH: Update user profile
    """
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user endpoint.
    POST: Add a user to the current user's following list.
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': 'You are already following this user.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.add(user_to_follow)
    return Response(
        {
            'message': f'You are now following {user_to_follow.username}.',
            'following_count': request.user.following.count(),
            'followers_count': user_to_follow.followers.count()
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user endpoint.
    POST: Remove a user from the current user's following list.
    """
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': 'You are not following this user.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.remove(user_to_unfollow)
    return Response(
        {
            'message': f'You have unfollowed {user_to_unfollow.username}.',
            'following_count': request.user.following.count(),
            'followers_count': user_to_unfollow.followers.count()
        },
        status=status.HTTP_200_OK
    )