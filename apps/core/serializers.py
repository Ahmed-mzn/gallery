from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Plan, User, Role, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'price')


class UserSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'plan', 'plan_status', 'plan_end_date')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=45, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'role')

    def validate_role(self, value):
        try:
            Role.objects.get(id=value)
            return value
        except:
            raise ValidationError(f"Role doesn't exist")

    def validate_email(self, value):
        email_exists = User.objects.filter(email=value).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return value

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop("password")
        role = validated_data.pop('role')
        user = super().create(validated_data)
        user.set_password(password)
        user.username = user.email
        user.save()

        UserRole.objects.create(user=user, role_id=role)
        return user
