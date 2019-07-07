from django.db import models

# Create your models here.
from django.utils.timezone import now


class Skill(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )
    description = models.CharField(
        max_length=200,
    )
    skill_group = models.ForeignKey(
        "SkillGroup",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )
    description = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return self.name


class ReferenceRank(models.Model):
    yoe = models.IntegerField(default=0)
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return ",".join([self.skill.name, self.rank.name, str(self.yoe)])

    class Meta:
        unique_together = ('yoe', 'skill')


class SkillGroup(models.Model):
    name = models.CharField(max_length=100)
    upper_skill_group = models.ForeignKey(
        "SkillGroup",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="lower_skill_group_set",
    )

    def __str__(self):
        return self.name


from users.models import User


class SkillMaster(models.Model):
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return ", ".join([self.user.username, self.skill.name, self.rank.name])

    class Meta:
        unique_together = ('skill', 'user')


class Status(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)

    def __str__(self):
        return self.name


class UpdateRequest(models.Model):
    skill_master = models.ForeignKey(
        SkillMaster,
        on_delete=models.CASCADE,
    )
    rank_cur = models.ForeignKey(
        Rank,
        on_delete=models.CASCADE,
        related_name='current_rank',
        null=True,
        verbose_name="current rank"
    )
    rank_req = models.ForeignKey(
        Rank,
        on_delete=models.CASCADE,
        related_name='request_rank',
        null=True,
        verbose_name="request rank"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reason = models.CharField(
        max_length=1023,
        null=False,
        blank=False,
    )
    comment = models.CharField(
        max_length=1023,
        null=True,
        blank=True,
    )

    date_req = models.DateTimeField(
        verbose_name="request date",
        default=now,
    )

    date_app = models.DateTimeField(
        verbose_name="approved date",
        default=now,
    )

    # def __str__(self):
    #     return self.skill_master.user.username + " requests " + \
    #            self.skill_master.skill.name + " rank from " + \
    #            self.rank_cur.name + " to " + self.rank_req.name

    class Meta:
        permissions = (
            ("can_create", "Can create update request"),
            ("can_approve", "Can approve update request")
        )
