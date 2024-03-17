from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    # def as_tree(self):
    #     children = list(self.children.all())
    #     print('children: ', children)
    #     branch = bool(children)
    #     yield branch, self
    #     for child in children:
    #         for next in child.as_tree():
    #             print('next: ', next)
    #             yield next
    #         yield branch, None

    def __str__(self):
        return f'Item name: {self.name}'
