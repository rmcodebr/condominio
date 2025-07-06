from uuid import UUID
from celery import shared_task
from .models import Profile


# tasks.py
from celery import shared_task
from django.core.files import File
from accounts.models import Profile
from PIL import Image
import os
from io import BytesIO

@shared_task
def save_profile_avatar(profile_id, image_path):
  try:
    profile = Profile.objects.get(id=profile_id)

    # Open the original image
    with Image.open(image_path) as img:
      # Convert to RGB if it's not (important for formats like PNG with alpha)
      if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

      # Resize (maintain aspect ratio, max width/height 300px)
      img.thumbnail((300, 300))

      # Save to a BytesIO buffer with compression (quality=70 for JPEG)
      buffer = BytesIO()
      img.save(buffer, format='JPEG', quality=70)
      buffer.seek(0)

      # Save to model field
      filename = f"resized_{os.path.basename(image_path)}"
      profile.avatar.save(filename, File(buffer), save=True)

    return "Avatar resized, compressed, and saved successfully"

  except Profile.DoesNotExist:
    return "Profile not found"
  except Exception as e:
    return str(e)


@shared_task(name="update_all_reputations")
def update_all_reputations():
  for profile in Profile.objects.all():
    profile.update_reputation()
    profile.save()

