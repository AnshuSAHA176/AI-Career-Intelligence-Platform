from rest_framework import serializers
from .models import User,Profile
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    def validate(self, attrs):
        user=authenticate(email=attrs["email"],password=attrs['password'])
        if user!=None:
            attrs['user']=user
            return attrs
        else :
            raise serializers.ValidationError( "Invalid email or password")
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['education',
                'college',
                'graduation_year',
                'github_url',
                'linkedin_url',
                'target_role',
                'experience_level',
                'bio']

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile"
        ]