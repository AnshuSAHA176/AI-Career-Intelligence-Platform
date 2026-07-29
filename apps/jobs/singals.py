from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Job

# @receiver([post_save,post_delete],sender=Job )
# def invalidate_job_cache(sender, instance, **kwargs):
#     print("clearing cache ")
#     cache.delete_pattern("*job_list*")


