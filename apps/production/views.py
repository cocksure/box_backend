from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import generics, status

from .models import BoxModel, BoxOrder, BoxOrderDetail, ProductionOrder, ProcessLog, Process
from .serializers import BoxModelSerializer, BoxOrderSerializer, ProductionOrderSerializer, ProcessLogSerializer, \
	ProcessLogCreateSerializer, PackagingAmountSerializer, ProductionOrderCodeSerializer
from rest_framework.permissions import IsAuthenticated

from ..depo.models.incoming import IncomingMaterial, Incoming
from ..depo.models.outgoing import Outgoing, OutgoingMaterial
from ..depo.models.stock import Stock
from ..info.models import Warehouse, Material, MaterialType
from ..shared.utils import CustomPagination, generate_qr_code
from django.template.loader import render_to_string
from weasyprint import HTML

from ..shared.views import BaseListView


class BoxModelListCreate(generics.ListCreateAPIView):
	queryset = BoxModel.objects.all()
	serializer_class = BoxModelSerializer
	filterset_fields = ['box_type']
	search_fields = ['material__name', 'name']


class BoxOrderListCreate(generics.ListCreateAPIView):
	queryset = BoxOrder.objects.all().order_by('-created_time')
	serializer_class = BoxOrderSerializer
	permission_classes = [IsAuthenticated]
	filterset_fields = ['type_order', 'status']
	search_fields = ['id', 'specification__name']
	pagination_class = CustomPagination

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['request'] = self.request
		return context


