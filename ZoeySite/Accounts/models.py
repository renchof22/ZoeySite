from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

DEFAULT_IMAGE = "../../media/default/no_image.png"


class UserManager(BaseUserManager):

    # ユーザー新規作成時に呼び出されるメソッド
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        elif not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # スーパーユーザー作成時に呼び出されるメソッド
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    psn_id = models.CharField(max_length=30)
    image = models.ImageField(upload_to='account_image', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    status_enable = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return '<id:' + str(self.username) + ',' + str(self.email) + '>'

    def get_image(self):
        if not self.image:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image.url

    def get_image_thumbnail(self):
        if not self.image_thumbnail:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image_thumbnail.url
