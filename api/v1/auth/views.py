from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from .custom_permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication





class SignUpView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        serializer = SignUpSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {'message': 'OTP has been send to your email.'},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data
        serializer = VerifyOTPSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response(
                {'message': 'Your email has been verified!'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResendOtp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        serializer = ResendOtpSerializer(data=data)
        if serializer.is_valid():
            return Response(
                {'message': 'OTP has been send to your email.'},
                status=status.HTTP_200_OK
            ) 
        
        return Response(
            {'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny, IsVerified]

    def post(self, request):
        data = request.data
        serializer = LogInSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response({'message': serializer.errors})


class ForgetPassword(APIView):
    permission_classes = [AllowAny, IsVerified]

    def post(self, request):
        data = request.data
        serializer = ForgetPasswordSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            # return Response({'message': 'Password changed succesfully!'})
            return Response(
                {'message': 'OTP has been send to your email.'},
                status=status.HTTP_200_OK
            )
        
        return Response({'message': serializer.errors})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            return Response({'message': 'Password changed successfully!'})

        return Response({'message': serializer.errors})


class AddProfile(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        data = request.data
        serializer = UpdateProfileSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            return Response({'message': "profile updated successfully!"})

        return Response(serializer.errors)


class EditProfile(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = UpdateProfileSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.get(email=self.request.user.email)
        return queryset
    
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {'message': 'Profile updated successfully!'}
        return Response(response_data)   


class ChangeEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):

        data = request.data
        print(request.user)
        serializer = ChangeEmailSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response({'message': 'OTP has been send to your email!'})
        
        return Response(serializer.errors)
    

class ChangeEmailVerification(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        data = request.data
        serializer = VerifyOTPSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response({'message': 'Email updated successfully!'})
        return Response(serializer.errors)
    

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response({'message': 'password changed successfully!'})
        return Response(serializer.errors)