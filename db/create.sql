CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY (START WITH 1000) PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(256) NOT NULL,
    balance FLOAT DEFAULT 0.0 CHECK (balance >= 0.0)
);

CREATE TABLE Seller(
    user_id INTEGER NOT NULL PRIMARY KEY REFERENCES Users(id),
    seller_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Buyer(
    user_id INTEGER NOT NULL PRIMARY KEY REFERENCES Users(id)
);

CREATE TABLE Category(
    name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE Product(
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL REFERENCES Category(name),
    image_url VARCHAR(255) NOT NULL,
    available BOOLEAN NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE Selling(
    seller_id INT NOT NULL REFERENCES Seller(user_id),
    product_name VARCHAR(255) NOT NULL REFERENCES Product(name),
    price FLOAT NOT NULL,
    quantity_in_inventory INT NOT NULL,
    PRIMARY KEY(seller_id, product_name)
);

CREATE TABLE Orders (
    buyer_id INT NOT NULL REFERENCES Buyer(user_id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    seller_id INT NOT NULL REFERENCES Seller(user_id),
    product_name VARCHAR(255) NOT NULL REFERENCES Product(name),
    quantity INT NOT NULL,
    fulfillment_status BOOLEAN DEFAULT FALSE,
    detailed_product_link VARCHAR(255),
    final_price FLOAT NOT NULL,
    PRIMARY KEY(buyer_id, time_purchased, seller_id, product_name)
);

CREATE TABLE Product_Review (
    product_name VARCHAR(255) NOT NULL REFERENCES Product(name),
    buyer_id INT NOT NULL REFERENCES Buyer(user_id),
    rating INT NOT NULL,
    date DATE,
    upvote_count INT,
    downvote_count INT,
    PRIMARY KEY(product_name, buyer_id)
);

CREATE TABLE Seller_Review (
    buyer_id INT NOT NULL REFERENCES Buyer(user_id),
    seller_id INT NOT NULL REFERENCES Seller(user_id),
    rating INT NOT NULL,
    date DATE,
    upvote_count INT,
    downvote_count INT,
    PRIMARY KEY(buyer_id, seller_id)
);

CREATE TABLE Message(
    buyer_id INT NOT NULL REFERENCES Buyer(user_id),
    seller_id INT NOT NULL REFERENCES Seller(user_id),
    directionality INT,
    date DATE,
    messageText VARCHAR(1000),
    PRIMARY KEY(buyer_id, seller_id, date)
);

CREATE TABLE Cart (
    buyer_id INT NOT NULL REFERENCES Buyer(user_id),
    product_name VARCHAR(255) NOT NULL REFERENCES Product(name),
    seller_id INT NOT NULL REFERENCES Seller(user_id),
    quantity INT NOT NULL,
    PRIMARY KEY(buyer_id, product_name, seller_id)
);
