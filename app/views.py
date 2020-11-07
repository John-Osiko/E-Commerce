from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from django.contrib.auth.models import User
from .forms import *
from .serializer import ShopProductSerializer, UserRegistrationSerializer, UserLoginSerializer, UserListSerializer

# Create your views here.
class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)


class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
        register_form = {
            'form': form,
        }
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')
def home(request):
    current_user = request.user
    params = {
        'current_user': current_user,
    }
    return render(request, "my_temps/home.html", params)


def logout_request(request):
    logout(request)
    message = "Logged out successfully!"
    params = {
        'message': message,
    }
    return redirect('registration/signup.html', {'message': message})



def login_request(request):
    form = AuthenticationForm()
    return render(request = request, template_name = "registration/login.html", context={"form":form})


class ProdsList(APIView):
    def get(self, request, format=None):
        all_prods = ShopProduct.objects.all()
        serializers = ShopProduct(all_prods, many=True)
        return Response(serializers.data)


def search_results(request):
    if 'productsearch' in request.GET and request.GET["productsearch"]:
        product_category = request.GET.get("imagesearch")
        searched_products = Product.search_by_category(product_category)
        message = f"{product_category}"
        print(searched_products)
        return render(request, 'my_temps/search.html', {"message": message, "images": searched_products})
    else:
        message = "You haven't searched for any valid item category"
        return render(request, 'my_temps/search.html', {"message": message})


def project_view(request, post):
    post = Product.objects.get(title=post)
    data = {
        'post': post,
    }
    return render(request, 'my_temps/home.html', data)