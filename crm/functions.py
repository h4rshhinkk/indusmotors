from masters.models import Stock


def get_stock_in_optlist(variant):
    stock_count = Stock.objects.filter(variant=variant).exclude(is_chassis_blocked=True).count()
    return stock_count
