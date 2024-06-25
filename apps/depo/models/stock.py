from django.db import models
from apps.shared.models import BaseModel
from django.core.validators import MinValueValidator


class Stock(BaseModel):
	material = models.ForeignKey('info.Material', on_delete=models.SET_NULL, null=True, verbose_name="Материал")
	warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, verbose_name="Склад")
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)],
								 verbose_name="Количество")

	class Meta:
		verbose_name = "Остаток на складе"
		verbose_name_plural = "Остатки на складе"
		indexes = [
			models.Index(fields=['material'])
		]

		def __str__(self):
			return f"{self.material} в {self.warehouse} ({self.amount} шт.)"
