from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import VendorUser, Subscription, Card, Vendor, CardsInUse
from loyaliapi.serializer import MobileUserSerializer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['store_name', 'location', 'store_type', 'logo_title', 'phone']

    def to_representation(self, instance):
        representation = {
            "store_name": instance.store_name,
            "location": instance.location,
            "store_type": instance.store_type,
            "phone": instance.phone,
            "logo_title": instance.logo_title.name
        }
        return representation


class VendorUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'vendor_id']

    def create(self, validated_data):
        vendor = Vendor.objects.get(id=self.initial_data['vendor_id'])
        user = VendorUser.objects.create_user(username=validated_data['username'],
                                              email=validated_data['email'],
                                              password=validated_data['password'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              vendor=vendor)
        return user

    def to_representation(self, instance):
        representation = {
            "username": instance.username,
            "first_name": instance.first_name
        }
        return representation


class VendorUserSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    class Meta:
        model = VendorUser
        fields = ['id', 'vendor']


class VendorCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['description', 'max', 'vendor']


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['vendor', 'customer']


class VendorSubscriptionSerializer(serializers.ModelSerializer):
    vendor = VendorUserSerializer()

    class Meta:
        model = Subscription
        fields = ['vendor']


class CustomerSubscriptionSerializer(serializers.ModelSerializer):
    customer = MobileUserSerializer()

    class Meta:
        model = Subscription
        fields = ['customer']


class CardSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Card
        fields = ['vendor', 'description', 'max']


class CardsInUseSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = CardsInUse
        fields = ['id', 'card', 'current']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class AdminUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'groups']
