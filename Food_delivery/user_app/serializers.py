from rest_framework import serializers,exceptions
from user_app.models import Account
from rest_framework.response import Response


PASSWORD_LENGTH=8




class UserRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['id','name','phone_number','email','date_of_birth','profile_picture','password','password2']
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    
    def get_profile_image_url(self, obj):
        return obj.profile_picture.url
    
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        print(password)
        return instance
    
    def save(self):
        reg = Account(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            date_of_birth=self.validated_data['date_of_birth'],
            name=self.validated_data['name'],
            profile_picture=self.validated_data['profile_picture'],
        )
        if Account.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error':'phone number already registered!!'})
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'password does not match!!'})
        reg.set_password(password)
        reg.save()
        print(password)
        return reg




class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True,required=True)
    password2 =serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=Account
        fields=('old_password','password','password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password not match"})
        return attrs
    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"old password is incorrect"})
        return value
    def update(self,instance,validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class RegisterWithEmailSerializer(serializers.Serializer):
     email = serializers.EmailField(max_length=50, min_length=5)
     password = serializers.CharField(min_length=8, max_length=30)

     def validate_password(self, password):
        if not any(ch.isdigit() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain digit.')
        if not any(ch.isalpha() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain alpha.')
        if len(password) < PASSWORD_LENGTH:
            raise exceptions.ValidationError(detail='Password must be more than 8 character.')

     class Meta:
        model = Account
        fields = (
            'password', 'email',)

