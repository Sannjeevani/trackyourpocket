from django.contrib import admin
from django.urls import path
from .views import CustomLoginView, index, edit, delete, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete')
]