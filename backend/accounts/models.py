from django.db import models
from django.contrib.auth.models import AbstractUser

HF_PRODUCT_TYPE = (
    ("happyfox_helpdesk", "HappyFox Helpdesk"),
    ("happyfox_service_desk", "HappyFox Service Desk"),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(BaseModel):
    product = models.TextField(choices=HF_PRODUCT_TYPE)
    account_reference = models.TextField()

    def __str__(self):
        return f"{self.product} - {self.account_reference}"

    class Meta:
        ordering = ["created_at"]


# TODO: Implement better Role later
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username