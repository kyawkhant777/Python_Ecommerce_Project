from shop_app.models import Category,Cart

def category(request):
    category = Category.objects.all()
    return {'cat':category}

def cartCount(request):
    count = Cart.objects.filter(user_id=request.user.id).count()
    return {'count':count}
