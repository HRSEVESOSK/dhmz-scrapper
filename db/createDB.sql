CREATE TABLE IF NOT EXISTS
    "meteodb"."public".grad
    (
        oid bigserial NOT NULL,
        id CHARACTER VARYING(256) NOT NULL,
        geom geometry NOT NULL,
        metadata jsonb,
        PRIMARY KEY (oid),
        CONSTRAINT grad_id_ix1 UNIQUE (id)
    )
;
CREATE TABLE IF NOT EXISTS
    "meteodb"."public".observation
    (
        oid bigserial NOT NULL,
        time timestamp NOT NULL,
        grad_ref bigint NOT NULL,
        data jsonb NOT NULL,
        PRIMARY KEY (oid),
        CONSTRAINT observation_fk1 FOREIGN KEY (grad_ref) REFERENCES
        "meteodb"."public"."grad" ("oid")
    )
;