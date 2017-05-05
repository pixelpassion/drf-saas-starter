from rest_framework import serializers

import django.contrib.auth.password_validation as validators
from django.core import exceptions

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Serialize data from the User """

    class Meta:
        """ """
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', 'password')
        read_only_fields = ('is_active', 'activation_token')

        extra_kwargs = {
            'password': {'write_only': True, 'help_text': 'Password of the user'},
        }

    def validate(self, data):

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateUserSerializer, self).validate(data)

    def create(self, validated_data):
        """call create_user on user object. Without this the password will be stored in plain text."""

        user = User.objects.create_user(**validated_data)

        return user




################


class UserSerializer(serializers.ModelSerializer):
    """Serialize data from the User """

    class Meta:
        """ """
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', )
        read_only_fields = ('is_active', 'activation_token' )


class ActivateUserSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = User
        fields = ('id', 'activation_token', 'is_active')


class ResetPasswordSerializer(serializers.ModelSerializer):
    """ """

    def validate_password(self, data):
        """initial_data has to be converted to an object for UserAttributeSimilarityValidator"""
        user = self.initial_data
        validators.validate_password(password=data, user=user)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        read_only_fields = ('email',)
        extra_kwargs = {'password': {'write_only': True}}


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     """ """
#
#     def validate_password(self, data):
#         """initial_data has to be converted to an object for UserAttributeSimilarityValidator"""
#         user = self.initial_data
#         validators.validate_password(password=data, user=user)
#
#     class Meta:
#         model = User
#         fields = ('password', )
#         read_only_fields = ('password',)
#         extra_kwargs = {'new_password': {'write_only': True}}


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})

    def validate_new_password(self, data):
        """initial_data has to be converted to an object for UserAttributeSimilarityValidator"""
        user = self.initial_data
        validators.validate_password(password=data, user=user)


class CurrentPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {
        'invalid_password': 'The password is invalid'
    }

    def __init__(self, *args, **kwargs):
        super(CurrentPasswordSerializer, self).__init__(*args, **kwargs)

    def validate_old_password(self, value):
        user = self.initial_data
        print(user)
        if not self.context.get("request").user.check_password(value):
            raise serializers.ValidationError(self.error_messages['invalid_password'])
        return value


class ChangePasswordSerializer(PasswordSerializer, CurrentPasswordSerializer):
    pass
