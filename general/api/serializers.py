from rest_framework import serializers
from general.models import User, Profile, Announcement
from rest_framework.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user', )
    
    def update(self, instance, validated_data):
        if(validated_data['meta_key'] == 'vatNumber'):
            raise ValidationError("vatNumber should not be changed.")
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True, source='get_profile')
    class Meta:
        model = User
        fields = ('id', 'username', 'profile', 'last_login', 'role', 'date_joined')
        depth = 1
    
    def create(self, validated_data):
        profile_data = validated_data.pop('get_profile')
        user = User.objects.create(**validated_data) # TODO: check role
        for item in profile_data:
            item['user'] = user
            Profile.objects.create(**item)
        return user
        
    def to_internal_value(self, data):
        profile_data = data.pop('profile')
        data['profile'] = [{'meta_key': key, 'meta_value':value} for key, value in profile_data.items()]
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profiles = data.pop('profile')
        temp = {}
        for profile in profiles:
            key = profile['meta_key']
            value = profile['meta_value']
            temp[key] = value
        data['profile'] = temp
        return data
        

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    class Meta:
        model = User
        fields = ['username','password','email','role', 'profile']
        required = ['username', 'password', 'email', 'role']
        
    extra_kwargs = {
        'password' : {'write_only': True}
    }
    
    def create(self, validated_data):
        
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        
        profile_data = validated_data.pop('profile')
        for item in profile_data:
            item['user'] = user
            Profile.objects.create(**item)
        return user
    
    
    def to_internal_value(self, data):
        profile_data = data.pop('profile')
        data['profile'] = [{'meta_key': key, 'meta_value':value} for key, value in profile_data.items()]
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profiles = data.pop('profile')
        temp = {}
        for profile in profiles:
            key = profile['meta_key']
            value = profile['meta_value']
            temp[key] = value
        data['profile'] = temp
        return data
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        
class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
class PasswordForgorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
