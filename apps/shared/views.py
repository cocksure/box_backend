from rest_framework import generics
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.shared.utils import CustomPagination


class BaseListView(generics.ListAPIView):
	queryset = None
	serializer_class = None
	pagination_class = CustomPagination

	def perform_create(self, serializer):
		serializer.save()

	def get(self, request, *args, **kwargs):
		page_size = request.query_params.get('page_size', None)
		if page_size:
			self.pagination_class.page_size = page_size
		return self.list(request, *args, **kwargs)


class BaseCreateView(CreateAPIView):

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
