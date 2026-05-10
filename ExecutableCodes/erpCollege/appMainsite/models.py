from django.db import models

# Create your models here.


class MainsiteEnquiryForm(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=13)
    from_place=models.CharField(max_length=20)
    course= models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    db_table = "mainsite_enquiry_form"