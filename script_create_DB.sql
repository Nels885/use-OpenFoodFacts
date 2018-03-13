CREATE SEQUENCE category_id_seq;

CREATE TABLE category (
                id INTEGER NOT NULL DEFAULT nextval('category_id_seq'),
                name TEXT NOT NULL,
                PRIMARY KEY(id)
);


CREATE SEQUENCE product_id_seq;

CREATE TABLE product (
                id INTEGER NOT NULL DEFAULT nextval('product_id_seq'),
                product_name TEXT NOT NULL,
                quantity TEXT,
                ingredient TEXT,
                nutrition_grade TEXT,
                url TEXT,
                stores TEXT,
                PRIMARY KEY(id)
);

CREATE SEQUENCE backup_id_seq;

CREATE TABLE backup (
                id INTEGER NOT NULL DEFAULT nextval('backup_id_seq'),
                product_id INTEGER NOT NULL,
                substituted_product TEXT,
                PRIMARY KEY(id),
                FOREIGN KEY(product_id) REFERENCES product(id)
);

CREATE TABLE assoc_product_category (
                product_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                PRIMARY KEY(product_id,category_id),
                FOREIGN KEY(product_id) REFERENCES product(id),
                FOREIGN KEY(category_id) REFERENCES category(id)
);