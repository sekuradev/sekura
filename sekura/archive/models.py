from django.db import models
import hashlib
import os


def hash_file(file, block_size=65536):
    hasher = hashlib.sha512()
    for buf in iter(hasher(file.read, block_size), b""):
        hasher.update(buf)

    return hasher.hexdigest()


def hash_upload(instance, filename):
    _, ext = os.path.splitext(filename)
    with open(instance.content.file.path) as fd:
        name = hash_file(fd)
    return f"{name}.{ext}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Archive(models.Model):
    name = models.CharField(max_length=100)
    # content = models.FileField(upload_to=hash_upload)
    content = models.FileField()
    categories = models.ManyToManyField(Category, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
