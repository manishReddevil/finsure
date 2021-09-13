from django.db import models
import uuid


class Lenders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    upfront_commission_rate = models.IntegerField()
    trial_commission_rate = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
