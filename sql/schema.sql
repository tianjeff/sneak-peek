PRAGMA foreign_keys = ON;

CREATE TABLE sneakers(
    snkrname VARCHAR(40) NOT NULL,
    sku VARCHAR(12) NOT NULL,
    imgname VARCHAR(40) NOT NULL,
    size INT NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY(sku)
)