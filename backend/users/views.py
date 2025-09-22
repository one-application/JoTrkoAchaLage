from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'detail': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    print(username, password)
    token, created = Token.objects.get_or_create(user=User.objects.get(username=username))
    user= Token.objects.get(key=token.key).user
    print(user.groups,user)
    # group = GroupsSerializer(user.groups.all(),many=True,context={'request':None})
    # print(group.data)
    sinfo = UserSerializer(user, context={'request': None})
    response = {
        'token': token.key,
        'info':sinfo.data,
        # 'group' : group.data

    }
    return Response(response)
    
    # user = authenticate(username=username, password=password)
    # if user is not None:
    #     auth_login(request, user)
    #     token, _ = Token.objects.get_or_create(user=user)
    #     return Response({
    #         'token': token.key,
    #         'user': UserSerializer(user).data
    #     })
    # # return Response(
    # #     {'detail': 'Invalid credentials'},
    # #     status=status.HTTP_401_UNAUTHORIZED
    # # )
    # # serializer = self.serializer_class(data=request.data, context={'request':request})
    # # serializer.is_valid(raise_exception=True)
    # # print(serializer.validated_data)
    # # user = serializer.validated_data['user']
    # token, created = Token.objects.get_or_create(user=user)
    # user= Token.objects.get(key=token.key).user
    # print(user.groups,user)
    # group = GroupsSerializer(user.groups.all(),many=True,context={'request':None})
    # print(group.data)
    # sinfo = UserSerializer(user, context={'request': None})
    # response = {
    #     'token': token.key,
    #     'info':sinfo.data,
    #     'group' : group.data

    # }
    # return Response(response)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        # Handle user profile updates
        user_data = {k: v for k, v in request.data.items() if k in ['first_name', 'last_name', 'email']}
        profile_data = {k: v for k, v in request.data.items() if k in ['phone']}
        
        # Update user
        user_serializer = UserSerializer(
            request.user, 
            data=user_data, 
            partial=True
        )
        
        if user_serializer.is_valid():
            user_serializer.save()
            
            # Update profile if there's profile data
            if profile_data and hasattr(request.user, 'profile'):
                profile = request.user.profile
                for attr, value in profile_data.items():
                    setattr(profile, attr, value)
                profile.save()
            
            # Return updated user data
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
            
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        # Get the user from the request
        user = request.user
        # Update the password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Update or create a new token
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Password updated successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
