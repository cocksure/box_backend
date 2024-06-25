from django.urls import path
from .views import BoxModelListCreate, BoxOrderDetailView, BoxOrderListCreate, ProcessLogView, PackagingView, \
	GenerateBoxOrderPDFView, generate_production_order_pdf

app_name = 'production'

urlpatterns = [
	path('boxmodels/', BoxModelListCreate.as_view(), name='boxmodel-list'),
	path('boxorders/', BoxOrderListCreate.as_view(), name='boxorder-list'),
	path('boxorder/<int:pk>/', BoxOrderDetailView.as_view(), name='boxorder-detail'),
	path('process-logs/', ProcessLogView.as_view(), name='process_log'),
	path('packaging/', PackagingView.as_view(), name='packaging'),

	# pdf
	path('boxorder/<int:order_id>/pdf/', GenerateBoxOrderPDFView.as_view(), name='generate_box_order_pdf'),
	path('productionorder/<int:production_order_id>/pdf/', generate_production_order_pdf,
		 name='generate_production_order_pdf'),
]
