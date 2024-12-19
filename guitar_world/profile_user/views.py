from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from catalog.models import Product, Order
from datetime import datetime

statuses = {
    "registration": "Оформление заказа",
    "dedlivery": "Доставка заказа",
    "done": "Заказ выполнен"
}

class ProfileAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'auth/login.html')
        get = request.GET
        if get.get("action") is not None:
            if get.get("action") == "logout":
                auth.logout(request)
                return HttpResponseRedirect("/auth/login")
        result = []
        for order in request.user.orders.all():
            change = False
            tempresult = []
            for item in order.products["cart"]:
                item = Product.objects.get(id=item)
                change = False
                for i in tempresult:
                    if item.id == i["id"]:
                        i["count"] += 1
                        change = True
                        break
                if change:
                    continue
                tempresult.append({"id": item.id, "name": item.name, "price": int(item.price), "count": 1})
            tempresult = {"products": tempresult, "status": statuses[order.status], "id": order.id, "general_sum": int(sum([i["price"]*i["count"] for i in tempresult]))}
            result.append(tempresult)
        return render(request, 'profile/index.html', context={"orders": result})
    
    def post(self, request):
        post = request.POST
        for key in ["first_name", "last_name", "city", "street", "house"]:
            if " " in post.get(key, " "):
                return render(request, 'profile/index.html', context={"error": "Поля не могут содержать пробелы или быть пустыми"})
        
        if not post.get("house").isdigit():
            return render(request, 'profile/index.html', context={"error": "Поле 'Дом/Квартира' должен быть числом"})
        
        request.user.first_name = post.get("first_name")
        request.user.last_name = post.get("last_name")
        request.user.city = post.get("city")
        request.user.street = post.get("street")
        request.user.house = post.get("house")
        request.user.save()

        return render(request, 'profile/index.html')

class CartAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'auth/login.html')
        
        postprocess = []
        for item in request.user.cart["cart"]:
            product = Product.objects.get(id=item)
            postprocess.append({"id": product.id, "name": product.name, "price": product.price, "count": 1})
        change = False
        result = []
        for item in postprocess:
            change = False
            for i in result:
                if item["id"] == i["id"]:
                    i["count"] += 1
                    change = True
                    break
            if change:
                continue
            result.append({"id": item["id"], "name": item["name"], "price": item["price"], "count": 1})
        
        address = f"г.{request.user.city}, ул.{request.user.street} {request.user.house}"
        addressValid = True

        if None in [request.user.city, request.user.street, request.user.house]:
            address = "Что бы сделать заказ укажите адресс доставки в настройках профиля"
            addressValid = False

        return render(request, 'profile/cart.html', context={"items_cart": result, "empty": (not result), "address": address, "address_valid": addressValid})

class NewOrderAPIView(APIView):
    def get(self, request):
        neworder = Order.objects.create(
            products=request.user.cart,
            ordered_date=datetime.now(),
            status="registration",
            user=request.user
        )
        request.user.cart = {"cart": []}
        request.user.orders.add(neworder)
        request.user.save()

        return render(request, 'profile/success_new_order.html')

class OrderAPIView(APIView):
    def get(self, request, id):
        resultOrder = Order.objects.filter(id=id)
        if not resultOrder.exists():
            return HttpResponseRedirect("/")
        resultOrder = resultOrder.first()
        if resultOrder.user.id != request.user.id and not request.user.is_staff:
            return HttpResponseRedirect("/")

        products = resultOrder.products["cart"]
        result = {}

        for item in products:
            if item in result:
                result[item]["count"] += 1
            else:
                product = Product.objects.get(id=item)
                result[item] = {"count": 1}
                result[item].update({"name": product.name, "price": product.price})
        resultOrder.status = statuses[resultOrder.status]
        total_price = sum([result[product]["price"]*result[product]["count"] for product in result])
        return render(request, 'profile/order.html', context={"order": resultOrder, "products": [result[item] for item in result], "total_price":total_price})

    def post(self, request, id):
        if not request.POST.get("status") in ["registration", "dedlivery", "done"] or not request.user.is_staff:
            return HttpResponseRedirect("/")

        order = Order.objects.get(id=id)
        order.status = request.POST.get("status")
        order.save()
        return HttpResponseRedirect("/admin_panel/")