from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .util import getWeekPopularProducts

class IndexAPIView(APIView):
    def get(self, request):
        top3product = getWeekPopularProducts()
        result = []
        for product in top3product:
            result.append(top3product[product])
        result = list(filter(lambda x: x["count"], result))[0:3]
        return render(request, 'catalog/index.html', context={'products': result})
    
class CatalogAPIView(APIView):
    def get(self, request):
        pages = False
        countPages = 0
        filtred = False
        get = request.GET
        for arg in [get.get("category")]:
            if arg is not None:
                filtred = True
                break
        
        if not filtred:
            return render(request, 'catalog/catalog.html')
        
        allProduct = Product.objects.all()
        
        if get.get("category", "") != "" and get.get("category") != "all":
            allProduct = Product.objects.filter(category=get.get("category"))
        
        if get.get("search", "") != "":
            searchWords = get.get("search")
            allProduct = allProduct.filter(name__icontains=searchWords)
        
        if get.get("toPrice", "").isdigit() or get.get("fromPrice", "").isdigit():
            toPrice = int(get.get("toPrice", "")) if get.get("toPrice", "").isdigit() else 9999999
            fromPrice = int(get.get("fromPrice", "")) if get.get("fromPrice", "").isdigit() else 0
            allProduct = allProduct.filter(price__range=(fromPrice, toPrice))
        
        if get.get("filter", "") in ["fromA2Z", "fromZ2A"]:
            allProduct = allProduct.order_by("name" if get.get("filter", "") == "fromA2Z" else "-name")
        
        if get.get("filter", "") in ["lowPrice", "highPrice"]:
            allProduct = allProduct.order_by("price" if get.get("filter", "") == "lowPrice" else "-price")

        for product in allProduct:
            in_cart = request.user.cart["cart"]
            product.in_cart_count = in_cart.count(product.id)
            product.in_cart = product.in_cart_count != 0

        
        paginator = Paginator(allProduct, 3)
        
        if len(allProduct) > 3:
            if len(allProduct) / 3 % 1 != 0:
                countPages = int(len(allProduct) / 3) + 1
            else:
                countPages = int(len(allProduct) / 3)
            pages = True
        if get.get("page", "").isdigit():
            allProduct = paginator.page(int(get.get("page", "")))
        else:
            allProduct = paginator.page(1)

        for product in allProduct:
            if product.id in request.user.cart["cart"]:
                product.countInCart = request.user.cart["cart"].count(product.id)
            else:
                product.countInCart = 0

        return render(request, 'catalog/products.html', context={"products": allProduct, "filter": get.get("filter", ""), "category": get.get("category"), "pages": pages, "count_pages": range(1, countPages+1)})
    
class AddIncartAPIView(APIView):
    def get(self, request):
        if request.GET.get("product") is None:
            return Response({"status": "error", "message": "Не указан продукт"})
        
        product = Product.objects.filter(id=request.GET.get("product"))
        if not product.exists():
            return Response({"status": "error", "message": "Продукт не найден"})
        
        user = request.user
        if not user.cart:
            user.cart = {"cart": []}
        user.cart["cart"].append(product.first().id)
        user.save()
        
        return Response({"status": "success"})
       
class MinusCartAPIView(APIView):
    def get(self, request):
        if request.GET.get("product") is None:
            return Response({"status": "error", "message": "Не указан продукт"})
        
        user = request.user
        if not user.cart:
            user.cart = {"cart": []}
        
        if int(request.GET.get("product")) in user.cart["cart"]:
            user.cart["cart"].remove(int(request.GET.get("product")))
            user.save()
        return Response({"status": "success"})

class ProductDetailAPIView(APIView):
    def get(self, request, id=None):
        if id is None:
            return Response({"status": "error", "message": "Не указан продукт"})

        product = Product.objects.filter(id=id)
        if not product.exists():
            return Response({"status": "error", "message": "Продукт не найден"})
        return render(request, 'catalog/product_detail.html', context={"product": product.first()})