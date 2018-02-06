
CREATE SEQUENCE public.store_id_seq;

CREATE TABLE public.store (
                id INTEGER NOT NULL DEFAULT nextval('public.store_id_seq'),
                name VARCHAR(300),
                CONSTRAINT store_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.store_id_seq OWNED BY public.store.id;

CREATE TABLE public.categorie (
                id INTEGER NOT NULL,
                name VARCHAR(300) NOT NULL,
                CONSTRAINT categorie_pk PRIMARY KEY (id)
);


CREATE TABLE public.product (
                product_id INTEGER NOT NULL,
                ingredient VARCHAR(1000),
                product_name VARCHAR(300) NOT NULL,
                nutrition_grade VARCHAR(1) NOT NULL,
                url VARCHAR(1000) NOT NULL,
                categorie_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                CONSTRAINT product_pk PRIMARY KEY (product_id)
);


CREATE SEQUENCE public.backup_number_seq;

CREATE TABLE public.backup (
                number INTEGER NOT NULL DEFAULT nextval('public.backup_number_seq'),
                product_id INTEGER NOT NULL,
                CONSTRAINT backup_pk PRIMARY KEY (number)
);


ALTER SEQUENCE public.backup_number_seq OWNED BY public.backup.number;

ALTER TABLE public.product ADD CONSTRAINT store_product_fk
FOREIGN KEY (store_id)
REFERENCES public.store (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.product ADD CONSTRAINT categorie_product_fk
FOREIGN KEY (categorie_id)
REFERENCES public.categorie (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.backup ADD CONSTRAINT product_backup_fk
FOREIGN KEY (product_id)
REFERENCES public.product (product_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
