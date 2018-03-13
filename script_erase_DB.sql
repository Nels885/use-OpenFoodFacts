BEGIN TRANSACTION;

DELETE FROM assoc_product_category;
DELETE FROM backup;
DELETE FROM product;
DELETE FROM category;

SELECT setval('product_id_seq',1, false);
SELECT setval('category_id_seq', 1, false);
SELECT setval('backup_id_seq',1, false);

COMMIT;