from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'is_staff',
            'email',

            # FIX FOR PROBLEM #3 - A3:2017 Sensitive Data Exposure
            # Obviously you wouldn't want to expose private information, like
            # full name, date of birth, or the phone number of a user,
            # so the fix is to remove it from the API; in this case
            # just remove it from this serializer's fields list.
            'date_of_birth',
            'phone_number',
        )