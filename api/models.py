from django.db import models


class url(models.Model):
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.url




class download(models.Model):
    url = models.URLField(max_length=120)
    file = models.FileField(null=True,blank=True)


    def __str__(self):
        return self.url
    