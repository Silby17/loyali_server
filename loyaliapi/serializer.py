from rest_framework import serializers
from loyali.models import Rewards, Vendor, Purchase
from .models import MobileUser


class MobileUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password',
                  'facebook_id', 'push_api_key', 'subscriptions']

    def create(self, validated_data):
        user = MobileUser.objects.create_user(username=validated_data['username'],
                                              email=validated_data['email'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              password=validated_data['password'],
                                              facebook_id=validated_data['facebook_id'],
                                              push_api_key=validated_data['push_api_key'])
        return user

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "username": instance.username
        }
        return representation


class MobileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ['first_name', 'last_name', 'id']

    def to_representation(self, instance):
        representation = {
            "first_name": instance.first_name,
            "last_name": instance.last_name
        }
        return representation


class MobileUserFirstNameSerialize(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ['first_name', 'last_name', 'id', 'username']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "full_name": instance.first_name + ' ' + instance.last_name,
            "username": instance.username
        }
        return representation


class MobileUserFullNameSerialize(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ['first_name', 'last_name', 'id', 'username']

    def to_representation(self, instance):
        representation = {
            "full_name": instance.first_name + ' ' + instance.last_name
        }
        return representation


class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rewards
        fields = ['id', 'amount', 'type']


class VendorRewardSerializer(serializers.ModelSerializer):
    rewards = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'location', 'store_type', 'logo_title', 'phone',
                  'rewards']

    def get_rewards(self, obj):
        vendor_rewards = self.context.get("vendor_rewards")
        return RewardSerializer(vendor_rewards[obj.id], many=True).data


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'location', 'store_type', 'logo_title', 'phone']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "store_name": instance.store_name,
            "logo_title": instance.logo_title.url
        }
        return representation


def get_formatted_date(obj):
    return obj.date.strftime("%d %b %Y")


class AllCustomersPurchasesSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('get_formatted_date')
    vendor = VendorSerializer()

    class Meta:
        model = Purchase
        fields = ['vendor', 'type', 'date']
