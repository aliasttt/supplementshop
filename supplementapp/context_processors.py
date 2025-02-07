def cart_items_count(request):
    basket = request.session.get('basket', {})
    return {'cart_items_count': sum(basket.values())}
