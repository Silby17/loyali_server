from django.contrib.auth.models import Group, User
from rest_framework import serializers
from loyaliapi.models import MobileUser
from .models import VendorUser, Subscription, Card, Vendor, CardsInUse, Rewards
from loyaliapi.serializer import MobileUserSerializer, MobileUserFirstNameSerialize


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'location', 'store_type', 'logo_title', 'phone']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "store_name": instance.store_name,
            "location": instance.location,
            "store_type": instance.store_type,
            "phone": instance.phone,
            "logo_title": instance.logo_title.url
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
        fields = ['vendor', 'description', 'max', 'type']


class SingleCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'description', 'max', 'type']

    def to_representation(self, instance):
        representation = {
            "description": instance.description,
            "max": instance.max,
            "type": instance.type
        }
        return representation


class CardsInUseSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = CardsInUse
        fields = ['id', 'card', 'current']


class CardsInUseSerializerWithCardDetails(serializers.ModelSerializer):
    card = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CardsInUse
        fields = ['id', 'card', 'current']

    def get_card(self, obj):
        return {'id': obj.card.id, 'description': obj.card.description,
                'max': obj.card.max, 'type': obj.card.type}


class VendorWithCardsSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'location', 'store_type', 'logo_title', 'phone', 'cards']

    def get_cards(self, obj):
        cards = obj.cards
        cards_data = cards.values('id', 'max', 'description')
        return cards_data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class AdminUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'groups']


class SubscribedCustomersSerializer(serializers.ModelSerializer):
    customer = MobileUserFirstNameSerialize()

    class Meta:
        model = Subscription
        fields = ['customer']


class SubscriptionsSerializerWithCardsInUse(serializers.ModelSerializer):
    vendor_user_id = serializers.PrimaryKeyRelatedField(source='vendor', read_only=True)
    vendor = VendorSerializer(source='vendor.vendor', read_only=True)
    cards_in_use = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['vendor_user_id', 'vendor', 'cards_in_use']

    def get_cards_in_use(self, obj):
        cards_in_use = CardsInUse.objects.filter(customer=obj.customer, card__vendor=obj.vendor.vendor)
        return CardsInUseSerializerWithCardDetails(cards_in_use, many=True).data


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


class CustomerRewardSerializer(serializers.ModelSerializer):
    rewards = serializers.SerializerMethodField()

    class Meta:
        model = MobileUser
        fields = ['first_name', 'last_name', 'id', 'rewards']

    def get_rewards(self, obj):
        customer_rewards = self.context.get("customer_rewards")
        return RewardSerializer(customer_rewards[obj.id], many=True).data