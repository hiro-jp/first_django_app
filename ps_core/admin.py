from django.contrib import admin

# Register your models here.
from ps_core.models import Rank, Skill, ReferenceRank, SkillMaster, UpdateRequest, Status, SkillGroup


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferenceRank)
class RefRankAdmin(admin.ModelAdmin):
    pass


@admin.register(SkillMaster)
class SkillMasterAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(UpdateRequest)
class UpdateRequestAdmin(admin.ModelAdmin):
    pass
