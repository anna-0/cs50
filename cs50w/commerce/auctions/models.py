from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator 

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = (
        ("HOM", "Home"),
        ("ELC", "Electronics"),
        ("FSN", "Fashion"),
        ("PET", "Pets"),
        ("LES", "Leisure"),
        ("SUP", "Supplies"),
    )
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                default=0.01,
                                verbose_name="Starting bid")
    image = models.URLField(null=True, blank=True,
                            verbose_name="Image URL")
    date_added = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open = models.BooleanField(default=True)
    category = models.CharField(max_length=3,
                                choices=CATEGORIES,
                                )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        args = [
            str(self.id),
            ]
        return reverse('listing', args=args)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.listing}'

    def get_absolute_url(self):
        args = [str(self.listing_id)]
        return reverse('listing', args=args)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
    amount = models.DecimalField(max_digits=8, decimal_places=2, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    
    def __str__(self):
        return f'Bid for £{self.amount} on {self.listing} by {self.user}'
    def __int__(self):
        return self.amount

class Comment(models.Model):
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.comment}'
