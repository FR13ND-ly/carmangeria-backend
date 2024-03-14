from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Product, Order, File, OrderProduct, Email, News
from rest_framework import status
import os 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@csrf_exempt
def getAllProducts(request):
    res = []
    for product in Product.objects.all():
        res.append({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "type": product.type,
            "date": product.date,
            "imageId": product.imageId,
            "imageUrl": getFile(product.imageId)
        })
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def getProductsById(request):
    data = JSONParser().parse(request)
    res = []
    for item in data:
        product = Product.objects.get(id = item["productId"])
        res.append({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "type": product.type,
            "date": product.date,
            "imageUrl": getFile(product.imageId),
            "amount": item["amount"]
        })
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def addProduct(request):
    data = JSONParser().parse(request)
    Product.objects.create(
        title = data["title"],
        description = data["description"],
        type = data["type"],
        imageId = data["imageId"],
        price = data["price"],
    ).save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
    

@csrf_exempt
def updateProduct(request):
    data = JSONParser().parse(request)
    product = Product.objects.get(id = data["id"])
    product.title = data["title"]
    product.description = data["description"]
    product.type = data["type"]
    product.imageId = data["imageId"]
    product.price = data["price"]
    product.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
    
    
@csrf_exempt
def deleteProduct(request, id):
    Product.objects.get(id = id).delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)

def getAllOrders(request):
    res = []
    for order in Order.objects.all().order_by("deliveryDate"):
        item = {
            "id": order.id,
            "name": order.name,
            "phone": order.phone,
            "completed": order.completed,
            "email": order.email,
            "message": order.message,
            "deliveryDate": order.deliveryDate,
            "date": order.date,
            "products": []
        }
        for orderP in OrderProduct.objects.filter(orderId = order.id):
            product = Product.objects.get(id = orderP.productId)
            item["products"].append({
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "type": product.type,
                "price": orderP.price,
                "date": product.date,
                "imageUrl": getFile(product.imageId),
                "amount": orderP.amount,
            })
        res.append(item)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def addOrder(request):
    data = JSONParser().parse(request)
    info = data["data"]
    email = {
        "order": {
            "name": info["name"],
            "phone": info["phone"],
            "email": info["email"],
            "message": info.get("message", ""),
            "deliveryDate": info["deliveryDate"],
        },
        "items": [],
        "total": 0
    }
    order = Order.objects.create(
        name = info["name"],
        phone = info["phone"],
        email = info["email"],
        message = info.get("message", ""),
        deliveryDate = info["deliveryDate"],
    )
    order.save()
    orderItems = []
    for data in data["products"]:
        product = Product.objects.get(id = data["productId"])
        orderItem = OrderProduct.objects.create(
            orderId = order.id,
            productId = product.id,
            amount = data["amount"],
            price = product.price
        )
        orderItem.save()
        orderItems.append(orderItem)
        email["items"].append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "totalPrice": product.price * data["amount"],
            "amount": data["amount"]
        })
        email["total"] += data["amount"] * product.price
    if info['email']:
        sendEmail(email)
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
    

def completeOrder(request, id):
    order = Order.objects.get(id = id)
    order.completed = True
    order.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteOrder(request, id):
    for product in OrderProduct.objects.filter(orderId = id):
        product.delete()
    Order.objects.get(id = id).delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def addFile(request):
    file = File.objects.create(file=request.FILES['file'])
    file.save()
    return JsonResponse(file.id, status=status.HTTP_200_OK, safe=False)


def getFile(id, path=""):
    if File.objects.filter(id=id).exists():
        return settings.API_URL + "/media/" + path + os.path.basename(File.objects.get(id=id).file.name)
    else:
        return ""
    

def getDashboard(request):
    res = {
        "productsCount": Product.objects.all().count(),
        "ordersCount": Order.objects.filter(completed = False).count(),
        "email": Email.objects.all()[0].email,
        "news": News.objects.all()[0].text
    }
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)
    
def setEmail(request, newEmail):
    email = Email.objects.all()[0]
    email.email = newEmail
    email.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)

def sendEmail(email):
    subject = 'Comandă nouă'
    customerMessage = render_to_string('customer_notification.html', email)
    orderMessage = render_to_string('order_notification.html', email)
    send_mail(
        subject = subject, 
        message="",
        html_message=customerMessage, 
        from_email='contact@carmangerialuigeo.ro', 
        recipient_list=[email["order"]["email"]]
    )
    send_mail(
        subject = subject, 
        message="",
        html_message=orderMessage, 
        from_email='contact@carmangerialuigeo.ro', 
        recipient_list=[Email.objects.all()[0].email]
    )


def getNews(request):
    res = News.objects.all()[0].text
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def setNews(request, text):
    news = News.objects.all()[0]
    news.text = text
    news.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)

def statistics(request):
    productsStats = {}
    usersStats = {}
    for product in Product.objects.all():
        productsStats[product.id] = {
            "title": product.title,
            "stats": []
        }
    for order in Order.objects.filter(completed = True):
        if usersStats.get(order.phone) == None:
            usersStats[order.phone] = {
                "name": order.name,
                "email": order.email,
                "stats": []
            }
        for orderProduct in OrderProduct.objects.filter(orderId = order.id):
            product = Product.objects.get(id = orderProduct.productId)

            productsStats[product.id]["stats"].append({
                "amount": orderProduct.amount,
                "price": orderProduct.price,
                "date": order.date
            })
            usersStats[order.phone]["stats"].append({
                "amount": orderProduct.amount,
                "price": orderProduct.price * orderProduct.amount,
                "date": order.date
            })

    res = {
        "productsStats": productsStats,
        "usersStats": usersStats,
    }
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)