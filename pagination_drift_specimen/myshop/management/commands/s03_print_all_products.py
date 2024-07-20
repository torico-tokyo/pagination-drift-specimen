from django.core.management import BaseCommand
from django.core.paginator import Paginator

from ...models import Product


class Command(BaseCommand):
    help = '全 Product を表示'

    def handle(self, *args, **options):

        paginator = Paginator(
            Product.objects.all().order_by('id'),
            1000
        )
        for page in [paginator.get_page(p) for p in paginator.page_range]:
            for product in page.object_list:
                print(f'id={product.id}, active={product.active},'
                      f' name={product.name}')
