from django.core.management import BaseCommand
from django.core.paginator import Paginator
from ...models import Product


class Command(BaseCommand):
    """
    name に「不適切」が含まれる Product の active を False にする。
    """
    help = 'name に「不適切」が含まれる Product の active を False にする'

    def handle(self, *args, **options):
        product_qs = Product.objects.filter(
            name__contains='不適切', active=True
        ).order_by('id')

        # Paginator を使って1000件ごとに SQL を発行する
        paginator = Paginator(product_qs, 1000)

        for page_number in paginator.page_range:
            for product in paginator.page(page_number).object_list:
                # 該当した Product を無効化する
                product.active = False
                product.save(update_fields=['active'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{product.id} {product.name} を無効化しました。'))
