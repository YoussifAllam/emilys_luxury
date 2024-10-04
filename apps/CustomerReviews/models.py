from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CustomerReviews(models.Model):
    user = models.ForeignKey(
        "Users.User", related_name="CustomerReviews_set", on_delete=models.CASCADE
    )
    Rating_stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating stars",
    )  # to control min and max values
    uploaded_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        unique_together = ("user", "feedback")
        index_together = ("user", "feedback")

        verbose_name_plural = "Customer Reviews"
        verbose_name = "Customer Reviews"

        ordering = ["-uploaded_at"]
