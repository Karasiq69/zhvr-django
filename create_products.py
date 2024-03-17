from django.core.files import File
from os import listdir
from random import choice

from products.models import Product, Category, ProductImage

# Путь к директории с фотографиями
image_dir = "D:\\zharvar\\django\\backend\\media\\menu_images"

# Получаем список файлов в директории
image_files = listdir(image_dir)

# Создаем 100 товаров
for i in range(1, 101):
	# Выбираем случайную категорию (предполагая, что у вас есть категории с id от 1 до 4)
	category = Category.objects.get(id=choice(range(1, 5)))
	
	# Создаем новый товар
	product = Product(
		title=f"Товар {i}",
		category=category,
		description="Описание товара",
		regular_price=100.00,
		is_active=True
	)
	product.save()
	
	# Выбираем случайное изображение из директории
	image_file = choice(image_files)
	
	# Создаем новый экземпляр модели ProductImage и привязываем его к товару
	product_image = ProductImage(product=product, is_feature=True)
	
	# Открываем изображение и присваиваем его полю image экземпляра ProductImage
	with open(f"{image_dir}\\{image_file}", "rb") as f:
		product_image.image.save(image_file, File(f))
	
	# Сохраняем экземпляр ProductImage
	product_image.save()