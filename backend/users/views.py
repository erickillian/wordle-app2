from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
import requests

from backend.pagination import LargerResultsSetPagination, StandardResultsSetPagination
from users.models import User, TokenMetadata
from users.serializers import *

# Helper function to get the client IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Get the first IP in the list, which is the real client IP
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Use REMOTE_ADDR if not behind a proxy
        ip = request.META.get("REMOTE_ADDR")
    return ip


# Helper function to get location from IP address
def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        
        location_parts = []
        if "city" in data:
            location_parts.append(data["city"])
        if "region" in data:
            location_parts.append(data["region"])
        if "country" in data:
            location_parts.append(data["country"])
        
        if location_parts:
            return ", ".join(location_parts)
        else:
            return "Unknown Location"
    except requests.exceptions.RequestException:
        return "Unknown Location"
    except ValueError:
        return "Unknown Location"


class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Authenticate the user using email and password
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the client IP and location
        ip_address = get_client_ip(request)
        location = get_location_from_ip(ip_address)
        device = request.META.get("HTTP_USER_AGENT")

        # Create a refresh and access token
        refresh = RefreshToken.for_user(user)

        # Get the outstanding token for the user
        outstanding_token = OutstandingToken.objects.get(user=user, token=str(refresh))

        # Update the token metadata
        TokenMetadata.objects.create(
            token=outstanding_token,
            ip_address=ip_address,
            location=location,
            device=device,
        )

        access_token = str(refresh.access_token)

        return Response(
            {
                "refresh": str(refresh),
                "access": access_token,
                "created_at": outstanding_token.created_at,
                "user": UserSelfSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

def logout_user(refresh_token):
    try:
        outstanding_token = OutstandingToken.objects.filter(
            token=refresh_token
        ).first()

        if outstanding_token:
            # Blacklist the OutstandingToken
            BlacklistedToken.objects.create(token=outstanding_token)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"message": "Successfully logged out"}, status=status.HTTP_200_OK
    )


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's refresh token from the request
            refresh_token = request.data.get("refresh")

            # Blacklist the refresh token
            RefreshToken(refresh_token).blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)  # No content response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRemoveSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_time = request.data.get("session_time")
        if not session_time:
            return Response(
                {"error": "Session time is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            session_time = datetime.strptime(session_time, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Find the outstanding token created at the specified time
            outstanding_token = OutstandingToken.objects.filter(
                user=request.user, created_at=session_time
            ).first()

            refresh_token = str(outstanding_token.token)

            # Blacklist the refresh token
            RefreshToken(refresh_token).blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)  # No content response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new user
            user = serializer.save()

            # Get the client IP and location
            ip_address = get_client_ip(request)
            location = get_location_from_ip(ip_address)
            device = request.META.get("HTTP_USER_AGENT")

            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            
            # Get the outstanding token for the user
            outstanding_token = OutstandingToken.objects.get(user=user, token=str(refresh))

            # Update the token metadata
            TokenMetadata.objects.create(
                token=outstanding_token,
                ip_address=ip_address,
                location=location,
                device=device,
            )

            access_token = str(refresh.access_token)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": access_token,
                    "created_at": outstanding_token.created_at,
                    "user": UserSelfSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            refresh = RefreshToken(refresh_token)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        access_token = str(refresh.access_token)

        return Response(
            {
                "refresh": str(refresh),
                "access": access_token,
            },
            status=status.HTTP_200_OK,
        )


class UserSelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSelfSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSelfSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserSessionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSessionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return OutstandingToken.objects.filter(
            user=self.request.user,
            expires_at__gt=datetime.now()
        ).exclude(
            blacklistedtoken__isnull=False
        ).order_by('-created_at')

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ["id"]
    permission_classes = [IsAuthenticated]
    search_fields = ["email", "full_name"]
    filter_backends = [SearchFilter]
    pagination_class = LargerResultsSetPagination

    # @method_decorator(cache_page(60*15))  # Cache the view for 15 minutes
    def list(self, request, *args, **kwargs):
        # Simulate a long networking delay
        return super().list(request, *args, **kwargs)
