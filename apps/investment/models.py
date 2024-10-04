from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class investmenter_details(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30)
    account_owner_name = models.CharField(max_length=40)
    credit_card_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=30)
    # payout_account_id = models.CharField(max_length=50)
    iban = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding or self.pk is None
        super(investmenter_details, self).save(*args, **kwargs)
        if is_new:
            investmenter_balance.objects.create(
                user=self.user, investmenter_detailsFk=self
            )

    class Meta:
        verbose_name = "Investmenter Bank Details"
        verbose_name_plural = "Investmenter Bank Details"


class investmenter_balance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="investmenter_bank_set"
    )
    investmenter_detailsFk = models.OneToOneField(
        "investmenter_details",
        on_delete=models.CASCADE,
        related_name="investmenter_bank",
    )
    total_balance = models.IntegerField(default=0)
    curr_balance = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} , {self.total_balance} , {self.curr_balance}"


class investmenter_dresses(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="investmenter_dresses_set"
    )
    dress = models.OneToOneField(
        "Dresses.Dresses", on_delete=models.CASCADE, related_name="investmenter_dresses"
    )

    class Meta:
        unique_together = ("user", "dress")
