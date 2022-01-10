-- CREATE DATABASE myntwise
-- createdb myntwiseps
-- DROP DATABASE IF EXISTS myntwise

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(255), 
  password VARCHAR(255)
);

INSERT INTO users (email, password) VALUES ('test@test.com');
INSERT INTO users (email, password) VALUES ('test2@test.com');
INSERT INTO users (email, password) VALUES ('test3@test.com');
INSERT INTO users (email, password) VALUES ('test4@test.com');
INSERT INTO users (email, password) VALUES ('test5@test.com');
INSERT INTO users (email, password) VALUES ('test6@test.com');

CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(255), 
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO categories (category_name) VALUES ('Grocery');
INSERT INTO categories (category_name) VALUES ('Clothing');
INSERT INTO categories (category_name) VALUES ('Bill');
INSERT INTO categories (category_name) VALUES ('Miscellaneous');
INSERT INTO categories (category_name) VALUES ('Subscription');
INSERT INTO categories (category_name) VALUES ('Self-Care');

CREATE TABLE budgets (
  budget_id SERIAL PRIMARY KEY,
  budget_name VARCHAR(255),
  budget_amount INT,
  budget_description VARCHAR(500),
  budget_frequency ENUM('monthly', 'weekly', 'daily'),
  category_id INT,
  user_id INT, 
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO budgets (budget_name, budget_amount, budget_description, budget_frequency, user_id) VALUES ('Weekly Hair Cut', 50, 'Get hair cut from Fresh Cutz', 'weekly');
INSERT INTO budgets (budget_name, budget_amount, budget_description, budget_frequency, user_id) VALUES ('Phone', 120, 'Monthly phone bill with add ons', 'monthly');
INSERT INTO budgets (budget_name, budget_amount, budget_description, budget_frequency, user_id) VALUES ('Rent', 1900, 'Studio apartment rent', 'monthly');


CREATE TABLE user_transactions (
  user_transactions SERIAL PRIMARY KEY,
  user_transactions_name VARCHAR(255),
  user_transactions_amount INT,
  user_transactions_date Date,
  budget_id INT,
  category_id INT,
  user_id INT, 
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (budget_id) REFERENCES users(budget_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (2, 1, 10, FALSE);
INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (1, 1, 20, FALSE);
INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (3, 1, 100, FALSE);
INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (3, 1, 75, FALSE);
INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (2, 5, 4, FALSE);
INSERT INTO user_transactions (user_transactions_name, user_transactions_amount, user_transactions_date, user_id) VALUES (3, 5, 4, TRUE);

CREATE TABLE advice (
  advice_id SERIAL PRIMARY KEY,
  advice_name VARCHAR(155), 
  advice_price INT,
  advice_url VARCHAR(300),
  advice_description VARCHAR(500),
  advice_img VARCHAR(300),
  user_id INT, 
  budget_id INT,
  category_id INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (budget_id) REFERENCES users(budget_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO advice (advice_name, advice_price, advice_description, advice_img, user_id, budget_id, category_id) VALUES (1, 1, 10, TRUE);
INSERT INTO advice (advice_name, advice_price, advice_description, advice_img, user_id, budget_id, category_id) VALUES (2, 4, 2, TRUE);
INSERT INTO advice (advice_name, advice_price, advice_description, advice_img, user_id, budget_id, category_id) VALUES (1, 3, 10, TRUE);

