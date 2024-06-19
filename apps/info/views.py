from rest_framework.generics import ListAPIView, UpdateAPIView

from . import serializers
from . import models
from ..shared.utils import CustomPagination
from ..shared.views import BaseListView, BaseCreateView


# -------------------------------List views--------------------------------------------

class WarehouseListView(BaseListView):
	queryset = models.Warehouse.objects.all().order_by('-created_time')
	serializer_class = serializers.WarehouseSerializer
	filterset_fields = ['is_active', ]
	search_fields = ['id', 'code', 'name']


class MaterialListView(BaseListView):
	queryset = models.Material.objects.all().order_by('-created_time')
	serializer_class = serializers.MaterialSerializer
	filterset_fields = ['material_group', 'special_group', 'material_type']
	search_fields = ['code', 'name']


class MaterialTypeListView(ListAPIView):
	queryset = models.MaterialType.objects.all().order_by('id')
	serializer_class = serializers.MaterialTypeSerializer


class BoxSizeListView(ListAPIView):
	queryset = models.BoxSize.objects.all().order_by('id')
	serializer_class = serializers.BoxSizeSerializer


class MaterialGroupListView(ListAPIView):
	queryset = models.MaterialGroup.objects.all().order_by('id')
	serializer_class = serializers.MaterialGroupSerializer
	pagination_class = CustomPagination


class FirmListView(ListAPIView):
	queryset = models.Firm.objects.all().order_by('-created_time')
	serializer_class = serializers.FirmSerializer
	pagination_class = CustomPagination
	filterset_fields = ['type_firm']
	search_fields = ['id', 'code', 'name', 'mfo']


class MaterialSpecialGroupListView(ListAPIView):
	queryset = models.MaterialSpecialGroup.objects.all().order_by('id')
	serializer_class = serializers.MaterialSpecialGroupSerializer
	pagination_class = CustomPagination


class BrandListView(ListAPIView):
	queryset = models.Brand.objects.all().order_by('id')
	serializer_class = serializers.BrandSerializer
	pagination_class = CustomPagination


class SpecificationListView(ListAPIView):
	queryset = models.Specification.objects.all().order_by('id')
	serializer_class = serializers.SpecificationSerializer
	pagination_class = CustomPagination


class BoxTypeListView(ListAPIView):
	queryset = models.BoxType.objects.all().order_by('id')
	serializer_class = serializers.BoxTypeSerializer
	pagination_class = CustomPagination


# -------------------------------Crete views--------------------------------------------
class CreateWarehouseView(BaseCreateView):
	serializer_class = serializers.WarehouseSerializer


class CreateBrandView(BaseCreateView):
	serializer_class = serializers.BrandSerializer


class CreateMaterialTypeView(BaseCreateView):
	serializer_class = serializers.MaterialTypeSerializer


class CreateMaterialGroupView(BaseCreateView):
	serializer_class = serializers.MaterialGroupSerializer


class CreateMaterialSpecialGroupView(BaseCreateView):
	serializer_class = serializers.MaterialSpecialGroupSerializer


class CreateMaterialView(BaseCreateView):
	serializer_class = serializers.MaterialSerializer


class CreateBoxSizeView(BaseCreateView):
	serializer_class = serializers.BoxSizeSerializer


class CreateFirmView(BaseCreateView):
	serializer_class = serializers.FirmSerializer


class CreateSpecificationView(BaseCreateView):
	serializer_class = serializers.SpecificationSerializer


class CreateBoxTypeView(BaseCreateView):
	serializer_class = serializers.BoxTypeSerializer


# -------------------------------Update views--------------------------------------------


class MaterialUpdateView(UpdateAPIView):
	queryset = models.Material.objects.all()
	serializer_class = serializers.MaterialSerializer


class MaterialTypeUpdateView(UpdateAPIView):
	queryset = models.MaterialType.objects.all()
	serializer_class = serializers.MaterialTypeSerializer


class BoxSizeUpdateView(UpdateAPIView):
	queryset = models.BoxSize.objects.all()
	serializer_class = serializers.BoxSizeSerializer


class MaterialGroupUpdateView(UpdateAPIView):
	queryset = models.MaterialGroup.objects.all()
	serializer_class = serializers.MaterialGroupSerializer


class FirmUpdateView(UpdateAPIView):
	queryset = models.Firm.objects.all()
	serializer_class = serializers.FirmSerializer


class MaterialSpecialGroupUpdateView(UpdateAPIView):
	queryset = models.MaterialSpecialGroup.objects.all()
	serializer_class = serializers.MaterialSpecialGroupSerializer


class BrandUpdateView(UpdateAPIView):
	queryset = models.Brand.objects.all()
	serializer_class = serializers.BrandSerializer


class SpecificationUpdateView(UpdateAPIView):
	queryset = models.Specification.objects.all()
	serializer_class = serializers.SpecificationSerializer


class BoxTypeUpdateView(UpdateAPIView):
	queryset = models.BoxType.objects.all()
	serializer_class = serializers.BoxTypeSerializer
