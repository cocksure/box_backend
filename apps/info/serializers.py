from rest_framework import serializers
from apps.info import models
from apps.shared.serializers import BaseNameCodeSerializer


class WarehouseSerializer(BaseNameCodeSerializer):
	managers = serializers.SerializerMethodField()

	class Meta:
		model = models.Warehouse
		fields = (
			'id', 'code', 'name', 'location', 'can_import', 'can_export', 'use_negative', 'is_active', 'managers'
		)

		read_only_fields = ['code']

	def get_managers(self, obj):
		managers = obj.managers.all()
		return [{'id': manager.id, 'manager_name': manager.username} for manager in managers] if managers else None


class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Brand
		fields = '__all__'


class MaterialTypeSerializer(BaseNameCodeSerializer):
	class Meta:
		model = models.MaterialType
		fields = ('id', 'name')


class MaterialGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.MaterialGroup
		fields = '__all__'


class MaterialSpecialGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.MaterialSpecialGroup
		fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
	group_id = serializers.SerializerMethodField()
	group_name = serializers.SerializerMethodField()
	type_id = serializers.SerializerMethodField()
	type_name = serializers.SerializerMethodField()
	spec_group_id = serializers.SerializerMethodField()
	spec_name = serializers.SerializerMethodField()
	brand_id = serializers.SerializerMethodField()
	brand_name = serializers.SerializerMethodField()

	class Meta:
		model = models.Material
		fields = (
			'id', 'code', 'name', 'material_group', 'group_id', 'group_name',
			'type_id', 'type_name', 'material_type',
			'unit_of_measurement', 'created_time', 'updated_time',
			'created_by', 'updated_by', 'special_group', 'spec_group_id', 'spec_name',
			'brand', 'brand_id', 'brand_name'
		)
		read_only_fields = ['code']

	def get_group_id(self, obj):
		return obj.material_group.id if obj.material_group else None

	def get_group_name(self, obj):
		return obj.material_group.name if obj.material_group else None

	def get_type_id(self, obj):
		return obj.material_type.id if obj.material_type else None

	def get_type_name(self, obj):
		return obj.material_type.name if obj.material_type else None

	def get_spec_group_id(self, obj):
		return obj.special_group.id if obj.special_group else None

	def get_spec_name(self, obj):
		return obj.special_group.name if obj.special_group else None

	def get_brand_id(self, obj):
		return obj.brand.id if obj.brand else None

	def get_brand_name(self, obj):
		return obj.brand.name if obj.brand else None


class BoxSizeSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.BoxSize
		fields = '__all__'


class FirmSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Firm
		fields = '__all__'
		read_only_fields = ['code']


class SpecificationSerializer(serializers.ModelSerializer):
	firm_name = serializers.SerializerMethodField()

	class Meta:
		model = models.Specification
		fields = ('id', 'year', 'name', 'firm_name', 'firm', 'created_time', 'created_by', 'updated_time', 'updated_by')

	def get_firm_name(self, obj):
		return obj.firm.name if obj.firm else None


class BoxTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.BoxType
		fields = '__all__'
