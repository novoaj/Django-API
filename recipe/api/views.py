from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.db.utils import IntegrityError
from rest_framework import status, generics, views, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserRecipeSerializer
from .models import UserRecipe, Recipe
# Create your views here.

class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save() # invokes serializer create() method
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST) # https://stackoverflow.com/questions/4678584/in-django-how-can-i-get-an-exceptions-message
        except IntegrityError:
            return Response({"error": "A user with this email or username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred, please try again"}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        try: 
            serializer.is_valid(raise_exception=True) # serializer authenticates our user and returns user data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "An error occurred, please try again"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRecipeListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserRecipeSerializer

    def get_queryset(self):
        # Return recipes for the currently authenticated user
        user = self.request.user
        return UserRecipe.objects.filter(user=user)[:10]

class UserRecipeCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserRecipeSerializer
    def post(self, request):
        print(request)
        # get user id from request?
        user=request.user
        # get recipe id
        recipe_uri = request.data.get('recipe')
        if not recipe_uri:
            return Response({'error': 'Recipe URI is required'}, status=status.HTTP_400_BAD_REQUEST)
        # ensure recipe exists or gets created
        recipe, created = Recipe.objects.get_or_create(api_id=recipe_uri)
        # UserRecipe entry
        try:
            user_recipe, created = UserRecipe.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response({'message': 'Recipe saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Recipe already saved for this user'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'error': 'Error saving recipe'}, status=status.HTTP_400_BAD_REQUEST)