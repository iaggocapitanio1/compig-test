from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save



class Base(models.Model):
    publication = models.DateTimeField(auto_now_add=True)
    actualization = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Company(Base):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=200)
    cnpj: str = models.CharField(max_length=12)
    email: str = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Producer(Base):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='producers')

    class Meta:
        verbose_name: str = 'Producer'
        verbose_name_plural: str = 'Producers'
        ordering: list = ['id']

    def __str__(self):
        return self.name


class Truck(Base):
    producer = models.ForeignKey(Producer, related_name='trucks', on_delete=models.CASCADE)
    license_plate: str = models.CharField(max_length=7, unique=True)

    class Meta:
        verbose_name: str = 'Truck'
        verbose_name_plural: str = 'Trucks'
        ordering: list = ['id']

    def __str__(self):
        if len(self.license_plate) == 7:
            return self.license_plate[:3] + " - " + self.license_plate[3:]
        return self.license_plate


class Loading(Base):
    STATUS = (
        ('Pending', 'Pending'),
        ('Finished', 'Finished'),
    )
    quantity = models.IntegerField()
    gta = models.IntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, related_name='loadings', null=True)
    cargo = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    class Meta:
        verbose_name = 'Loading'
        verbose_name_plural = 'Loading'
        ordering = ['-publication']

    def __str__(self):
        return f"{self.publication.strftime('%Y-%m-%d %H:%M:%S')}"
