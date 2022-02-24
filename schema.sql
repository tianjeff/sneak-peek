DROP TABLE IF EXISTS sneakers;

CREATE TABLE sneakers(
    snkrid INT NOT NULL,
    snkrname VARCHAR(40) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    size INT NOT NULL,
    price INT NOT NULL,
    loc VARCHAR(20) NOT NULL,
    PRIMARY KEY(snkrid)
)