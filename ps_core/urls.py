from django.urls import path, include

from ps_core.views import SkillMasterIndexView, SkillMasterDetailView, UpdateRequestCreateView, UpdateRequestDetailView, \
    SkillMasterSummary, SkillMasterChartData

app_name = "ps_core"
urlpatterns = [
    path(
        '',
        SkillMasterIndexView.as_view(),
        name="index"
    ),
    path(
        'skill_master/detail/<int:pk>',
        SkillMasterDetailView.as_view(),
        name="skill_master_detail"
    ),
    path(
        'update_request/<int:pk>',
        UpdateRequestDetailView.as_view(),
        name="update_request_detail"
    ),
    path(
        'update_request/create/',
        UpdateRequestCreateView.as_view(),
        name="update_request_create"
    ),
    path(
        'skill_master/summary/',
        SkillMasterSummary.as_view(),
        name="skill_master_summary"
    ),
    path(
        'skill_master/chart/api2/',
        SkillMasterChartData.as_view(),
        name='api-data-2',
    ),
]
