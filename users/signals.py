# from users.models import NewUser
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import Profile

# @receiver(post_save, sender = NewUser)
# def create_profile(sender, instance, created, *args, **kwags):
#   if created:
#       Profile.objects.create(user = instance)

# @receiver(post_save, sender = NewUser)
# def save_profile(sender, instance, *args, **kwags):
  
#     instance.profile.save()