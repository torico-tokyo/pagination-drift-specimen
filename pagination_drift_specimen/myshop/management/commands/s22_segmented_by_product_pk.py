from django.core.management import BaseCommand
from django.db.models import Min, Max

from ...models import Product


class Command(BaseCommand):
    """
    name に「不適切」が含まれる Product の active を False にする。

    product の PK で範囲わけするパターン
    """
    help = 'name に「不適切」が含まれる Product の active を False にする'

    def handle(self, *args, **options):
        aggregated = Product.objects.aggregate(
            min_id=Min('id'), max_id=Max('id'))

        product_qs = Product.objects.filter(
            name__contains='不適切', active=True
        ).order_by('id')

        page_size = 2000
        for offset in range(
            aggregated['min_id'], aggregated['max_id'] + 1, page_size
        ):
            products = product_qs.filter(
                id__gte=offset, id__lt=offset + page_size)

            for product in products:
                # 該当した Product を無効化する
                product.active = False
                product.save(update_fields=['active'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{product.id} {product.name} を無効化しました。'))
