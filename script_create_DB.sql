CREATE SEQUENCE categorie_id_seq;

CREATE TABLE categorie (
                id INTEGER NOT NULL DEFAULT nextval('categorie_id_seq'),
                name TEXT NOT NULL,
                PRIMARY KEY(id)
);


CREATE SEQUENCE product_id_seq;

CREATE TABLE product (
                id INTEGER NOT NULL DEFAULT nextval('product_id_seq'),
                product_name TEXT NOT NULL,
                quantite TEXT,
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
                PRIMARY KEY(id),
                FOREIGN KEY(product_id) REFERENCES product(id)
);

CREATE TABLE assoc_product_categorie (
                product_id INTEGER NOT NULL,
                categorie_id INTEGER NOT NULL,
                PRIMARY KEY(product_id,categorie_id),
                FOREIGN KEY(product_id) REFERENCES product(id),
                FOREIGN KEY(categorie_id) REFERENCES categorie(id)
);