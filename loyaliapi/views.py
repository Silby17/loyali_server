import datetime
from django.contrib import auth
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from loyali.models import VendorUser, Subscription, Card, CardsInUse, Vendor, Purchase
from loyali.serializer import VendorSerializer, VendorWithCardsSerializer,\
    CardsInUseSerializer, SubscriptionsSerializerWithCardsInUse
from loyaliapi.models import MobileUser
from loyaliapi.serializer import MobileUserModelSerializer, PurchaseSerializer

CUSTOMER_GROUP_NAME = 'Customer'
ADMIN_GROUP_NAME = 'Admin'
QR_BARCODE = "Testing LOYALI"


# Creates a Mobile User
class MobileUserAPI(GenericAPIView):
    queryset = MobileUser.objects.all()
    serializer_class = MobileUserModelSerializer

    def post(self, request, *args, **kwargs):
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
                return Response(context, status=status.HTTP_200_OK)
            else:
                errors = ""
                serializer_errors = serializer.erros
                for error in serializer_errors:
                    errors += serializer_errors[error][0]


# This function will allow mobile users to log in to the app
class CheckUserCredentialsAPI(APIView):
    parser_classes = ([FormParser, MultiPartParser])

    def post(self, request):
        raw_data = request.POST.copy()
        username = raw_data.get('username')
        password = raw_data.get('password')
        try:
            # Checks if the user exists
            user = MobileUser.objects.get(username=username)
            auth_user = auth.authenticate(username=username, password=password)
            if auth_user is not None:
                print 'Mobile User:', username, ' - has logged in'
                user_result = {'username': username,
                           'id': auth_user.id}
                context = {'user_result': user_result}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except MobileUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# This will create a new subscription between a customer and vendor
class AddSubscriptionAPI(APIView):
    def post(self, request):
        print 'Creating new Subscription'
        try:
            data = request.data
            vendor_id = data.get('vendor_id')
            customer_id = data.get('customer_id')
            try:
                # Gets the Vendor from the DB
                vendor = Vendor.objects.get(id=vendor_id)
                # Gets the VendorUser by vendor
                vendor_user = VendorUser.objects.get(vendor=vendor)
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
                subscription = Subscription.objects.get(vendor=vendor_user, customer=customer_id)
                context = {'message': 'Subscription already exists'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except:
                # Creates a subscription between Customer and Vendor
                Subscription.objects.create(vendor=vendor_user, customer=mobile_user)
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


# Delete Subscription
class DeleteSubscriptionAPI(APIView):
    def post(self, request):
        data = request.POST.copy()
        customer_id = data.get('customer_id')
        vendor_id = data.get('vendor_id')

        # Gets all the Customers Cards in Use
        customer_cards_in_use = CardsInUse.objects.all().filter(customer=customer_id)
        # Gets all the ID's of the Cards of the Vendor
        card_ids = Card.objects.all().filter(vendor__id=vendor_id).values_list('id', flat=True)
        # Deletes the seSubscription
        vendor = Vendor.objects.all().filter(id=vendor_id)[:1].get()
        vendor_user = VendorUser.objects.all().filter(vendor=vendor)
        Subscription.objects.all().filter(customer=customer_id, vendor=vendor_user).delete()
        # Run through the list of cards and delete them from the DB
        for card_ID in card_ids:
            customer_cards_in_use.filter(customer=customer_id, card__id=card_ID).delete()

        return Response(status=status.HTTP_200_OK)


# Method to Punch the current Users Card
class PunchCardAPI(APIView):
    def post(self, request):
        raw_data = request.POST.copy()
        customer_id = raw_data.get('customer_id')
        barcode = raw_data.get('barcode')
        card_id = raw_data.get('card_id')
        print 'Customer_id: ', customer_id, ' Barcode: ', barcode, ' card_id: ', card_id
        # Checks if the QR Code that is scanned is Valid
        if barcode != QR_BARCODE:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            # Checks to see that the Customer Exists
            customer = MobileUser.objects.get(id=customer_id) # Object
            try:
                card_in_use = CardsInUse.objects.get(id=card_id)
                # Checks to see if the user has reached their free Item
                if (card_in_use.current + 1) is card_in_use.card.max:
                    card = Card.objects.get(id=card_in_use.card.id)  # Object
                    # Creates a new Card
                    CardsInUse.objects.create(customer=customer, card=card, current=0)
                    CardsInUse.objects.all().filter(id=card_id).delete()  # Deletes the Card
                    context = {'message': 'Congratulations, you get your free item!'}
                    # 202 is the code that will code that will show FREE COFFEE
                    return Response(context, status=status.HTTP_202_ACCEPTED)
                card_in_use.current += 1
                card_in_use.save()
                context = {'message': "Punched!"}
                return Response(context, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


# GET Specific vendor for user by ID
class VendorByIdAPI(APIView):
    def post(self, request):
        raw_data = request.POST.copy()
        vendor_id = raw_data.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)
        serializer = VendorSerializer(vendor)
        context = {'vendor': serializer.data}
        return Response(context, status=status.HTTP_200_OK)


# GET a list of ALL Vendors and their associated Cards
class VendorsWithCardsAPI(APIView):
    def get(self, request):
        vendor_users = VendorUser.objects.values_list('vendor', flat=True)
        vendors = Vendor.objects.filter(id__in=vendor_users)
        serializer = VendorWithCardsSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Gets a list of Card In Use of a specific Customer
class CustomersCardsAPI(APIView):
    def post(self, request):
        raw_data = request.POST.copy()
        customer_id = raw_data.get('customer_id')
        customer = MobileUser.objects.get(id=customer_id)
        customers_cards = CardsInUse.objects.all().filter(customer=customer)
        serializer = CardsInUseSerializer(customers_cards, many=True)
        print serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)


# GETS a list of all the Customers Subscriptions and current Card Status
class AllCustomersSubscriptionsAPI(APIView):
    def get(self, request):
        raw_data = request.GET.copy()
        customer_id = raw_data.get('customer_id')
        try:
            mobile_user = MobileUser.objects.get(id=customer_id)
            subscriptions = Subscription.objects.all().filter(customer=mobile_user)
            # Creates a JSON with a list of all Subscriptions and card status
            serializer = SubscriptionsSerializerWithCardsInUse(subscriptions, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


# GET a single Subscription with the Current Card Details
class SingleSubscriptionAPI(APIView):
    def get(self, request):
        raw_data = request.GET.copy()
        customer_id = raw_data.get('customer_id')
        vendor_id = raw_data.get('vendor_id')
        # Gets the Vendor as an Object
        vendor = Vendor.objects.all().filter(id=vendor_id)[:1].get()
        # Gets the VendorUser
        vendor_user = VendorUser.objects.all().filter(vendor=vendor)
        subscriptions = Subscription.objects.all().filter(customer__id=customer_id, vendor=vendor_user)
        serializer = SubscriptionsSerializerWithCardsInUse(subscriptions, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class TestingAPI(APIView):
    serializer_class = PurchaseSerializer

    def post(self, request):
        raw_data = request.POST.copy()
        customer_id = raw_data.get('customer_id')
        vendor_id = raw_data.get('vendor_id')
        vendor = Vendor.objects.all().filter(id=vendor_id)[:1].get()
        customer = MobileUser.objects.all().filter(id=customer_id)[:1].get()
        now = datetime.datetime.now()
        type = raw_data.get('type') # Coffee or Pastry
        purchase = Purchase(vendor=vendor, customer=customer, date=now,
                            type=type).save()
        return Response(status=status.HTTP_200_OK)

