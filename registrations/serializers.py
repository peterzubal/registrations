from rest_framework import serializers
from mongoengine import fields as me_fields
from .models import Student

class StudentSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=300)
    date_of_birth = serializers.DateField()
    phone_number = serializers.CharField(max_length=20)
    disabilities = serializers.CharField(allow_blank=True)
    password = serializers.CharField()

    def create(self, validated_data):
        return Student(**validated_data)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.disabilities = validated_data.get('disabilities', instance.disabilities)
        instance.save()
        return instance
