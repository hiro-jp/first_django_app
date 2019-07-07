from django import template
from django.db.models import QuerySet
from ps_core.models import ReferenceRank

from ps_core.models import Rank

register = template.Library()


@register.filter
def ref_rank_filter(ref_rank_set: QuerySet, yoe):
    try:
        ref_rank_name = ref_rank_set.get(yoe=yoe).rank.name
    except ReferenceRank.DoesNotExist:
        return None
    return ref_rank_name
