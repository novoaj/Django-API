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
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = LogoutSerializer
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
        print("Authenticated user:", user)  # Debug line to print the authenticated user
        return UserRecipe.objects.filter(user=user)[:10]

class UserRecipeCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserRecipeSerializer
    def post(self, request):
        # get user id from request?
        user=request.user
        # get recipe id
        recipe_data = request.data.get('recipe')
        recipe_id = recipe_data.get("id")
        label = recipe_data.get("label")
        thumbnail = recipe_data.get("thumbnail")
        if not recipe_id or not label or not thumbnail:
            return Response({'error': 'Recipe ID, title, and thumbnail are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ensure recipe exists or gets created
        recipe, created = Recipe.objects.get_or_create(
                api_id=recipe_id,
                defaults={'title': label, 'thumbnail': thumbnail}
            )
        # UserRecipe entry
        try:
            user_recipe, created = UserRecipe.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response({'message': 'Recipe saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Recipe already saved for this user'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'error': 'Error saving recipe'}, status=status.HTTP_400_BAD_REQUEST)

class UserRecipeDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, recipe_id):
        user = request.user
        try:
            user_recipe = UserRecipe.objects.get(user=user, recipe__api_id=recipe_id)
            user_recipe.delete()
            return Response({'message': 'Recipe link deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserRecipe.DoesNotExist:
            return Response({'error': 'Recipe link not found'}, status=status.HTTP_404_NOT_FOUND)