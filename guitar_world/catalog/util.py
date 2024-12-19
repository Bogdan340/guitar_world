from .models import Order, Product
from datetime import datetime, timedelta

def getWeekPopularProducts():
    products = {product.id: {"product": product, "count": 0} for product in Product.objects.all()}

    for order in Order.objects.filter(ordered_date__range=(datetime.now() - timedelta(days=7), datetime.now()+timedelta(days=1))):
        for item_id in order.products["cart"]:
            if item_id not in products:
                continue
            products[item_id]["count"] += 1
    
    return products