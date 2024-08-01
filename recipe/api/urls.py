from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"), # we dont need a view just endpoint?
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"), 
    path('user-recipes/', views.UserRecipeListView.as_view(), name='user-recipe-list'),
    path('user-recipes/create/', views.UserRecipeCreateView.as_view(), name='user-recipe-create'),
    path('user-recipes/delete/<str:recipe_id>/', views.UserRecipeDeleteView.as_view(), name='user-recipe-delete'),
]