CREATE TABLE IF NOT EXISTS users (
    username        VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    password    VARCHAR(50)     NOT NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS topics (
    id_topic     INTEGER PRIMARY KEY AUTOINCREMENT,
    title       VARCHAR(50)     NOT NULL,
    content     TEXT            NOT NULL,
    votes       INTEGER         NOT NULL DEFAULT 0,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username    VARCHAR(50)     NOT NULL,
    FOREIGN KEY (username) REFERENCES user(username)
);
