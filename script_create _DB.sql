CREATE SEQUENCE store_id_seq;

CREATE TABLE store (
                id INTEGER NOT NULL DEFAULT nextval('store_id_seq'),
                name TEXT NOT NULL,
                PRIMARY KEY(id)
);

CREATE UNIQUE INDEX store_idx ON store (name);


CREATE SEQUENCE categorie_id_seq;

CREATE TABLE categorie (
                id INTEGER NOT NULL DEFAULT nextval('categorie_id_seq'),
                name TEXT NOT NULL,
                PRIMARY KEY(id)
);

CREATE UNIQUE INDEX categorie_idx ON categorie(name);


CREATE SEQUENCE product_id_seq;

CREATE TABLE product (
                id INTEGER NOT NULL DEFAULT nextval('product_id_seq'),
                product_name TEXT NOT NULL,
                ingredient TEXT,
                quantite TEXT,
                nutrition_grade TEXT,
                url TEXT,
                PRIMARY KEY(id)
);

CREATE UNIQUE INDEX product_idx ON product(product_name);

CREATE SEQUENCE backup_number_seq;

CREATE TABLE backup (
                number INTEGER NOT NULL DEFAULT nextval('backup_number_seq'),
                product_id INTEGER NOT NULL,
                PRIMARY KEY(number),
                FOREIGN KEY(product_id) REFERENCES product(id)
);

CREATE TABLE assoc_product_categorie (
                product_id INTEGER NOT NULL,
                categorie_id INTEGER NOT NULL,
                PRIMARY KEY(product_id,categorie_id),
                FOREIGN KEY(product_id) REFERENCES product(id),
                FOREIGN KEY(categorie_id) REFERENCES categorie(id)
);

CREATE TABLE assoc_product_store (
                product_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                PRIMARY KEY(product_id, store_id),
                FOREIGN KEY(product_id) REFERENCES product(id),
                FOREIGN KEY(store_id) REFERENCES store(id)
);