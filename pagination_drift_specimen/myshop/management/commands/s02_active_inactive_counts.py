from django.core.management import BaseCommand
from django.db.models import Count
from ...models import Product


class Command(BaseCommand):
    help = 'Product の active 別に件数を表示する'

    def handle(self, *args, **options):
        qs = Product.objects.values('active').annotate(
            count=Count('active')).order_by('active')

        for r in qs:
            print(f"active={r['active']}, Count: {r['count']}")
