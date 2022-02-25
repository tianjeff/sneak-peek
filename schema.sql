DROP TABLE IF EXISTS sneakers;
DROP TABLE IF EXISTS sales;

CREATE TABLE sneakers(
    snkrid INT NOT NULL,
    snkrname VARCHAR(40) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    size INT NOT NULL,
    price INT NOT NULL,
    loc VARCHAR(20) NOT NULL,
    PRIMARY KEY(snkrid)
);

CREATE TABLE sales(
    snkrid INT NOT NULL,
    snkrname VARCHAR(40) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    size INT NOT NULL,
    bought INT NOT NULL,
    sold INT NOT NULL,
    profit INT NOT NULL,
    PRIMARY KEY(snkrid)
);