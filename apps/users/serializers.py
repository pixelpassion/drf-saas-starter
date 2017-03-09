import django.contrib.auth.password_validation as validators
from rest_framework import serializers

from .models import User


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
