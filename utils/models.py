from django.db import models
from .functions import create_id


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, default=create_id, max_length=26, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
