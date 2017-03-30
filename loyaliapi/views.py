from django.contrib import auth
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from loyali.models import VendorUser, Subscription, Card, CardsInUse
from loyaliapi.models import MobileUser
from loyaliapi.serializer import MobileUserModelSerializer

CUSTOMER_GROUP_NAME = 'customer'
ADMIN_GROUP_NAME = 'admin'


class MobileUserAPI(GenericAPIView):
    queryset = MobileUser.objects.all()
    serializer_class = MobileUserModelSerializer

    def post(self, request, *args, **kwargs):
        context = {}
        raw_data = request.POST.copy()
        username = raw_data.get('username')

        try:
            customer_user = MobileUser.objects.get(username=username)
            context = {"message": "user already exists"}
            return Response(context, status=status.HTTP_409_CONFLICT)
        except:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                group = Group.objects.get_or_create(name=CUSTOMER_GROUP_NAME)[0]
                group.user_set.add(user)
                context = {"user_result": serializer.data}
                print context
                return Response(context, status=status.HTTP_200_OK)
            else:
                errors = ""
                serializer_errors = serializer.erros
                for error in serializer_errors:
                    errors += serializer_errors[error][0]


# This function will allow mobile users to log in to the app
class CheckUserCredentials(APIView):
    parser_classes = ([FormParser, MultiPartParser])

    def post(self, request):
        context = {}
        raw_data = request.POST.copy()
        email = raw_data.get('email')
        password = raw_data.get('password')
        try:
            # Checks if the user exists
            user = MobileUser.objects.get(username=email)
            auth_user = auth.authenticate(username=email, password=password)
            if auth_user is not None:
                print 'Mobile User:', email, ' - has logged in'
                context = {'username': email,
                           'id': auth_user.id}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except MobileUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# This will create a new subscription between a customer and vendor
class AddSubscription(APIView):
    def post(self, request):
        context = {}
        try:
            data = request.data
            vendor_id = data.get('vendor_id')
            customer_id = data.get('customer_id')
            try:
                # Gets the VendorUser from the DB
                vendor_user = VendorUser.objects.get(id=vendor_id)
            except:
                context = {'message': 'Invalid Vendor ID'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Gets the Customer from the DB
                mobile_user = MobileUser.objects.get(id=customer_id)
            except:
                context = {'message': 'Invalid Customer ID'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Checks to see if the Subscription already exists
                subscription = Subscription.objects.get(vendor=vendor_id, customer=customer_id)
                context = {'message': 'Subscription already exists'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except:
                # Creates a subscription between Customer and Vendor
                new_subscription = Subscription.objects.create(vendor=vendor_user, customer=mobile_user)
                # Get all the cards of the Vendor
                vendor_cards = Card.objects.filter(vendor=vendor_user.vendor)
                # Assign the User the Cards
                for card in vendor_cards:
                    CardsInUse.objects.create(customer=mobile_user, card=card, current=0)
                context = {'message': 'Subscription Created successfully'}
                return Response(context, status=status.HTTP_200_OK)
        except:
            context = {'message': 'Unknown error occurred'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)