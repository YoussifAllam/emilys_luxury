from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator


class product_Category(models.TextChoices):
    Dress = "Dress", "Dress"
    Bag = "Bag", "Bag"


class Dresses(models.Model):
    status_choices = {"available": "available", "unavailable": "unavailable"}

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    designer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=status_choices)
    Color = models.CharField(max_length=30)
    measurement = models.CharField(max_length=6)
    price_for_3days = models.FloatField()
    price_for_6days = models.FloatField()
    price_for_8days = models.FloatField()
    actual_price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    delivery_information = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_special = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    product_type = models.CharField(max_length=10, choices=product_Category.choices)
    Num_of_rentals = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Dresses"
        verbose_name_plural = "Dresses"

    def __str__(self) -> str:
        return f"{self.id}"

    def is_investment(self):
        return hasattr(self, "investmenter_dresses")

    is_investment.boolean = True
    is_investment.short_description = "Is Investment"


class dress_images(models.Model):
    dress = models.ForeignKey(
        Dresses, related_name="image_set", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="dresses_images/")


class dress_busy_days(models.Model):
    dress = models.ForeignKey(
        Dresses, related_name="busy_day_set", on_delete=models.CASCADE
    )
    busy_day = models.DateField()
    is_temporary = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # New field to track when the booking was created
    order_uuid = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.dress} , {self.busy_day}"

    class Meta:
        unique_together = ("dress", "busy_day")


class dress_number_of_visitors(models.Model):
    dress = models.ForeignKey(
        Dresses, related_name="number_of_visitors_set", on_delete=models.CASCADE
    )
    number_of_visitors = models.IntegerField()

    class Meta:
        verbose_name = "Dress number of visitors"
        verbose_name_plural = "Dress number of visitors"

    def __str__(self) -> str:
        return f"{self.dress.id}"


class dress_reviews(models.Model):
    dress = models.ForeignKey(
        Dresses, related_name="review_set", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "Users.User", related_name="User_review_set", on_delete=models.CASCADE
    )
    Rating_stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating stars",
    )  # to control min and max values
    uploaded_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()

    def __str__(self) -> str:
        return f"{self.dress} -- {self.user}"

    class Meta:
        unique_together = ("user", "dress")
        index_together = ("user", "dress")

        verbose_name_plural = "Dresses Reviews"
        verbose_name = "Dresses Reviews"

        ordering = ["-uploaded_at"]


class favorite_dresses(models.Model):
    user = models.ForeignKey(
        "Users.User", related_name="User_favorite_set", on_delete=models.CASCADE
    )
    dress = models.ForeignKey(
        Dresses, related_name="favorite_set", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "dress")
