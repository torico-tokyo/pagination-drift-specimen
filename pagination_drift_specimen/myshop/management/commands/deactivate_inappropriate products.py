from django.core.management import BaseCommand
from django.core.paginator import Paginator
from ...models import Product


class Command(BaseCommand):
    help = 'name に「不適切」が含まれる Product の active を False にする'

    def handle(self, *args, **options):

        chunk_size = 1000

        product_qs = Product.objects.filter(
            name__contains='不適切', active=True
        ).order_by('id')

        # Paginator を使って1000件ごとに SQL を発行する
        paginator = Paginator(product_qs, chunk_size)

        for page_number in paginator.page_range:
            for product in paginator.page(page_number).object_list:
                print(f'{page_number}, {product.id}')
                # product.active = False
                # product.save()
                # self.stdout.write(
                #     self.style.SUCCESS(f'{product} を非アクティブ化しました。'))
