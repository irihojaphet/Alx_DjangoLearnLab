from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Post instances.
    Provides CRUD operations with filtering and search capabilities.
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """Automatically set the author to the current user"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        """Get all comments for a specific post"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Comment instances.
    Provides CRUD operations for comments on posts.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def get_queryset(self):
        """Optionally filter comments by post"""
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        """Automatically set the author to the current user"""
        serializer.save(author=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    """
    Feed endpoint.
    GET: Retrieve posts from users that the current user follows.
    Posts are ordered by creation date, most recent first.
    """
    # Get users that the current user follows
    following_users = request.user.following.all()
    
    # Get posts from followed users, ordered by creation date (newest first)
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination
    page = request.query_params.get('page', 1)
    page_size = 10
    
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
    
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_posts = posts[start:end]
    serializer = PostListSerializer(paginated_posts, many=True, context={'request': request})
    
    return Response({
        'count': posts.count(),
        'next': f'/api/feed/?page={page + 1}' if end < posts.count() else None,
        'previous': f'/api/feed/?page={page - 1}' if page > 1 else None,
        'results': serializer.data
    }, status=status.HTTP_200_OK)
