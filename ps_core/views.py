from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import ModelFormMixin

from ps_core.forms import UpdateRequestCreateForm, UpdateRequestApproveForm
from ps_core.models import SkillMaster, UpdateRequest, Status, Rank, SkillGroup, ReferenceRank, Skill
from users.models import User, Unit


class SkillMasterIndexView(PermissionRequiredMixin, ListView):
    model = SkillMaster
    template_name = 'ps_core/skill_master_index.html'
    permission_required = (
        'ps_core.can_create',
    )
    raise_exception = False
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return SkillMaster.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['yoe'] = self.request.user.get_yoe()
        context['update_request_list'] = \
            UpdateRequest.objects.filter(
                approver=self.request.user
            ).filter(status__name="Waiting").order_by('date_req')
        return context


class SkillMasterDetailView(UserPassesTestMixin, ModelFormMixin, DetailView):
    model = SkillMaster
    template_name = 'ps_core/skill_master_detail.html'
    form_class = UpdateRequestCreateForm

    def get(self, request, *args, **kwargs):
        self.request.session['skill_master_id'] = SkillMaster.objects.get(pk=self.kwargs['pk']).id
        self.request.session['rank_cur_id'] = SkillMaster.objects.get(pk=self.kwargs['pk']).rank.id
        self.request.session['status_id'] = Status.objects.get(name="Waiting").id
        self.request.session['approver_id'] = User.objects.get(username="admin").id
        return super().get(request)

    def test_func(self):
        user = self.request.user
        skill_master_user = SkillMaster.objects.get(pk=self.kwargs['pk']).user
        return user == skill_master_user or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['update_request_list'] = \
            UpdateRequest.objects.filter(
                skill_master=SkillMaster.objects.get(pk=self.kwargs['pk'])).order_by('-date_req')
        return context


class UpdateRequestCreateView(CreateView):
    model = UpdateRequest
    form_class = UpdateRequestCreateForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.skill_master = SkillMaster.objects.get(id=self.request.session['skill_master_id'])
        form.instance.rank_cur = Rank.objects.get(id=self.request.session['rank_cur_id'])
        form.instance.status = Status.objects.get(id=self.request.session['status_id'])
        form.instance.approver = User.objects.get(id=self.request.session['approver_id'])
        del self.request.session['skill_master_id']
        del self.request.session['rank_cur_id']
        del self.request.session['status_id']
        del self.request.session['approver_id']
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateRequestDetailView(UpdateView):
    model = UpdateRequest
    template_name = "ps_core/update_request_detail.html"
    form_class = UpdateRequestApproveForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['update_request'] = update_request = UpdateRequest.objects.get(id=self.kwargs['pk'])
        context['skill_master'] = skill_master = SkillMaster.objects.get(id=update_request.skill_master.id)
        context['update_request_list'] = UpdateRequest.objects.filter(skill_master__user=skill_master.user).filter(skill_master__skill=update_request.skill_master.skill).order_by('-date_app')
        return context

    def get(self, request, *args, **kwargs):
        self.request.session['update_request_id'] = self.kwargs['pk']
        return super().get(request)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ↑とても重要！あとでまとめる。
        form = self.get_form()
        ur_id = self.object.id
        ur_object = UpdateRequest.objects.get(id=ur_id)
        form.instance.approver = ur_object.approver
        form.instance.skill_master = ur_object.skill_master
        form.instance.reason = ur_object.reason
        form.instance.rank_req = ur_object.rank_req
        form.instance.rank_cur = ur_object.rank_cur
        form.instance.date_req = ur_object.date_req
        form.instance.date_app = timezone.now()
        del self.request.session['update_request_id']
        if form.is_valid():
            if form.instance.status == Status.objects.get(name="Approved"):
                sm = SkillMaster.objects.get(id=ur_object.skill_master.id)
                sm.rank = ur_object.rank_req
                sm.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SkillMasterSummary(UserPassesTestMixin, TemplateView):
    template_name = "ps_core/skill_master_summary.html"

    def test_func(self):
        user = self.request.user
        if user.is_anonymous:
            return False
        unit_set = user.unit_set.all()
        for u in unit_set:
            if u.manager == user:
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        unit = user.unit_set.first()
        member = unit.get_member()
        context['member'] = member.exclude(id=user.id)
        return context


class SkillMasterChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        user = User.objects.get(id=1)
        unit_set = Unit.objects.filter(manager=user)

        # 自分がmanagerを勤めているunitのリストでしかない。
        # 半分abstractみたいなもので、ここにはメンバーはいない。
        data = {
            "id": 0,
            "subs": self.extract_subs(unit_set),
            "member": [],
        }
        return Response(data)

    def extract_subs(self, unit_set):
        result = []
        if unit_set.first() is None:
            return result
        else:
            for unit in unit_set:
                unit_data = {
                    "id": unit.id,
                    "subs": [],
                    "member": [],
                }
                if unit.has_lower_unit():
                    unit_data["subs"] = self.extract_subs(unit.get_lower_unit_set())
                if unit.has_member():
                    unit_data["member"] = self.extract_member(unit)
                result.append(unit_data)
            return result

    def extract_member(self, unit):
        result = []
        member = unit.get_member()
        for user in member:
            user_data = {
                "id": user.id,
                "name": user.username,
                "yoe": user.get_yoe(),
                "skill_group": self.extract_skill_group(user=user),
            }
            result.append(user_data)
        return result

    def extract_skill_group(self, user: User, skill_group: SkillGroup=None):
        result = []
        if skill_group is None:
            skill_group_follow = user.skill_group_follow.all()
        else:
            skill_group_follow = skill_group.lower_skill_group_set.all()
        for sg in skill_group_follow:
            sg_data = {
                "id": sg.id,
                "name": sg.name,
                "skill_group": self.extract_skill_group(user=user, skill_group=sg),
                "skill": self.extract_skill(user=user, skill_group=sg)
            }
            result.append(sg_data)
        return result

    def extract_skill(self, user: User, skill_group: SkillGroup):
        skill_set = skill_group.skill_set.all()
        if skill_set.first() is None:
            return []
        skill_data = {
            "label": [],
            "user_data": [],
            "ref_data": [],
        }
        for skill in skill_set:
            skill_data["label"].append(skill.name)
            skill_data["user_data"].append(self.extract_rank(user, skill))
            skill_data["ref_data"].append(self.extract_ref_rank(user, skill))
        return skill_data

    def extract_rank(self, user: User, skill: Skill):
        skill_master = SkillMaster.objects.filter(user=user).filter(skill=skill).first()
        if skill_master is not None:
            return self.conv_rank(skill_master.rank.name)

    def extract_ref_rank(self, user: User, skill: Skill):
        ref_rank = ReferenceRank.objects.filter(yoe=user.get_yoe()).filter(skill=skill).first()
        if ref_rank is not None:
            return self.conv_rank(ref_rank.rank.name)

    def conv_rank(self, rank: str):
        if rank is "A":
            return 5
        elif rank is "B":
            return 4
        elif rank is "C":
            return 3
        elif rank is "D":
            return 2
        elif rank is "E":
            return 1
        else:
            return 0
