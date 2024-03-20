import os

from django.core.files import File
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from products.models import ProductImage, Product, Category, Attribute, AttributeValue

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# test
# SPREADSHEET_ID = '1Df9CJ6iXvyWivpfTk_incYbGOFN9LJ9dJTcWpMnA9Ic'
# prod
SPREADSHEET_ID = '1MUniKMAvwdIorThCS3sPT0QuJF1GN43rksxrvqifCVk'
RANGE_NAME = 'Sheet1'
SERVICE_ACCOUNT_FILE = 'zharimvarim-1ff09cae89ed.json'


def authenticate_google_sheets_with_service_account(json_file_path, scopes):
	"""Аутентификация в Google Sheets с использованием сервисного аккаунта."""
	credentials = service_account.Credentials.from_service_account_file(json_file_path, scopes=scopes)
	service = build('sheets', 'v4', credentials=credentials)
	return service


def read_sheet_data(service, spreadsheet_id, range_name):
	"""Чтение данных из Google Sheets."""
	try:
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
		data = result.get('values', [])
		return data[1:]
	except HttpError as e:
		print(e)
		return None


def get_row_data(row):
	data = {
		'sku': None,
		'category_name': None,
		'title': None,
		'weight': None,
		'drink_value': None,
		'regular_price': None,
		'discount_price': None,
		'description': row[7] if len(row) > 7 and row[7] else '',
		'image': None
	}
	
	try:
		data['sku'] = row[0]
		data['category_name'] = row[1]
		data['title'] = row[2]
		data['weight'] = row[3] if row[3] else None
		data['drink_value'] = row[4]
		data['regular_price'] = row[5]
		data['discount_price'] = row[6]
		data['description'] = row[7]
		data['image'] = row[8]
	except IndexError:
		pass
	
	return data


def convert_to_float(value):
	if value=='':
		return 69
	try:
		return float(value.replace(',', '.'))
	except (ValueError, AttributeError):
		return None


def get_image_path(image_name):
	if image_name:
		image_path = os.path.join('importing', 'resized', f'{image_name}.jpg')
		if os.path.exists(os.path.join('media', image_path)):
			return image_path
	return 'placeholder.webp'


def create_or_update_attributes(product, row_data):
	drink_value = row_data['drink_value']
	attribute_prices = row_data['regular_price']
	if drink_value and attribute_prices:
		drink_values = drink_value.split('/')
		prices = attribute_prices.split('/')
		
		if len(drink_values)==len(prices):
			attribute, _ = Attribute.objects.get_or_create(name='Объем', category=product.category)
			
			for value, price in zip(drink_values, prices):
				attribute_value, _ = AttributeValue.objects.get_or_create(
					attribute=attribute,
					value=value,
					defaults={'price': convert_to_float(price)}
				)
				product.attribute_values.add(attribute_value)
		else:
			print(f"Несоответствие количества атрибутов и цен для товара: {product.title}")
	
	product.save()


def attach_image_to_product(product, image_name):
	# Получаем существующий объект ProductImage для данного товара
	product_image = ProductImage.objects.filter(product=product).first()
	
	if image_name:
		image_path = os.path.join('importing', 'resized', f'{image_name}.jpg')
		if os.path.exists(os.path.join('media', image_path)):
			if product_image:
				pass
			else:
				with open(os.path.join('media', image_path), 'rb') as f:
					ProductImage.objects.create(
						product=product,
						alt_text=product.title,
						image=File(f, name=f'{image_name}.jpg')
					)
	else:
		if product_image:
			# Если объект ProductImage существует, устанавливаем изображение-заполнитель
			product_image.image = 'images/placeholder.webp'
			product_image.save()
		else:
			# Если объект ProductImage не существует, создаем новый с изображением-заполнителем
			ProductImage.objects.create(
				product=product,
				alt_text=product.title,
				image='images/placeholder.webp'
			)


def create_or_update_product(row_data):
	sku = row_data['sku']
	category_name = row_data['category_name']
	title = row_data['title']
	weight = row_data['weight']
	# Получаем первое значение цены после разделения по "/"
	regular_price_str = row_data['regular_price'].split("/")[0]
	regular_price = convert_to_float(regular_price_str)
	
	# Получаем первое значение цены со скидкой после разделения по "/"
	discount_price_str = row_data['discount_price'].split("/")[0] if row_data['discount_price'] else None
	discount_price = convert_to_float(discount_price_str) if discount_price_str else None
	
	description = row_data['description']
	image = row_data['image']
	
	# Получаем или создаем категорию
	category, _ = Category.objects.get_or_create(name=category_name)
	
	# Создаем или обновляем товар
	product, created = Product.objects.update_or_create(
		sku=sku,
		defaults={
			'title': title,
			'category': category,
			'description': description,
			'regular_price': regular_price,
			'discount_price': discount_price,
			'weight': weight,
		}
	)
	image_name = row_data['image']
	attach_image_to_product(product, image_name)
	create_or_update_attributes(product, row_data)


def main():
	service = authenticate_google_sheets_with_service_account(SERVICE_ACCOUNT_FILE, SCOPES)
	data = read_sheet_data(service, SPREADSHEET_ID, RANGE_NAME)
	
	if data:
		for row in data:
			row_data = get_row_data(row)
			create_or_update_product(row_data)


if __name__=='__main__':
	main()
