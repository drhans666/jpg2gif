from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator

from hdick.settings import UPLOAD_DIR
from .scripts import validate_file_extension


class Upload(models.Model):
    upload = models.FileField(verbose_name='Choose file', storage=default_storage, upload_to=UPLOAD_DIR,
                              validators=[validate_file_extension])
    date_added = models.DateTimeField(auto_now_add=True)
    output_name = models.CharField(default='', max_length=20)
    color = models.BooleanField(default=True)
    base_width = models.IntegerField(help_text="Value must be between 100-800.", default=500,
                                     validators=[MinValueValidator(10), MaxValueValidator(800)])
    speed = models.FloatField(help_text="No negative numbers. Stay positive", default=0.5,
                              validators=[MinValueValidator(0)])


class UploadStats(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default='', max_length=20)
    number_of_files = models.IntegerField(default=0)
    sourceurl = models.CharField(default='', max_length=200)
    width_size = models.IntegerField(default=500)
    frames = models.FloatField(default=0.5)


class SizeChange(models.Model):
    size_file = models.FileField(verbose_name='Choose file', storage=default_storage, upload_to=UPLOAD_DIR,
                                 validators=[validate_file_extension])
    size_name = models.CharField(verbose_name='New filename', default='', max_length=20)
    size_date_added = models.DateTimeField(auto_now_add=True)
    new_size = models.IntegerField(help_text="kb. Minimum value is 50kb ", default=500, validators=[MinValueValidator(50)])


class SizeChangeStats(models.Model):
    size_stat_date = models.DateTimeField(auto_now_add=True)
    size_stat_name = models.CharField(default='', max_length=20)
    old_stat_size = models.IntegerField(default=500)
    new_stat_size = models.IntegerField(default=500)
    output_file_path = models.CharField(default='', max_length=100)



