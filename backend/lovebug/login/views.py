from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Challenge, UserChallenge
from .serializers import ChallengeSerializer, UserChallengeSerializer
from django.db import transaction
from django.db.models import F, Sum, Count


def index(request):
    return JsonResponse({"ok": True, "service": "lovebug-backend"})


def get_username_from_request(request):
    """Helper to get username from X-Username header"""
    return request.headers.get('X-Username')


@api_view(['GET'])
@permission_classes([AllowAny])
def me(request):
    """Check if user has a username set (not used with localStorage, but keeping for compatibility)"""
    username = get_username_from_request(request)
    
    return JsonResponse({
        "authenticated": username is not None,
        "username": username
    })


@csrf_exempt
@require_POST
@permission_classes([AllowAny])
def api_logout(request):
    """Logout (not really used with localStorage, but keeping for compatibility)"""
    return JsonResponse({"ok": True})


@api_view(['GET'])
@permission_classes([AllowAny])
def challenges_list(request):
    """Get all active challenges with user completion status"""
    username = get_username_from_request(request)
    
    print(f"DEBUG: Username from header: {username}") 
    print(f"DEBUG: All headers: {dict(request.headers)}")  
    
    if not username:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    challenges = Challenge.objects.filter(is_active=True)
    serializer = ChallengeSerializer(challenges, many=True, context={'request': request, 'username': username})
    return Response(serializer.data)

@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_flag(request, challenge_id):
    username = get_username_from_request(request)
    
    if not username:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    submitted_flag = request.data.get('flag', '').strip()

    with transaction.atomic():
        try:
            challenge = Challenge.objects.select_for_update().get(id=challenge_id, is_active=True)
        except Challenge.DoesNotExist:
            return Response({"error": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)

        if UserChallenge.objects.filter(username=username, challenge=challenge).exists():
            return Response({"error": "Challenge already completed"}, status=status.HTTP_400_BAD_REQUEST)

        if submitted_flag != challenge.flag:
            return Response({"success": False, "message": "Incorrect flag. Try again!"}, status=status.HTTP_400_BAD_REQUEST)

        awarded = challenge.current_points

        UserChallenge.objects.create(username=username, challenge=challenge, awarded_points=awarded)
        Challenge.objects.filter(id=challenge.id).update(solves_count=F('solves_count') + 1)

    return Response({
        "success": True,
        "message": "Correct! Challenge completed!",
        "points": awarded 
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def user_stats(request):
    """Get user statistics"""
    username = get_username_from_request(request)
    
    if not username:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    completed = UserChallenge.objects.filter(username=username).order_by('-completed_at')
    total_points = completed.aggregate(total=Sum('awarded_points'))['total'] or 0
    
    return Response({
        "challenges_completed": completed.count(),
        "total_points": total_points,
        "recent_completions": UserChallengeSerializer(completed[:5], many=True).data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def scoreboard(request):
    """Get top users by points"""
    users = UserChallenge.objects.values('username').annotate(
        total_points=Sum('awarded_points'),
        challenges_count=Count('id')
    ).order_by('-total_points', 'challenges_count')[:10]
    
    scoreboard_data = [
        {
            "rank": idx + 1,
            "username": user['username'],
            "points": user['total_points'] or 0,
            "challenges_completed": user['challenges_count']
        }
        for idx, user in enumerate(users)
    ]
    
    return Response(scoreboard_data)