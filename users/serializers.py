from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .validators import (
    password_validator,
    password_pattern,
    username_validator,
)

# 회원가입
class SignupSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(
        error_messages={
            "required": "비밀번호를 입력해주세요.",
            "blank": "비밀번호를 입력해주세요.",
            "write_only": True,
        }
    )
    class Meta:
        model = User
        fields = (
            "userNameLoc",
            "telNo",
            "email",
            "password",
            "repassword",
        )
        extra_kwrags = {
            "userNameLoc": {
                "error_messages":{
                    "required": "아이디를 입력해주세요.",
                    "blank": "아이디를 입력해주세요."
                }
            },
            "password": {
                "write_only": True,
                "error_messages":{
                    "required": "비밀번호를 입력해주세요.",
                    "blank": "비밀번호를 입력해주세요."
                }
            },
            "email":{
                "error_messages":{
                    "required": "이메일을 입력해주세요.",
                    "blank": "이메일을 입력해주세요.",
                    "invalid": "알맞은 형식의 이메일을 입력해주세요."
                }
            },
            "telNo": {
                "error_messages":{
                    "required": "전화번호를 입력해주세요.",
                }
            }
        }
        
    def validate(self, data):
        userNameLoc = data.get("userNameLoc")
        telNo = data.get("telNo")
        password = data.get("password")
        repassword = data.get("repassword")
        
        # 아이디 유효성 검사
        if username_validator(userNameLoc):
            raise serializers.ValidationError(detail={"아이디는 6자 이상 20자 이하의 숫자, 영문 대/소문자 이어야 합니다."})

        # 비밀번호 일치
        if password != repassword:
            raise serializers.ValidationError(detail={"password": "비밀번호가 일치하지 않습니다."})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상 16자이하의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다. "})

        # 비밀번호 동일여부 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 3자리 이상 동일한 영문,숫자,특수문자 사용 불가합니다. "})

        # 휴대폰 번호 존재여부와 blank 허용
        if (User.objects.filter(telNo=telNo).exists() and not telNo == ""):
            raise serializers.ValidationError(detail={"telNo": "이미 사용중인 휴대폰 번호입니다."})

        return data
    
    def create(self, validated_data):
        userNameLoc = validated_data["userNameLoc"]
        email = validated_data["email"]
        telNo = validated_data["telNo"]

        user = User(
            userNameLoc=userNameLoc,
            telNo=telNo,
            email=email,
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token["email"] = user.email
        token["userNameLoc"] = user.userNameLoc
        return token
    

# 회원정보 수정
class UserdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("userNameLoc", "email", "telNo")
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "이메일을 입력해주세요.",
                    "invalid": "알맞은 형식의 이메일을 입력해주세요.",
                    "blank": "이메일을 입력해주세요."
                }
            },
            "telNo" : {
              "error_messages":{
                  "required":"휴대폰 번호를 입력해주세요."
              }  
            }
        }
    
    def validate(self, data):
        telNo = data.get("telNo")
        current_phone_number = self.context.get("request").user.telNo
        
        if (User.objects.filter(telNo=telNo).exclude(telNo=current_phone_number).exists() and not telNo == ""):
            raise serializers.ValidationError(detail={"telNo": "이미 사용중인 휴대폰 번호입니다."})
        
        return data
    
    def update(self, instance, validated_data):
        instance.userNameLoc = validated_data.get("userNameLoc", instance.userNameLoc)
        instance.email = validated_data.get("email", instance.email)
        instance.telNo = validated_data.get("telNo", instance.telNo)
        instance.save()
        
        return instance
    
# 로그아웃
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            raise serializers.ValidationError(detail={"만료된 토큰": "유효하지 않거나 만료된 토큰입니다."})