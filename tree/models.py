from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Item name: {self.name}'
