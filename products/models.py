from django.core.cache import cache
import json
from datetime import datetime

class Product:
    def __init__(self, product_name, category_id, price, link, image_url, delivery_charge=0, created_at=None, updated_at=None, is_deleted=False):
        self.product_name = product_name
        self.category_id = category_id
        self.price = price
        self.link = link
        self.image_url = image_url
        self.delivery_charge = delivery_charge
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.is_deleted = is_deleted

    def to_dict(self):
        return {
            'product_name': self.product_name,
            'category_id': self.category_id,
            'price': self.price,
            'link': self.link,
            'image_url': self.image_url,
            'delivery_charge': self.delivery_charge,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_name=data['product_name'],
            category_id=data['category_id'],
            price=data['price'],
            link=data['link'],
            image_url=data['image_url'],
            delivery_charge=data.get('delivery_charge', 0),
            created_at=datetime.fromisoformat(data['created_at']) if data['created_at'] else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data['updated_at'] else None,
            is_deleted=data.get('is_deleted', False)
        )

class ProductManager:
    @classmethod
    def save_to_redis(cls, search_url, products):
        key = search_url
        products_data = [product.to_dict() for product in products]     #products 는 JSON
        cache.set(key, json.dumps(products_data))                       #products_data 를 JSON 으로 바꿔서 저장

    @classmethod
    def get_from_redis(cls, search_url):
        key = search_url
        products_data = cache.get(key)
        if products_data:
            products_list = json.loads(products_data)
            return [Product.from_dict(product) for product in products_list]
        return None

    @classmethod
    def exists_in_redis(cls, search_url):
        key = search_url
        return cache.get(key) is not None
