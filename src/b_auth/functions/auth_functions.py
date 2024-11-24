# Header Comment
# Project: [Garrett's Tracking System] [https://github.com/GreenBeanio/Garrett-s-Tracking-System]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Tracking System] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track a variety of purposes.]
# File Description: [The functions used for authentication.]

# My Imports
# from classes.credentials import Config  # The config class

# Imports
import secrets
import string
import hashlib
import psycopg2
from typing import Tuple, Dict
import datetime
import logging


# Function to create a salt
def createSalt() -> str:
    # Generate a random salt for a new user
    salt = "".join(
        [
            secrets.choice(string.ascii_letters + string.digits + string.punctuation)
            for x in range(secrets.choice(range(5, 20)))
        ]
    )
    return salt


# Function to create a hashed password (hashpass)
def createHashPass(password: str, salt: str) -> str:
    hash_pass = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hash_pass


# Function to check if a user exists
def checkUser(username: str, conn: psycopg2.extensions.connection) -> bool:
    # Query the database
    cursor = conn.cursor()
    sql = "SELECT 1 FROM accounts where username=%s LIMIT 1;"
    cursor.execute(sql, (username,))
    # Save the results
    results = cursor.fetchone()
    # Commit and close the cursor
    conn.commit()
    cursor.close()
    # Check the results (False if user doesn't exist, True if it does)
    if results is None:
        return False
    else:
        return True


# Function to create a user
def createUser(
    username: str,
    password: str,
    recovery: Tuple[Dict, None],
    email: Tuple[Dict, None],
    conn: psycopg2.extensions.connection,
    log: logging.Logger,
):
    # Generating a salt
    salt = createSalt()
    # Creating a hashpass
    hash_pass = createHashPass(password=password, salt=salt)
    # Creating the values
    # print("========================")
    # print(
    #     datetime.datetime.now(datetime.timezone.utc).astimezone()
    # )  # Datetime with correct local time and local time zone
    # print(
    #     datetime.datetime.now(datetime.timezone.utc)
    # )  # Date time with utc time and timezone
    # print(
    #     datetime.datetime.now().astimezone()
    # )  # Date time with local time and local time zone
    # print(datetime.datetime.now())  # Date time with current time and no time zone
    # print("-----------------")
    cur_time = datetime.datetime.now().astimezone()
    # print(cur_time.tzinfo)
    # print(cur_time)
    # print(
    #     cur_time.astimezone(datetime.timezone.utc)
    # )  # Changes the time to match the new time zone
    # print(
    #     cur_time.replace(tzinfo=datetime.timezone.utc)
    # )  # Doesn't change the times, just changes the time zone
    values = (username, hash_pass, salt, recovery, email, cur_time, cur_time, 1)
    # Creating the new user
    cur = conn.cursor()
    sql = """INSERT INTO accounts (username, password, salt, recovery, email, creation, last_session, total_sessions)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
    # Try to execute
    try:
        cur.execute(sql, values)
        conn.commit()
        cur.close()
    except psycopg2.Error as err:
        log.error(f'SQL Error: "{err.pgerror}"')
        conn.rollback()
        cur.close()
    except:
        log.error("Other Error")
        conn.rollback()
        cur.close()

    # I will want to create a session too


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
