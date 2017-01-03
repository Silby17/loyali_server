from rest_framework import serializers
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
