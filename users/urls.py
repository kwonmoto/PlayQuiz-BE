from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users import views


urlpatterns = [
    path('signup/', views.UserView.as_view(), name='UserView'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    
]