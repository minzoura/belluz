from django.db import models

class BuyCrps(models.Model):
	crp_nm = models.CharField(max_length=100)
	crp_cd = models.CharField(max_length=20, db_index=True)
	strength = models.FloatField(default=0.0)
	current_price = models.IntegerField()
	target_price = models.IntegerField()

