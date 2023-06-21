CREATE TABLE IF NOT EXISTS user (
    id_user     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(50)     NOT NULL,
    email       VARCHAR(50)     NOT NULL UNIQUE,
    password    VARCHAR(50)     NOT NULL,
    created_at  DATETIME        NOT NULL,
    updated_at  DATETIME        NOT NULL
);

CREATE TABLE IF NOT EXISTS topics (
    id_post     INTEGER PRIMARY KEY AUTOINCREMENT,
    title       VARCHAR(50)     NOT NULL,
    content     TEXT            NOT NULL,
    votes       INTEGER         NOT NULL DEFAULT 0,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_user     INTEGER         NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);
