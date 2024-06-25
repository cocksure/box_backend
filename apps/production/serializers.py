from rest_framework import serializers
from .models import Process, BoxModel, BoxOrder, BoxOrderDetail, ProductionOrder, UploadImage, ProcessLog, TypeWork


class ProcessSerializer(serializers.ModelSerializer):
	class Meta:
		model = Process
		fields = '__all__'


class UploadImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = UploadImage
		fields = ('id', 'photo')


class BoxModelSerializer(serializers.ModelSerializer):
	material_name = serializers.CharField(source='material.name', read_only=True)
	box_size_name = serializers.CharField(source='box_size.name', read_only=True)
	box_type_name = serializers.CharField(source='box_type.name', read_only=True)
	image_url = serializers.SerializerMethodField()
	color = serializers.CharField(read_only=True)

	class Meta:
		model = BoxModel
		fields = (
			'id', 'name', 'material', 'material_name', 'box_size', 'box_size_name', 'color',
			'box_type', 'box_type_name', 'photos', 'image_url')

	def get_image_url(self, obj):
		if obj.photos and obj.photos.photo:
			return obj.photos.photo.url
		return None


class BoxOrderDetailSerializer(serializers.ModelSerializer):
	box_model = BoxModelSerializer()

	class Meta:
		model = BoxOrderDetail
		fields = '__all__'
		extra_kwargs = {'box_order': {'required': False}}


class ProductionOrderSerializer(serializers.ModelSerializer):
	type_of_work = serializers.PrimaryKeyRelatedField(queryset=TypeWork.objects.all(), required=True)

	class Meta:
		model = ProductionOrder
		fields = '__all__'


class BoxOrderSerializer(serializers.ModelSerializer):
	box_order_details = BoxOrderDetailSerializer(many=True, source='details')
	production_orders = ProductionOrderSerializer(many=True, read_only=True)
	data = serializers.DateField(required=True)

	class Meta:
		model = BoxOrder
		fields = '__all__'
		read_only_fields = ('created_by', 'updated_by', 'created_time', 'updated_time')

	def create(self, validated_data):
		details_data = validated_data.pop('details', [])
		user = self.context['request'].user  # Получаем текущего пользователя
		box_order = BoxOrder.objects.create(created_by=user, **validated_data)
		for detail_data in details_data:
			BoxOrderDetail.objects.create(box_order=box_order, **detail_data)
		return box_order

	def update(self, instance, validated_data):
		details_data = validated_data.pop('details', [])
		instance = super().update(instance, validated_data)

		existing_details_ids = [detail.id for detail in instance.details.all()]

		# Update existing details or create new ones
		for detail_data in details_data:
			detail_id = detail_data.get('id')
			if detail_id:
				if detail_id in existing_details_ids:
					detail = BoxOrderDetail.objects.get(id=detail_id, box_order=instance)
					for attr, value in detail_data.items():
						setattr(detail, attr, value)
					detail.save()
				else:
					BoxOrderDetail.objects.create(box_order=instance, **detail_data)
			else:
				BoxOrderDetail.objects.create(box_order=instance, **detail_data)

		# Delete details that are not in updated data
		for detail in instance.details.all():
			if detail.id not in [d.get('id') for d in details_data]:
				detail.delete()

		return instance


class ProcessLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProcessLog
		fields = '__all__'


class ProcessLogCreateSerializer(serializers.Serializer):
	production_order_code = serializers.CharField()

	def create(self, validated_data):
		code_or_id = validated_data['production_order_code']
		try:
			if code_or_id.isdigit():
				production_order = ProductionOrder.objects.get(id=code_or_id)
			else:
				production_order = ProductionOrder.objects.get(code=code_or_id)

			type_of_work = production_order.type_of_work
			processes = type_of_work.process.order_by('queue')

			completed_processes = ProcessLog.objects.filter(production_order=production_order).values_list('process',
																										   flat=True)
			next_process = processes.exclude(id__in=completed_processes).first()

			if next_process:
				process_log = ProcessLog.objects.create(production_order=production_order, process=next_process)

				if next_process.queue == processes.first().queue:
					production_order.status = ProductionOrder.ProductionOrderStatus.IN_PROGRESS
				elif next_process.queue == processes.last().queue:
					production_order.status = ProductionOrder.ProductionOrderStatus.COMPLETED

				production_order.save()
				return process_log
			else:
				raise serializers.ValidationError("All processes for this order are already completed.")
		except ProductionOrder.DoesNotExist:
			raise serializers.ValidationError("Order with this code or ID does not exist.")


class ProductionOrderCodeSerializer(serializers.Serializer):
	production_order_code = serializers.CharField()


class PackagingAmountSerializer(serializers.Serializer):
	packed_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
