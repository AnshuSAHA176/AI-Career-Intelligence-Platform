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


class UserDashBordSerializer(serializers.Serializer):
    name=serializers.CharField()
    target_role=serializers.CharField()


class ResumeDashBordSerializer(serializers.Serializer):
    title=serializers.CharField()
    score=serializers.IntegerField()
    primary_role=serializers.CharField()
    uploaded_at=serializers.DateTimeField()



class SkillSummarySerializer(serializers.Serializer):
    found = serializers.IntegerField()
    missing = serializers.IntegerField()


class JobStaticsDashBordSerializer(serializers.Serializer):
    saved=serializers.IntegerField()
    applied=serializers.IntegerField()
    interview=serializers.IntegerField()
    offer=serializers.IntegerField()
    accepted=serializers.IntegerField()
    rejected=serializers.IntegerField()
    withdrawn=serializers.IntegerField()


class ActivitySerializer(serializers.Serializer):
    job = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

class DashboardSerializer(serializers.Serializer):
    user=UserDashBordSerializer()
    resume=ResumeDashBordSerializer()
    job_statistics=JobStaticsDashBordSerializer()
    skills=SkillSummarySerializer()
    recommended_jobs=serializers.IntegerField()
    recent_activity=ActivitySerializer(many=True)
