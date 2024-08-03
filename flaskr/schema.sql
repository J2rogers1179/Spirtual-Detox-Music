-- Drop tables if they already exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

-- Create the users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    occupation TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create the posts table as an example for future use
CREATE TABLE userData(




)