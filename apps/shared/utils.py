from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
import qrcode
from io import BytesIO


class CustomPagination(PageNumberPagination):
	page_size = 20
	page_size_query_param = 'page_size'
	max_page_size = 50

	def get_paginated_response(self, data):
		return Response(OrderedDict([
			('count', self.page.paginator.count),
			('current_page', self.page.number),
			('total_pages', self.page.paginator.num_pages),
			('next', self.get_next_link()),
			('previous', self.get_previous_link()),
			('results', data)
		]))


def generate_qr_code(data):
	if not data:
		return None

	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(data)
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	buffer = BytesIO()
	img.save(buffer, format="PNG")
	qr_code_data = buffer.getvalue()

	return qr_code_data
