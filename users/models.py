from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.validators import (
    MaxValueValidator,
    validate_image_file_extension,
    validate_ipv46_address,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userNameLoc = models.CharField("사용자이름(한국어)", max_length=50, unique=True)
    userNameGbl = models.CharField("사용자이름(영어)", max_length=50, unique=True)
    telNo = models.CharField("전화번호", max_length=64, blank=True)
    telCountryCode = models.CharField("전화국가번호", max_length=20, default="+82")
    email = models.EmailField("이메일주소", max_length=256)
    regDate = models.DateTimeField("계정 생성일", auto_now_add=True, null=True)
    regUserIP = models.CharField("계정 생성IP", max_length=20, null=True)
    userCode = models.CharField("사용자 구분", max_length=1, default="U")
    userStatus = models.CharField("사용자 상태", max_length=1)
    pwErrCount = models.IntegerField("비밀번호 실패횟수", default=0)
    last_loginIP = models.CharField("마지막 접속IP", max_length=20, default=False)
    is_admin = models.BooleanField("관리자", default=False)
    is_active = models.BooleanField("로그인 가능", default=True)

    objects = UserManager()

    USERNAME_FIELD = 'userNameLoc'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"[사용자이름(한국어)]{self.userNameLoc}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class LoggedIn(models.Model):
    updated_ip = models.GenericIPAddressField("로그인한 IP", validators=[validate_ipv46_address])
    country = models.CharField("로그인한 국가", max_length=255)
    created_at = models.DateTimeField("로그인 기록", auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")

    def __str__(self):
        return f"[아이디]{self.user.userNameLoc}, [접속 기록]{self.created_at}"

    class Meta:
        ordering = ["-created_at"]
