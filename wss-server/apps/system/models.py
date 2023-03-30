from django.db import models


class SystemSetting(models.Model):
	MODE_CHOICES = (
		(1, 'Mode 1'),
		(1, 'Mode 1'),
		(1, 'Mode 1'),
		(1, 'Mode 1')
	)
	mode = models.IntegerField(choices=MODE_CHOICES, default=1)

	class Meta:
		verbose_name = "system_setting"
		verbose_name_plural = "system_setting"

	def __str__(self) -> str:
		return str(self.mode)