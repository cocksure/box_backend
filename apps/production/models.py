from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models

from apps.info.models import Material, BoxSize, BoxType
from apps.shared.models import BaseModel
from apps.users.models import CustomUser


class Process(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Процесс"
		verbose_name_plural = "Процессы"


class UploadImage(models.Model):
	photo = models.ImageField(
		upload_to='box_photos/',
		default='no-image.png',
		validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])]
	)


class BoxModel(BaseModel):
	name = models.CharField(max_length=100, unique=True, verbose_name="Название")
	material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Материал")
	photos = models.ForeignKey(
		UploadImage,
		on_delete=models.CASCADE,
		related_name='box_model',
		blank=True,
		null=True
	)
	box_size = models.ForeignKey(BoxSize, on_delete=models.SET_NULL,
								 blank=True, null=True, related_name='box_models_with_size',
								 verbose_name="Размер коробки")
	box_type = models.ForeignKey(BoxType, on_delete=models.SET_NULL,
								 blank=True, null=True, related_name='box_models_with_type', verbose_name="Тип коробки")

	class Meta:
		verbose_name = "Модель коробки"
		verbose_name_plural = "Модели коробок"

	def __str__(self):
		return self.name


class BoxOrder(BaseModel):
	class BoxOrderStatus(models.TextChoices):
		ACCEPT = 'Одобрено', 'Одобрено'
		REJECT = 'Отклонено', 'Отклонено'
		NEW = 'НОВАЯ', 'НОВАЯ'

	data = models.DateField(editable=True, verbose_name="Дата")
	customer = models.CharField(max_length=100, null=True, blank=True, verbose_name="Клиент")
	status = models.CharField(choices=BoxOrderStatus.choices, default=BoxOrderStatus.NEW, null=True, blank=True,
							  max_length=20, verbose_name="Статус")
	type_order = models.CharField(max_length=100, verbose_name="Тип заказа")
	specification = models.CharField(max_length=100, verbose_name="Спецификация")
	manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Менеджер")
	date_of_production = models.DateField(editable=True, verbose_name="Дата производства")

	def new(self):
		if self.status is None:
			self.status = self.BoxOrderStatus.NEW
			self.save()

	def confirm(self):
		if self.status == self.BoxOrderStatus.NEW:
			self.status = self.BoxOrderStatus.ACCEPT
			self.save()

	def reject(self):
		if self.status == self.BoxOrderStatus.NEW:
			self.status = self.BoxOrderStatus.REJECT
			self.save()

	def __str__(self):
		return f"Заказ - {self.id}"

	class Meta:
		verbose_name = "Заказ коробки"
		verbose_name_plural = "Заказы коробок"


class BoxOrderDetail(models.Model):
	box_order = models.ForeignKey(BoxOrder, on_delete=models.CASCADE, verbose_name="Заказ коробки")
	box_model = models.ForeignKey(BoxModel, on_delete=models.CASCADE, verbose_name="Модель коробки")
	amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
								 verbose_name="Количество")

	def __str__(self):
		return f"{self.box_order} - {self.box_model}"

	class Meta:
		verbose_name = "Детали заказа коробки"
		verbose_name_plural = "Детали заказов коробок"


class ProductionOrder(models.Model):
	box_order_detail = models.ForeignKey(
		BoxOrderDetail,
		on_delete=models.CASCADE,
		related_name='production_orders',
		blank=True,
		null=True,
		verbose_name="Детали заказа коробки"
	)
	shipping_date = models.DateField(verbose_name="Дата доставки")
	amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")

	status_choices = (
		('in_progress', 'In Progress'),
		('completed', 'Completed'),
		('not_started', 'Not Started'),
	)
	status = models.CharField(max_length=20, choices=status_choices, default='not_started', verbose_name="Статус")
	type_of_work = models.ManyToManyField(Process, related_name='processes', blank=True, verbose_name="Тип работы")

	class Meta:
		verbose_name = "Производственный заказ"
		verbose_name_plural = "Производственные заказы"
