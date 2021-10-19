from . models import Category, ShopCart


def cat(request):
    categories=Category.objects.all

    context={
        'categories':categories
    }

    return context #also a need to register this cpontext type in the settings


def cartread(request):
    cartread = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)
    itemread = 0 #This is initialising a variable command. giving it a start-up number zero
    for item in cartread:
        itemread +=item.quantity

    context = {
        'itemread': itemread 
    }

    return context     