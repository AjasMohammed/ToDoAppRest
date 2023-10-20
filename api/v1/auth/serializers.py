from home.models import CustomUser
from rest_framework import serializers
from .emails import send_otp_via_email
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=10, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_verified']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )

        user.generate_otp
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, default=None)
    otp = serializers.CharField(max_length=4)

    def validate(self, validated_data):
        email = validated_data['email']
        if not email:
            email = self.context.get('request').user.email
        otp = validated_data['otp']
        try:
            print(email, otp)
            user = CustomUser.objects.get(email=email)
            print(user)

            if user.otp == "" or user.otp == None:
                raise serializers.ValidationError('OTP not found, try resending the OTP!')
            if str(user.otp) != str(otp):
                raise serializers.ValidationError('Invalid OTP, Try Again!')
            # elif user.reset_otp and str(user.reset_otp) != str(otp):
            #     raise serializers.ValidationError('Invalid OTP, Try Again!')
            
            elif user.otp_expiry < timezone.now():  # Checks if the otp expired
                raise serializers.ValidationError('OTP expired. try resending the OTP!')

            if not user.is_verified:
                user.is_verified = True
            elif user.new_email != '' or user.new_email != None:
                user.email = user.new_email
                user.new_email = None
            else:
                user.password_reset = True
                
            user.otp = None
            user.otp_expiry = None
            user.save()

            return validated_data
        
        except Exception as e:
            raise serializers.ValidationError(e)


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, validated_data):
        try:
            user = CustomUser.objects.get(email=validated_data['email'])

            user_data = {
                'email': validated_data['email'],
                'password': validated_data['password']
            }
            auth_user = authenticate(**user_data)
            if not auth_user:
                raise serializers.ValidationError('Invalid Credentials!')
            
            tokens = TokenObtainPairSerializer.get_token(auth_user)

            data = {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            }
            return data
         
        except Exception as e:
            raise serializers.ValidationError(e)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
            # subject = "ToDoApp Password reset verification"
            # send_otp_via_email(email, user, subject)
            user.generate_otp
        except Exception as e:
            raise serializers.ValidationError(e)
        return attrs
    

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    new_password = serializers.CharField(max_length=10)
    old_password = serializers.CharField(max_length=10, required=False)

    def validate(self, attrs):
        email = attrs.get('email', None)
        new_password = attrs.get('new_password', '')
        old_password = attrs.get('old_password', '')
        try:
            if not email:
                email = self.context.get('request').user.email

                user = CustomUser.objects.get(email=email)
                if not user.check_password(old_password):
                    raise serializers.ValidationError('user password is wrong!')
                user.set_password(new_password)
                user.save()
            else:
                user = CustomUser.objects.get(email=email)
                if user.password_reset:
                    user.set_password(new_password)
                    user.password_reset = False
                    user.save()
                    return attrs
                raise serializers.ValidationError("Not Authorised")
        except Exception as e:
            raise serializers.ValidationError(e)
        

class UpdateProfileSerializer(serializers.Serializer):
    fname = serializers.CharField(required=False)
    lname = serializers.CharField(required=False)
    dob = serializers.DateField(required=False)
    profile_pic = serializers.ImageField(required=False)


    def validate(self, attrs):
        
        user = self.context.get('request').user
        email = user.email
        f_name = attrs.get('fname', None)
        l_name = attrs.get('lname', None)
        dob = attrs.get('dob', None)
        profile_pic = attrs.get('profile_pic', None)

        try:
            user = CustomUser.objects.get(email=email)
            if f_name:
                user.first_name = f_name
            if l_name:
                user.last_name = l_name
            if dob:
                dob = parse_date(str(dob))

                user.dob = dob
            if profile_pic:
                user.profile_pic = profile_pic
            
            user.save()
            return attrs
        
        except Exception as e:
            raise serializers.ValidationError(e)


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        current_user = self.context.get('request').user
        user = CustomUser.objects.get(email=current_user.email)
        new_email = attrs.get('email', None)

        if new_email:
            user.new_email = new_email
            # subject = 'ToDoApp Email Change Verification'
            # send_otp_via_email(new_email, user, subject)
            user.generate_otp
        
            return attrs
        raise serializers.ValidationError('Invalid Email!')


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_otp
        except Exception as e:
            raise serializers.ValidationError(e)
        return super().validate(attrs)