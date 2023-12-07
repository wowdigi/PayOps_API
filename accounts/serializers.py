from django.db.models import fields
from rest_framework import serializers
from .models import CustomUser, Transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'username', 'last_name', 'email', 'transaction_Pin', 'organisation', 'user_url',
        ]

    def create(self, validated_data):
        # user = CustomUser.objects.get(
        #     username=validated_data['username'])
        # if user.username == validated_data['username']:
        #     user = CustomUser.objects.create_user(
        #         # id=int(validated_data['id']),
        #         username=validated_data['username'],
        #         first_name=validated_data['first_name'],
        #         last_name=validated_data['last_name'],
        #         email=validated_data['email'],
        #         transaction_Pin=validated_data['transaction_Pin'],
        #         user_url=validated_data['user_url'],
        #         # organisation=int(validated_data['organisation']),
        #     )
        #     user.set_password(validated_data['email'])
        #     user.save()

        user = CustomUser.objects.get_or_create(username=validated_data['username'], defaults={
            'email': validated_data['email'], 'transaction_Pin': validated_data['transaction_Pin'], 'user_url': validated_data['user_url'],

        })
        
        return Response({
                    "status": "OK",
                    "url": "https://pay.geekops.co/pay",
                    },
                    status=status.HTTP_200_OK)

        # else:
        #     return user


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transactions_Status', 'transaction_Date',
                  'cutomer__customer_Id', 'transaction_Amount']
