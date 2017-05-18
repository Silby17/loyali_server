import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.template import loader
from django.contrib import auth
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from loyali.models import Vendor, Subscription, VendorUser, Card, CardsInUse
from loyali.serializer import VendorSerializer, VendorUserModelSerializer, \
    AdminUserSerializer, SingleCardSerializer, SubscribedCustomersSerializer

# Group name definitions
VENDOR_STAFF_GROUP_NAME = 'vendor_staff'
VENDOR_GROUP_NAME = 'Vendor'
ADMIN_GROUP_NAME = 'Admin'


# The Following code handles the GET request for the HTML Pages
def __redirect_after_login(user):
    if VENDOR_GROUP_NAME in user.groups.values_list('name', flat=True):
        return redirect(reverse('vendor_main'))
    elif ADMIN_GROUP_NAME in user.groups.values_list('name', flat=True):
        return redirect(reverse('admin_main'))
    else:
        return redirect(reverse('index'))


# Handles all the login requests
def login(req):
    context = {}
    if req.user.is_authenticated():
        return __redirect_after_login(req.user)
    # If user is not already logged in
    else:
        data = req.POST
        username = data.get('username')
        password = data.get('password')
        try:
            # CHECK if user exists
            user = User.objects.get(username=username)
            # If user exists Then Verify the password.
            auth_user = auth.authenticate(username=username, password=password)
            # If password is verified & correct, then login the user
            if auth_user is not None:
                auth.login(req, auth_user)
                return __redirect_after_login(auth_user)
            else:
                context['error_message'] = "Invalid credentials"
                return render(req, 'loyali/login.html', context)
        except User.DoesNotExist:
            context['error_message'] = "User not registered"
        return render(req, 'loyali/login.html', context)


class VendorAPI(APIView):
    parser_classes = ([FormParser, MultiPartParser])

    def post(self, request):
        raw_data = request.POST.copy()
        vendor_user_data = raw_data.pop('user')
        vendor_user_data = json.loads(vendor_user_data[0])
        vendor_data = raw_data
        vendor_serializer = VendorSerializer(data=vendor_data)
        # Checks if the user data is valid
        if vendor_serializer.is_valid():
            vendor = vendor_serializer.save()
        else:
            errors = ""
            serializer_errors = vendor_serializer.errors
            for error in serializer_errors:
                errors += serializer_errors[error][0]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=errors)
        files = request.FILES
        # Gets the file do upload
        if 'logo_title' in files:
            logo_title = files.get('logo_title')
            vendor.logo_title = logo_title
            vendor.save()
        # Adds the User to the vendor
        vendor_user_data['vendor_id'] = vendor.id
        vendor_user_serializer = VendorUserModelSerializer(data=vendor_user_data)
        vendor_user_serializer.is_valid(raise_exception=True)
        user = vendor_user_serializer.save()
        group = Group.objects.get_or_create(name=VENDOR_GROUP_NAME)[0]
        group.user_set.add(user)
        template = loader.get_template('loyali/saved.html')
        context = {'saved': 'saved'}
        return HttpResponse(template.render(context, request))

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)


@login_required
def delete_vendors(request):
    vendors = Vendor.objects.all()
    data = request.POST
    ids = data.get('ids')
    if ids is not None:
        vendor_ids = ids.split(',')
        for id in vendor_ids:
            if id != "":
                vendors.filter(id=id).delete()
    return HttpResponse(status=status.HTTP_200_OK)


class AdminUserAPI(APIView):
    def post(self, request):
        raw_data = request.POST.copy()
        username = raw_data.get('username')
        password = raw_data.get('password')
        first_name = raw_data.get('first_name')
        last_name = raw_data.get('last_name')
        group_data = raw_data.pop('group')
        group_data = group_data[0]
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name)
        group = Group.objects.get_or_create(name=group_data)[0]
        group.user_set.add(user)
        if user:
            template = loader.get_template('loyali/saved.html')
            context = {'saved': 'saved'}
            return HttpResponse(template.render(context, request))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        users = users.extra(order_by=['id'])
        # users = User.objects.filter(groups__name='admin')
        serializer = AdminUserSerializer(users, many=True).data
        return Response(serializer)


