from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from catalog.util import getWeekPopularProducts
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from .forms import UpdateProductForm
from catalog.models import Order, Product
from feedback.models import Quest, Chat


class MainPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        topWeek = getWeekPopularProducts()
        generalCount = sum([topWeek[product]["count"] for product in topWeek])
        for product in topWeek:
            topWeek[product].update({"proc": topWeek[product]["count"]/generalCount})
            topWeek[product].update({"summa": int(topWeek[product]["count"]*topWeek[product]["product"].price)})
        
        generalSumma = sum([topWeek[product]["summa"] for product in topWeek])

        for product in topWeek:
            topWeek[product].update({"proc_summa": int(topWeek[product]["summa"])/generalSumma})
        
        topWeek = [topWeek[value] for value in topWeek]
        topWeek = sorted(topWeek, key=lambda x: x["count"], reverse=True)
        for index, value in enumerate(topWeek):
            value.update({"id_top": index+1})

        topWeekSumma = sorted(topWeek, key=lambda x: x["summa"], reverse=True)
        for index, value in enumerate(topWeekSumma):
            value["id_top"] = index+1

        return render(request, "admin_panel/index.html", context={"top_week_diagram": topWeek, "top_week_diagram_summa": topWeekSumma})

class OrdersPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        orders = Order.objects.all()

        return render(request, "admin_panel/orders.html", context={"orders": orders})

class ProductsPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        products = Product.objects.all()
        return render(request, "admin_panel/products.html", context={"products": products})

class UpdatePrductPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        product = Product.objects.get(id=id)
        initialValues = {
            "name": product.name,
            "price": int(product.price),
            "description": product.description,
            "category": product.category,
        }
        return render(request, "admin_panel/update_product.html", context={"form": UpdateProductForm(initial=initialValues)})

    def post(self, request, id):
        product = Product.objects.get(id=id)

        form = UpdateProductForm(request.POST, instance=product)
        if not form.is_valid():
            return render(request, "admin_panel/update_product.html", context={"form": form, "errors": form.errors})
        form.save()
        return render(request, "admin_panel/update_product.html", context={"form": form, "message": "Product updated"})

class QuestionPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        questions = Quest.objects.all()
        for question in questions:
            question.answer = question.answer != None
        return render(request, "admin_panel/questions.html", context={"questions": questions})

class QuestPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        question = Quest.objects.get(id=id)
        return render(request, "admin_panel/quest.html", context={"question": question})
    def post(self, request, id):
        question = Quest.objects.get(id=id)
        answer = request.POST["answer"]
        question.answer = answer
        question.save()

        send_mail(
            f'Дан ответ на вопрос №{question.id}',
            f'На ваш вопрос "{question.question}" был дан ответ:\n"{answer}"',
            'guitar.world.project.23@gmail.com',
            [question.email],
        )

        return HttpResponseRedirect("/admin_panel/question")

class ChatsPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request, "admin_panel/chats.html", context={"chats": Chat.objects.all()})

class ChatPageAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        chat = Chat.objects.get(id=id)
        result_messages = []
        for message in chat.messages:
            is_my_message = message.split("__")[0] == str(request.user.id)
            result_messages.append({"text": chat.messages[message], "classText": "my" if is_my_message else "other",
                                    "classParentDiv": "my-parent-div" if is_my_message else ""})
        chat.messages = result_messages
        return render(request, "admin_panel/chat.html", context={"room_name": chat.user.id, "chat": chat})

class ProductsDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return HttpResponseRedirect('/admin_panel/products')

class ProductsCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request, "admin_panel/update_product.html", context={"form": UpdateProductForm()})

    def post(self, request):
        form = UpdateProductForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "admin_panel/update_product.html", context={"form": form, "errors": form.errors})
        form.save()
        return HttpResponseRedirect("/admin_panel/products")