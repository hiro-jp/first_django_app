# from django.contrib import auth
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
# from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from account.models import UserManager
from ps_core.models import SkillGroup


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    employee_code = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex=r'^\d\d\d\d\d\d\d$')],
        help_text=_('Required 7 digit code.'),
        unique=True,
    )

    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_approver = models.BooleanField(
        _('approver'),
        default=False,
        help_text=_(
            '承認権限。GMには承認権限があり、TLに承認権限がない場合、'
            '承認権限と閲覧権限を分ける。'
            'ふつう、approverのほうが、Unitのmanagerより少ない。'
        )
    )
    skill_group_follow = models.ManyToManyField(
        SkillGroup,
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'employee_code'
    REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_yoe(self):
        d = timezone.now() - self.date_joined
        return int(d.days / 365)

    def __str__(self):
        return ', '.join([self.employee_code, self.username])


class Unit(Group):
    upper_unit = models.ForeignKey(
        'Unit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # related_name="lower_unit_set",
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_(
            '各組織単位にひとりのリーダー。グループならGM、チームならTL。'
            '彼らはグループ員の情報を閲覧できる。'
            '承認権限はUserクラスのapproverが受け持つ。'
        )
    )

    def get_member(self):
        return User.objects.filter(groups=self)

    def has_member(self):
        return self.get_member().first() is not None

    def has_upper_unit(self):
        return False if self.upper_unit is None else True

    def get_upper_unit(self):
        return self.upper_unit

    def has_lower_unit(self):
        obj = Unit.objects.filter(upper_unit=self)
        return False if obj is None else True

    def get_lower_unit_set(self):
        return Unit.objects.filter(upper_unit=self)

