from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

import django.contrib.auth.password_validation as validators
from django.core import exceptions

from .models import User

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.utils import get_username_max_length
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


class OldCreateUserSerializer(serializers.ModelSerializer):
    """Serialize data from the User."""

    class Meta:
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
        """Call create_user on user object. Without this the password will be stored in plain text."""

        user = User.objects.create_user(**validated_data)

        return user


################


class UserSerializer(serializers.ModelSerializer):
    """Serialize data from the User."""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', )
        read_only_fields = ('is_active', 'activation_token', )


class ActivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'activation_token', 'is_active')


class ResetPasswordSerializer(serializers.ModelSerializer):

    def validate_password(self, data):
        """initial_data has to be converted to an object for UserAttributeSimilarityValidator."""
        user = self.initial_data
        validators.validate_password(password=data, user=user)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        read_only_fields = ('email',)
        extra_kwargs = {'password': {'write_only': True}}


# class ChangePasswordSerializer(serializers.ModelSerializer):
#
#     def validate_password(self, data):
#         """initial_data has to be converted to an object for UserAttributeSimilarityValidator."""
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
        """initial_data has to be converted to an object for UserAttributeSimilarityValidator."""
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


class CreateUserSerializer(RegisterSerializer):
    """Overwrite the register_auth RegisterSerializer to enable first_name and last_name."""
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.clean_password(self.cleaned_data['password1'], user)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
