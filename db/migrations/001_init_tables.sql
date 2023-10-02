DROP TABLE IF EXISTS tg_users, students, groups, admin;

CREATE TABLE tg_users (
        tg_id int8 PRIMARY KEY,
        tg_username varchar(255),
        first_name varchar(255),
        last_name varchar(255),
        is_blocked bool NOT NULL DEFAULT FALSE
);

CREATE TABLE admin (
        admin_id int generated by default as identity PRIMARY KEY,
        tg_id int8 REFERENCES tg_users(tg_id) ON DELETE CASCADE,
        UNIQUE (tg_id)
);