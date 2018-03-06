BEGIN TRANSACTION;

DELETE FROM assoc_product_categorie;
DELETE FROM backup;
DELETE FROM product;
DELETE FROM categorie;

SELECT setval('product_id_seq',1, false);
SELECT setval('categorie_id_seq', 1, false);
SELECT setval('backup_id_seq',1, false);

COMMIT;