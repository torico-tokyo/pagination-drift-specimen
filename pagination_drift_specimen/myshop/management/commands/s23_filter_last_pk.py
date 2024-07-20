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
        product_qs = Product.objects.filter(
            name__contains='不適切', active=True
        ).order_by('id')

        page_size = 1000
        last_max_id = 0

        while True:
            products = list(product_qs.filter(
                id__gt=last_max_id)[:page_size])

            if not products:
                break
            last_max_id = products[-1].id

            for product in products:
                # 該当した Product を無効化する
                product.active = False
                product.save(update_fields=['active'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{product.id} {product.name} を無効化しました。'))
