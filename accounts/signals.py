# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
# from django.dispatch import receiver
# import django.contrib.auth.models as models
# from .models import Company
#
#
# @receiver(post_save, sender=User)
# def company_profile(sender, instance, created, **kwargs):
#     if instance.is_staff:
#         if created:
#             group = Group.objects.get(name='staff')
#             instance.groups.add(group)
#             Company.objects.create(
#                 user=instance,
#                 name=instance.username,
#             )
#
#
# # post_save.connect(company_profile, sender=User)
#
#
# @receiver(post_save, sender=User)
# def update_profile(sender, instance: User, created, **kwargs):
#     if instance.is_staff:
#         if not created:
#             instance.company.save()
#             print('Profile updated!')