class AddCardAPI(APIView):
    def get(self, request):
        template = loader.get_template('loyali/vendor_pages/add_card.html')
        context = {'page': 'Add Card'}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        data = request.POST.copy()
        vendor_id = ''
        if request.user.is_authenticated():
            vendor_id = request.user.id
        try:
            vendor = VendorUser.objects.get(id=vendor_id).vendor
        except:
            context = {'error_message': 'no vendor of this ID'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        description = data.get('description')
        max = data.get('max')
        type = data.get('type')
        try:
            Card.objects.create(description=description, max=max, vendor=vendor, type=type)
            return redirect(reverse('saved'))
        except:
            context = {'error_message': 'unknown error has occurred'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# This will return a template and a list of cards to the vendor
class VendorsCardsAPI(APIView):
    def get(self, request):
        vendor = VendorUser.objects.get(id=request.user.id).vendor
        cards = Card.objects.all().filter(vendor=vendor)
        serializer = SingleCardSerializer(cards, many=True)
        return render_to_response('loyali/vendor_pages/view_cards.html', {"cards": serializer.data})


@login_required
def add_admin_user(request):
    if request.method == 'POST':
        raw_data = request.POST.copy()
        user = User.objects.create_user(data=raw_data)
        if user:
            group = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)[0]
            group.user_set(user)
        else:
            return HttpResponse(status=status.HTTP_409_CONFLICT)
    elif request.method == 'GET':
        template = loader.get_template('loyali/add_user.html')
        context = {
            'add_user': 'add_user'
        }
        return HttpResponse(template.render(context, request))


def vendor_customers(request):
    if request.method == 'GET':
        template = loader.get_template('loyali/vendor_pages/vendor_customers.html')
        vendor = VendorUser.objects.get(id=request.user.id)
        subscriptions = Subscription.objects.all().filter(vendor=vendor)
        serializer = SubscribedCustomersSerializer(subscriptions, many=True).data
        context = {'customers': serializer}
        return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('loyali/login.html')
    context = {'login': "login"}
    context.update(csrf(request))
    if request.user.is_authenticated():
        return __redirect_after_login(request.user)
    return HttpResponse(template.render(context, request))


# Displays the contact us page
def contact_us(request):
    template = loader.get_template('loyali/contact.html')
    context = {'contact': "contact"}
    return HttpResponse(template.render(context, request))


# Admin - Admin main menu
@login_required
def admin_main(request):
    template = loader.get_template('loyali/admin_main_menu.html')
    context = {'menu': "menu"}
    return HttpResponse(template.render(context, request))


# Admin - Adds a new Vendor
@login_required
# Shows the Add Vendor Page
def vendor_add(request):
    template = loader.get_template('loyali/add_vendor.html')
    context = {'login': "login"}
    return HttpResponse(template.render(context, request))


# Vendor - Vendor main menu
@login_required
def vendor_main(request):
    template = loader.get_template('loyali/vendor_pages/vendor_main_menu.html')
    context = {'menu': "menu"}
    return HttpResponse(template.render(context, request))


# Handles the user logout request
def logout(req):
    if req.user.is_authenticated():
        auth.logout(req)
        return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))


@login_required
def view_vendors(request):
    template = loader.get_template('loyali/all_vendors.html')
    context = {
        'vendors': "view_vendors"
    }
    return HttpResponse(template.render(context, request))


@login_required
def admin_user_page(request):
    template = loader.get_template('loyali/add_user.html')
    context = {
        'admin_user': "admin_users"
    }
    return HttpResponse(template.render(context, request))


@login_required
def saved_page(request):
    template = loader.get_template('loyali/saved.html')
    context = {
        'saved': "aved"
    }
    return HttpResponse(template.render(context, request))


@login_required
def redirect_to_main(request):
    if request.method == "GET":
        return __redirect_after_login(request.user)



@login_required
def view_users_page(request):
    template = loader.get_template('loyali/view_users.html')
    context = {
        'users': "users"
    }
    return HttpResponse(template.render(context, request))


@login_required
def full_vendors_page(request):
    template = loader.get_template('loyali/vendor_list.html')
    context = {
        'vendors': "full_vendor_list"
    }
    return HttpResponse(template.render(context, request))
