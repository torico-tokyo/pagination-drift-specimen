# 解説

データベースに記録してある大量のデータを一括で処理する際に発生しがちなパターンとして以下のものがあります。

- 対象データが大量(10万件とか)のため、アプリケーション側でループを書き、1回のループ内では対象データを `LIMIT 1000 OFFSET ... ` のSQLで取得する
- アプリケーション側での処理で、処理対象のデータの抽出SQL の `WHERE` 句の条件を、条件に当てはまらないように `UPDATE` する

このような処理を書いてしまうと、ループで全対象データを全て処理できずに漏れが発生します。


そのような現象を、 Pagination Drift (パジネーションドリフト) と呼ぶようです。

この Django プロジェクトは、パジネーションドリフトの再現と対策を書いたものです。


# コードの説明

## モデル

[myshop/models.py](pagination_drift_specimen/myshop/models.py)

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
```

## 失敗コード
パジネーションドリフトの不具合が含まれています。

- [s11_deactivate_inappropriate_products.py](pagination_drift_specimen/myshop/management/commands/s11_deactivate_inappropriate_products.py)

## 対策したコード

- [s21_preload_all_primary_keys.py](pagination_drift_specimen/myshop/management/commands/s21_preload_all_primary_keys.py)
- [s22_segmented_by_product_pk.py](pagination_drift_specimen/myshop/management/commands/s22_segmented_by_product_pk.py)
- [s23_filter_last_pk.py](pagination_drift_specimen/myshop/management/commands/s23_filter_last_pk.py)

# 環境構築

```shell
$ pipenv install
$ cd pagination_drift_specimen
$ ./manage.py migrate
```

# 実行

## 失敗コード

```shell
$ ./manage.py s01_refresh_products
```
10000 の Product を作ります。
その内半分は、商品名に「不適切」という文言が含まれます。

```shell
$ ./manage.py s02_active_inactive_counts
active=True, Count: 10000
```
全商品を対象に、 active 別に件数を表示します。

```shell
$ ./manage.py s11_deactivate_inappropriate_products
...
... 商品 10000 この商品は不適切です。 を無効化しました。

$ ./manage.py s02_active_inactive_counts
active=False, Count: 3000
active=True, Count: 7000
```

本来、5000件ある対象商品を無効化するスクリプトですが、パジネーションドリフトが発生するため3000件しか処理できていません。

## 対策したコード

```shell
$ ./manage.py s01_refresh_products

$ ./manage.py s02_active_inactive_counts
active=True, Count: 10000

$ ./manage.py s21_preload_all_primary_keys

$ ./manage.py s02_active_inactive_counts
active=False, Count: 5000
active=True, Count: 5000
```
