from django.urls import path
from apps.depo.views import outgoing, stock, incoming

app_name = 'depo'

urlpatterns = [
	path('incoming/', incoming.IncomingListView.as_view(), name='incoming-list'),
	path('incoming/create/', incoming.IncomingCreateView.as_view(), name='incoming-create'),
	path('incoming/detail/<int:pk>/', incoming.IncomingDetailView.as_view(), name='incoming-detail'),

	path('outgoing/', outgoing.OutgoingListView.as_view(), name='outgoing-list'),
	path('outgoing/create/', outgoing.OutgoingCreateView.as_view(), name='outgoing-create'),
	path('outgoing/detail/<int:pk>/', outgoing.OutgoingDetailView.as_view(), name='outgoing-detail'),

	path('stock/', stock.StockListView.as_view(), name='stock-list'),
	path('stock-detail/<int:pk>/', stock.StockDetailView.as_view(), name='stock-detail'),

	path('unaccepted-materials/', stock.UnacceptedMaterialsListView.as_view(), name='unaccepted-materials-list'),
	path('unaccepted-materials/<int:outgoing_id>/', stock.UnacceptedMaterialsDetailView.as_view(),
		 name='unaccepted-material-detail'),
]