class BoxOrderDetailView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, pk):
		box_order = get_object_or_404(BoxOrder, pk=pk)
		serializer = BoxOrderSerializer(box_order)
		return Response(serializer.data)

	def post(self, request, pk):
		box_order = get_object_or_404(BoxOrder, pk=pk)
		new_status = request.data.get('status')

		if new_status is not None:
			if not request.user.is_director:
				return Response({'error': 'У вас нет прав для выполнения этого действия.'},
								status=status.HTTP_403_FORBIDDEN)

			if new_status in [choice[0] for choice in BoxOrder.BoxOrderStatus.choices]:
				if box_order.status == BoxOrder.BoxOrderStatus.NEW:
					box_order.status = new_status
					box_order.save()
					return Response({'message': 'Статус заказа успешно обновлен.'}, status=status.HTTP_200_OK)
				else:
					return Response({'error': 'Заказ уже одобрен или отклонен'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'error': 'Неверный параметр статуса.'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			if box_order.status != BoxOrder.BoxOrderStatus.ACCEPT:
				return Response(
					{'error': 'Производственный заказ можно создать только если заказ на коробки утвержден.'},
					status=status.HTTP_400_BAD_REQUEST)

			detail_id = request.data.get('box_order_detail_id')
			if not detail_id:
				return Response({'error': 'Не указан идентификатор детали заказа коробки.'},
								status=status.HTTP_400_BAD_REQUEST)

			detail = get_object_or_404(BoxOrderDetail, pk=detail_id)

			if ProductionOrder.objects.filter(box_order_detail=detail).exists():
				return Response({'error': 'Производственный заказ для этой детали заказа коробки уже существует.'},
								status=status.HTTP_400_BAD_REQUEST)

			amount = detail.amount  # Получаем amount из BoxOrderDetail

			data = {
				'box_order_detail': detail.id,
				'shipping_date': request.data.get('shipping_date'),
				'amount': amount,
				'notes': request.data.get('notes'),
				'type_of_work': request.data.get('type_of_work')  # Передача поля вручную

			}

			serializer = ProductionOrderSerializer(data=data)
			if serializer.is_valid():
				grams_per_box = detail.box_model.grams_per_box
				if grams_per_box is None or detail.amount is None:
					return Response({'error': 'Грамм на одну коробку или количество не определены!'},
									status=status.HTTP_400_BAD_REQUEST)

				total_material_amount = detail.amount * grams_per_box

				with transaction.atomic():
					production_order = serializer.save()

					# Создаем запись о расходе
					warehouse_id = 1
					warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

					outgoing = Outgoing.objects.create(
						data=production_order.shipping_date,
						outgoing_type=Outgoing.OutgoingType.OUTGO,
						warehouse=warehouse,
						created_by=request.user
					)

					outgoing_material = OutgoingMaterial.objects.create(
						outgoing=outgoing,
						material=detail.box_model.material,
						amount=total_material_amount,
						production_order=production_order  # Связываем с производственным заказом
					)

					# Обновляем производственный заказ, связывая с OutgoingMaterial
					production_order.outgoing_detail = outgoing_material
					production_order.save()

					# Обновляем остатки на складе
					stock, created = Stock.objects.get_or_create(material=detail.box_model.material,
																 warehouse=warehouse)
					if stock.amount < total_material_amount:
						transaction.set_rollback(True)
						return Response({'error': 'Недостаточно материалов на складе.'},
										status=status.HTTP_400_BAD_REQUEST)

					stock.amount -= total_material_amount
					stock.save()

				return Response({'message': 'Производственный заказ успешно создан.'}, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessLogView(APIView):
	def get(self, request):
		process_logs = ProcessLog.objects.all()
		serializer = ProcessLogSerializer(process_logs, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ProcessLogCreateSerializer(data=request.data)
		if serializer.is_valid():
			try:
				process_log = serializer.save()
				return Response({
					'message': f'Process "{process_log.process.name}" marked as completed for order {process_log.production_order.code}.'},
					status=status.HTTP_201_CREATED)
			except ValidationError as e:
				return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackagingView(APIView):
	def post(self, request):
		if 'production_order_code' in request.data:
			code_serializer = ProductionOrderCodeSerializer(data=request.data)
			if code_serializer.is_valid():
				code_or_id = code_serializer.validated_data['production_order_code']
				try:
					if code_or_id.isdigit():
						production_order = ProductionOrder.objects.get(id=code_or_id)
					else:
						production_order = ProductionOrder.objects.get(code=code_or_id)

					type_of_work = production_order.type_of_work
					processes = type_of_work.process.order_by('queue')
					completed_processes = ProcessLog.objects.filter(production_order=production_order).values_list(
						'process', flat=True
					)

					if not processes.exclude(id__in=completed_processes).exists():
						remaining_to_pack = production_order.amount - production_order.packed_amount
						request.session['production_order_id'] = str(production_order.id)
						request.session['remaining_to_pack'] = str(remaining_to_pack)
						return Response({'message': f'Можно упаковать до {remaining_to_pack} товаров!',
										 'remaining_to_pack': remaining_to_pack})
					else:
						return Response({'error': 'Не все процессы завершены для этого заказа.'},
										status=status.HTTP_400_BAD_REQUEST)
				except ProductionOrder.DoesNotExist:
					return Response({'error': 'Заказ с таким кодом или ID не найден.'},
									status=status.HTTP_404_NOT_FOUND)
			else:
				return Response(code_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		elif 'packed_amount' in request.data:
			amount_serializer = PackagingAmountSerializer(data=request.data)
			if amount_serializer.is_valid():
				packed_amount = amount_serializer.validated_data['packed_amount']
				production_order_id = request.session.get('production_order_id')
				remaining_to_pack = request.session.get('remaining_to_pack')

				if production_order_id and remaining_to_pack is not None:
					try:
						production_order = ProductionOrder.objects.get(id=production_order_id)
						remaining_to_pack = Decimal(remaining_to_pack)

						if packed_amount > remaining_to_pack:
							return Response({'error': f'Невозможно упаковать больше {remaining_to_pack} товаров.'},
											status=status.HTTP_400_BAD_REQUEST)

						with transaction.atomic():
							production_order.packed_amount += packed_amount
							production_order.status = ProductionOrder.ProductionOrderStatus.PACKED
							production_order.save()

							warehouse_id = 2
							warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

							incoming = Incoming.objects.create(
								data=timezone.now(),
								warehouse=warehouse,
								created_by=request.user,
								created_time=timezone.now()
							)

							raw_material = production_order.box_order_detail.box_model.material
							finished_material_name = production_order.box_order_detail.box_model.name
							finished_material_type = get_object_or_404(MaterialType, name="Готовый продукт")

							finished_material, created = Material.objects.get_or_create(
								name=finished_material_name,
								defaults={
									'code': f'FIN_{production_order.box_order_detail.box_model.name}',
									'material_group': raw_material.material_group,
									'special_group': raw_material.special_group,
									'brand': raw_material.brand,
									'material_type': finished_material_type,
									'material_thickness': raw_material.material_thickness,
									'unit_of_measurement': raw_material.unit_of_measurement
								}
							)

							IncomingMaterial.objects.create(
								material=finished_material,
								amount=packed_amount,
								comment='Упаковано',
								incoming=incoming
							)

							stock, created = Stock.objects.get_or_create(material=finished_material,
																		 warehouse=warehouse)
							stock.amount += packed_amount
							stock.save()

							del request.session['production_order_id']
							del request.session['remaining_to_pack']

							return Response({'message': f'Упаковка завершена для заказа - {production_order.code}.'},
											status=status.HTTP_200_OK)
					except ProductionOrder.DoesNotExist:
						return Response({'error': 'Произошла ошибка, заказ не найден.'},
										status=status.HTTP_404_NOT_FOUND)
				else:
					return Response({'error': 'Сессия данных заказа не найдена.'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(amount_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'error': 'Некорректный запрос.'}, status=status.HTTP_400_BAD_REQUEST)


class ProductionOrderListAPIView(BaseListView):
	queryset = ProductionOrder.objects.all().order_by('-created_time')
	serializer_class = ProductionOrderSerializer
	filterset_fields = ['status', ]
	search_fields = ['code']
	ordering_fields = ['created_time', 'status']

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['request'] = self.request
		return context


class ProcessLogListAPIView(BaseListView):
	queryset = ProcessLog.objects.select_related('production_order', 'process').order_by('-timestamp')
	serializer_class = ProcessLogSerializer
	search_fields = ['production_order__code', 'process__name']
	ordering_fields = ['timestamp', 'production_order__status', 'process__name']

	def get_queryset(self):
		queryset = super().get_queryset()
		process = self.request.query_params.get('process', None)
		status = self.request.query_params.get('status', 'all')
		start_date = self.request.query_params.get('start_date', None)
		end_date = self.request.query_params.get('end_date', None)

		if process:
			queryset = queryset.filter(process_id=process)
		if status and status != "all":
			queryset = queryset.filter(production_order__status=status)
		if start_date:
			queryset = queryset.filter(timestamp__gte=start_date)
		if end_date:
			queryset = queryset.filter(timestamp__lte=end_date)

		return queryset

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['request'] = self.request
		return context


# ---------------------------------------------PDF views start----------------------------------------------------------


class GenerateBoxOrderPDFView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, order_id):
		order = get_object_or_404(BoxOrder, id=order_id)
		serializer = BoxOrderSerializer(order)

		# Debugging: Print serialized data to the console
		print(serializer.data)

		# Render the HTML template with the serialized data
		html_string = render_to_string('pdf/box_order_pdf.html', {'order': serializer.data})
		html = HTML(string=html_string)
		pdf = html.write_pdf()

		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = f'attachment; filename="box_order_{order_id}.pdf"'
		return response


def generate_production_order_pdf(request, production_order_id):
	production_order = get_object_or_404(ProductionOrder, id=production_order_id)
	box_order_detail = production_order.box_order_detail
	box_order = box_order_detail.box_order
	box_model = box_order_detail.box_model

	# Генерация QR-кода (если требуется)
	qr_code_data = generate_qr_code(production_order.code)

	# Получение процессов, связанных с типом работы
	processes = Process.objects.all()

	# Создание словаря для хранения информации о процессах для всех заказов на производство
	all_production_orders = ProductionOrder.objects.all()
	order_process_status = {}

	for order in all_production_orders:
		order_process_status[order.id] = {}
		logs = ProcessLog.objects.filter(production_order=order)
		for log in logs:
			process_id = log.process.id
			order_process_status[order.id][process_id] = True

	photo_url = request.build_absolute_uri(box_model.photos.photo.url) if box_model.photos else None

	context = {
		'order': production_order,
		'qr_code_data': qr_code_data,
		'box_order': box_order,
		'box_model': box_model,
		'photo_url': photo_url,
		'order_details': box_order_detail,
		'processes': processes,
		'order_process_status': order_process_status,
		'production_orders': all_production_orders,
	}

	html_string = render_to_string('pdf/production_order_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
	pdf = html.write_pdf()

	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="production_order_{production_order.id}.pdf"'

	return response

# ----------------------------------------PDF views finish----------------------------------------------------------
