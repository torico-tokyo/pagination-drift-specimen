from django.core.management import BaseCommand

from ...models import Product


def make_product_name(i):
    """
    テキトーな商品名を作成。iが偶数の場合、「この商品は不適切です。」という文言が入る。
    """
    if i % 2 == 0:
        return f'商品 {i} この商品は不適切です。'
    else:
        return f'商品 {i}'


class Command(BaseCommand):
    help = 'ダミー Product を10000個作成'

    def handle(self, *args, **options):
        Product.objects.all().delete()

        Product.objects.bulk_create(
            [
                Product(name=make_product_name(i))
                for i in range(1, 10001)
            ]
        )
