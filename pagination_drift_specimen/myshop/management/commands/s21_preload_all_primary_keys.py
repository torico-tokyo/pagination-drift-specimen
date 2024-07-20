from django.core.management import BaseCommand
from django.core.paginator import Paginator
from ...models import Product


class Command(BaseCommand):
    """
    name に「不適切」が含まれる Product の active を False にする。

    パジネーションドリフトを避けるため、あらかじめ全ての対象レコードの PK を取得しておくパターン
    """
    help = 'name に「不適切」が含まれる Product の active を False にする'

    def handle(self, *args, **options):
        # 対象のレコードのプライマリーキーを全部取得する
        product_pks = list(Product.objects.filter(
            name__contains='不適切', active=True
        ).order_by('id').values_list('id', flat=True))

        # Paginator を使って1000件ごとに切り分けながら処理する
        paginator = Paginator(product_pks, 1000)

        for page_number in paginator.page_range:
            products = Product.objects.filter(
                id__in=paginator.page(page_number).object_list)
            for product in products:
                # 該当した Product を無効化する
                product.active = False
                product.save(update_fields=['active'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{product.id} {product.name} を無効化しました。'))
