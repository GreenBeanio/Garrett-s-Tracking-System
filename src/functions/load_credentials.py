# Header Comment
# Project: [Garrett's Tracking System] [https://github.com/GreenBeanio/Garrett-s-Tracking-System]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Tracking System] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track a variety of purposes.]
# File Description: [Loads the credentials and configuration.]

# My Imports
from classes.credentials import Config  # The config class

# Imports
import json
import pathlib
import sys
import psycopg2
import redis
import ssl
import logging
import sys
from typing import Union, Any, Type, Callable, Tuple


# Function to check if a path exists
def checkPath(
    path: pathlib.Path, has_error: bool, variable: str, log: logging.Logger
) -> bool:
    # If the path exists return a result based off the existing has_error
    if pathlib.Path.exists(path):
        return has_error
    # If the path doesn't exist return an error
    else:
        log.warning(f'Invalid path for "{variable}"')
        return True


# Function to create Postgre Connection
def connectPostgre(
    connection_type: str,
    database: str,
    user: str,
    password: str,
    host: str,
    port: int,
    sslrootcert: Union[pathlib.Path, None],
    sslcert: Union[pathlib.Path, None],
    sslkey: Union[pathlib.Path, None],
) -> psycopg2:  # Not sure on the type
    # If there's no SSL
    if connection_type == "NO":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="require",
        )
    # If there's SSL verifying CA
    elif connection_type == "CA_CERTIFICATE":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="verify-ca",
            sslrootcert=sslrootcert,
        )
    # If there's SSL verifying full
    elif connection_type == "FULL_CERTIFICATE":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="verify-full",
            sslrootcert=sslrootcert,
            sslcert=sslcert,
            sslkey=sslkey,
        )
    # Return the resulting connection
    return postgre_client


# Function to create Redis Connection
def connectRedis(
    connection_type: str,
    db: int,
    username: str,
    password: str,
    host: str,
    port: int,
    ssl_ca_certs: Union[pathlib.Path, None],
    ssl_certfile: Union[pathlib.Path, None],
    ssl_keyfile: Union[pathlib.Path, None],
) -> redis.Redis:  # Not sure on the type
    # If there's no SSL
    if connection_type == "NO":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
            ssl=True,
            # ssl_cert_reqs=???
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
            ssl=True,
            # ssl_cert_reqs=???
            ssl_ca_certs=ssl_ca_certs,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )
    # Return the resulting connection
    return redis_client


# Function to create Celery Connection
def connectCelery(
    connection_type: str,
    db: int,
    username: str,
    password: str,
    host: str,
    port: int,
    ssl_ca_certs: Union[pathlib.Path, None],
    ssl_certfile: Union[pathlib.Path, None],
    ssl_keyfile: Union[pathlib.Path, None],
) -> dict:
    # If there's no SSL
    if connection_type == "NO":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="tracking_ecosystem",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="tracking_ecosystem",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
            broker_use_ssl={
                "keyfile": ssl_keyfile,
                "certfile": ssl_certfile,
                "ca_certs": ssl_ca_certs,
                "cert_reqs": ssl.CERT_NONE,  # Maybe set this to "ssl.CERT_OPTIONAL" instead
            },
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="tracking_ecosystem",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
            broker_use_ssl={
                "keyfile": ssl_keyfile,
                "certfile": ssl_certfile,
                "ca_certs": ssl_ca_certs,
                "cert_reqs": ssl.CERT_REQUIRED,
            },
        )
    # Return the resulting dictionary
    return celery_dict


# Function to validate data type
def validateData(
    test_data: Any,
    desired_type: Type,
    conversion_fun: Callable[[Any], Any],
    parameter: str,
    logger: logging.Logger,
) -> Tuple[bool, Any]:
    # Check if it's the correct type, and it's not a string (because we have multiple string conversion types)
    if isinstance(test_data, desired_type) and not isinstance(test_data, str):
        return (True, test_data)
    # Try to to convert the data
    try:
        return (True, conversion_fun(test_data))
    except:
        logger.warning(
            f'Value for "{parameter}" is the incorrect type. It must be a/an {str(desired_type)}.'
        )
        return (False, test_data)


# Function to try and convert to a string (uppercase specifically)
def convertStr(test_data: Any) -> str:
    return str(test_data).upper()


# Function to try and convert to a bool
def convertBool(test_data: Any) -> bool:
    # Check if the test_data is a string
    if isinstance(test_data, str):
        # Make it uppercase
        upper_data = test_data.upper()
        # Check it for matching
        if upper_data == "TRUE":
            return True
        elif upper_data == "FALSE":
            return False
    elif isinstance(test_data, int):
        if test_data == 1:
            return False
        elif test_data == 0:
            return True
    # If it wasn't one of the above raise an error
    raise Exception("Invalid Parameter")


# Function to load our credentials
def loadCredentials(running_path: pathlib.Path) -> Config:
    # Create a logger
    logger = logging.getLogger("Split_Tracker")
    logger.setLevel(logging.INFO)
    # Variable for storing if there's an error
    has_error = False
    # Create the path to the settings (where the main script is running then getting the directory)
    script_path = pathlib.Path(running_path).resolve().parent.resolve()
    json_path = pathlib.Path.joinpath(script_path, "config.json")
    # Load the file if it exists
    if pathlib.Path.exists(json_path):
        with open(json_path, "r") as file:
            # Load the json
            json_obj = json.load(file)

        # Attempting to validate the data types
        for key, value in json_obj.items():
            # Getting the type of conversion based off a list
            # Strings (and paths) that need to be uppercase
            if key in [
                "SSL_PATH_TYPE",
                "POSTGRE_SSL",
                "REDIS_SSL",
                "CELERY_REDIS_SSL",
            ]:
                result, new_data = validateData(value, str, convertStr, key, logger)
            # Strings (and paths) that need to be as they are
            elif key in [
                "SECRET_KEY",
                "FLASK_HOST",
                "FLASK_KEY_FILE",
                "FLASK_CERT_FILE",
                "POSTGRE_ADDRESS",
                "POSTGRE_USER",
                "POSTGRE_PASS",
                "POSTGRE_DATABASE",
                "POSTGRE_CA_FILE",
                "POSTGRE_KEY_FILE",
                "POSTGRE_CERT_FILE",
                "REDIS_ADDRESS",
                "REDIS_USER",
                "REDIS_PASS",
                "REDIS_CA_FILE",
                "REDIS_KEY_FILE",
                "REDIS_CERT_FILE",
                "CELERY_REDIS_ADDRESS",
                "CELERY_REDIS_USER",
                "CELERY_REDIS_PASS",
                "CELERY_REDIS_CA_FILE",
                "CELERY_REDIS_KEY_FILE",
                "CELERY_REDIS_CERT_FILE",
            ]:
                result, new_data = validateData(value, str, str, key, logger)
            # booleans
            elif key in ["TESTING", "DEBUG", "FLASK_SSL"]:
                # This could be problematic because any string that's not empty will be true and if empty it will be false
                result, new_data = validateData(value, bool, convertBool, key, logger)
            # integers
            elif key in [
                "FLASK_PORT",
                "POSTGRE_PORT",
                "REDIS_PORT",
                "REDIS_DATABASE",
                "CELERY_REDIS_PORT",
                "CELERY_REDIS_DATABASE",
            ]:
                result, new_data = validateData(value, int, int, key, logger)
            # If the result is true we replace the old data (even if it's the same data)
            if result:
                json_obj[key] = new_data
            # If it is not correct we acknowledge the error
            else:
                has_error = True
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        # Check for valid SSL types
        check_ssl_path = False
        if json_obj["FLASK_SSL"] in [True, False]:
            if json_obj["FLASK_SSL"] == True:
                check_ssl_path = True
        else:
            logger.warning(f'Invalid option for "FLASK_SSL"! It must be true or false')
            has_error = True
        if json_obj["POSTGRE_SSL"] in [
            "NO",
            "PLAIN",
            "CA_CERTIFICATE",
            "FULL_CERTIFICATE",
        ]:
            if json_obj["POSTGRE_SSL"] in ["CA_CERTIFICATE", "FULL_CERTIFICATE"]:
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "POSTGRE_SSL"! It must be "NO", "PLAIN", "CA_CERTIFICATE", or "FULL_CERTIFICATE"'
            )
            has_error = True
        if json_obj["REDIS_SSL"] in ["NO", "PLAIN", "CERTIFICATE"]:
            if json_obj["REDIS_SSL"] == "CERTIFICATE":
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "REDIS_SSL"! It must be "NO", "PLAIN", or "CERTIFICATE"'
            )
            has_error = True
        if json_obj["CELERY_REDIS_SSL"] in ["NO", "PLAIN", "CERTIFICATE"]:
            if json_obj["CELERY_REDIS_SSL"] == "CERTIFICATE":
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "CELERY_REDIS_SSL"! It must be "NO", "PLAIN", or "CERTIFICATE"'
            )
            has_error = True
        # Checking the SSL path type
        if check_ssl_path:
            if json_obj["SSL_PATH_TYPE"] not in ["RELATIVE", "ABSOLUTE"]:
                logger.warning(
                    f'Invalid option for "SSL_PATH_TYPE"! It must be "RELATIVE" or "ABSOLUTE"'
                )
                has_error = True
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        # If any of the connections are using ssl and a certificate we'll check the paths
        if check_ssl_path:
            # Check for Flask
            if json_obj["FLASK_SSL"] == True:
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    flask_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["FLASK_KEY_FILE"]
                    )
                    has_error = checkPath(flask_key_path, has_error, "FLASK_KEY_FILE")
                    flask_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["FLASK_CERT_FILE"]
                    )
                    has_error = checkPath(flask_cert_path, has_error, "FLASK_CERT_FILE")
                # If we're using absolute paths
                else:
                    flask_key_path = pathlib.Path(json_obj["FLASK_KEY_FILE"])
                    has_error = checkPath(flask_key_path, has_error, "FLASK_KEY_FILE")
                    flask_cert_path = pathlib.Path(json_obj["FLASK_CERT_FILE"])
                    has_error = checkPath(flask_cert_path, has_error, "FLASK_CERT_FILE")
            # If we're not using SSL Certificates
            else:
                flask_key_path = None
                flask_cert_path = None
            # Check for Postgre
            if json_obj["POSTGRE_SSL"] in ["CA_CERTIFICATE", "FULL_CERTIFICATE"]:
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    postgre_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["POSTGRE_CA_FILE"]
                    )
                    has_error = checkPath(postgre_ca_path, has_error, "POSTGRE_CA_FILE")
                    # If postgres is doing full verification
                    if json_obj["POSTGRE_SSL"] == "FULL_CERTIFICATE":
                        postgre_key_path = pathlib.Path.joinpath(
                            script_path, json_obj["POSTGRE_KEY_FILE"]
                        )
                        has_error = checkPath(
                            postgre_key_path, has_error, "POSTGRE_KEY_FILE"
                        )
                        postgre_cert_path = pathlib.Path.joinpath(
                            script_path, json_obj["POSTGRE_CERT_FILE"]
                        )
                        has_error = checkPath(
                            postgre_cert_path, has_error, "POSTGRE_CERT_FILE"
                        )
                    # If we're only doing the CA_Certificate
                    else:
                        postgre_key_path = None
                        postgre_cert_path = None
                # If we're using absolute paths
                else:
                    postgre_ca_path = pathlib.Path(json_obj["POSTGRE_CA_FILE"])
                    has_error = checkPath(postgre_ca_path, has_error, "POSTGRE_CA_FILE")
                    # If postgres is doing full verification
                    if json_obj["POSTGRE_SSL"] == "FULL_CERTIFICATE":
                        postgre_key_path = pathlib.Path(json_obj["POSTGRE_KEY_FILE"])
                        has_error = checkPath(
                            postgre_key_path, has_error, "POSTGRE_KEY_FILE"
                        )
                        postgre_cert_path = pathlib.Path(json_obj["POSTGRE_CERT_FILE"])
                        has_error = checkPath(
                            postgre_cert_path, has_error, "POSTGRE_CERT_FILE"
                        )
                    # If we're only doing the CA_Certificate
                    else:
                        postgre_key_path = None
                        postgre_cert_path = None
            # If we're not using SSL Certificates
            else:
                postgre_ca_path = None
                postgre_key_path = None
                postgre_cert_path = None
            # Check for Redis
            if json_obj["REDIS_SSL"] == "CERTIFICATE":
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    redis_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_CA_FILE"]
                    )
                    has_error = checkPath(redis_ca_path, has_error, "REDIS_CA_FILE")
                    redis_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(redis_key_path, has_error, "REDIS_KEY_FILE")
                    redis_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(redis_cert_path, has_error, "REDIS_CERT_FILE")
                # If we're using absolute paths
                else:
                    redis_ca_path = pathlib.Path(json_obj["REDIS_CA_FILE"])
                    has_error = checkPath(redis_ca_path, has_error, "REDIS_CA_FILE")
                    redis_key_path = pathlib.Path(json_obj["REDIS_KEY_FILE"])
                    has_error = checkPath(redis_key_path, has_error, "REDIS_KEY_FILE")
                    redis_cert_path = pathlib.Path(json_obj["REDIS_CERT_FILE"])
                    has_error = checkPath(redis_cert_path, has_error, "REDIS_CERT_FILE")
            # If we're not using SSL Certificates
            else:
                redis_ca_path = None
                redis_key_path = None
                redis_cert_path = None
            # Check for Celery
            if json_obj["CELERY_REDIS_ADDRESS"] == "CERTIFICATE":
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    celery_redis_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_CA_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_ca_path, has_error, "CELERY_REDIS_CA_FILE"
                    )
                    celery_redis_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_key_path, has_error, "CELERY_REDIS_KEY_FILE"
                    )
                    celery_redis_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_cert_path, has_error, "CELERY_REDIS_CERT_FILE"
                    )
                # If we're using absolute paths
                else:
                    celery_redis_ca_path = pathlib.Path(
                        json_obj["CELERY_REDIS_CA_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_ca_path, has_error, "CELERY_REDIS_CA_FILE"
                    )
                    celery_redis_key_path = pathlib.Path(
                        json_obj["CELERY_REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_key_path, has_error, "CELERY_REDIS_KEY_FILE"
                    )
                    celery_redis_cert_path = pathlib.Path(
                        json_obj["CELERY_REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_cert_path, has_error, "CELERY_REDIS_CERT_FILE"
                    )
            # If we're not using SSL Certificates
            else:
                celery_redis_ca_path = None
                celery_redis_key_path = None
                celery_redis_cert_path = None
        # If there is no SSL Certificates at all
        else:
            flask_key_path = None
            flask_cert_path = None
            postgre_ca_path = None
            postgre_key_path = None
            postgre_cert_path = None
            redis_ca_path = None
            redis_key_path = None
            redis_cert_path = None
            celery_redis_ca_path = None
            celery_redis_key_path = None
            celery_redis_cert_path = None
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        # Attempting to create the database connections
        try:
            postgre_connection = connectPostgre(
                connection_type=json_obj["POSTGRE_SSL"],
                database=json_obj["POSTGRE_DATABASE"],
                user=json_obj["POSTGRE_USER"],
                password=json_obj["POSTGRE_PASS"],
                host=json_obj["POSTGRE_ADDRESS"],
                port=json_obj["POSTGRE_PORT"],
                sslrootcert=postgre_ca_path,
                sslcert=postgre_cert_path,
                sslkey=postgre_key_path,
            )
        except:
            logger.warning(
                "Invalid options for the PostgreSQL connection! Can't form a connection!"
            )
            has_error = True
        try:
            redis_connection = connectRedis(
                connection_type=json_obj["REDIS_SSL"],
                db=json_obj["REDIS_DATABASE"],
                username=json_obj["REDIS_USER"],
                password=json_obj["REDIS_PASS"],
                host=json_obj["REDIS_ADDRESS"],
                port=json_obj["REDIS_PORT"],
                ssl_ca_certs=redis_ca_path,
                ssl_certfile=redis_cert_path,
                ssl_keyfile=redis_key_path,
            )
        except:
            logger.warning(
                "Invalid options for the Redis connection! Can't form a connection!"
            )
            has_error = True
        try:
            # Need to test this as a connection too
            celery_dict = connectCelery(
                connection_type=json_obj["CELERY_REDIS_SSL"],
                db=json_obj["CELERY_REDIS_DATABASE"],
                username=json_obj["CELERY_REDIS_USER"],
                password=json_obj["CELERY_REDIS_PASS"],
                host=json_obj["CELERY_REDIS_ADDRESS"],
                port=json_obj["CELERY_REDIS_PORT"],
                ssl_ca_certs=celery_redis_ca_path,
                ssl_certfile=celery_redis_cert_path,
                ssl_keyfile=celery_redis_key_path,
            )
            # Try to connect to the redis backend. If it works celery should work.
            celery_connection = connectRedis(
                connection_type=json_obj["REDIS_SSL"],
                db=json_obj["REDIS_DATABASE"],
                username=json_obj["REDIS_USER"],
                password=json_obj["REDIS_PASS"],
                host=json_obj["REDIS_ADDRESS"],
                port=json_obj["REDIS_PORT"],
                ssl_ca_certs=redis_ca_path,
                ssl_certfile=redis_cert_path,
                ssl_keyfile=redis_key_path,
            )
            # Closing this for now. We could keep it if we wanted, but I don't have a purpose for it right now.
            celery_connection.close()
        except:
            logger.warning(
                "Invalid options for the Celery Redis connection! Can't form a connection!"
            )
            has_error = True

        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()

        # Convert the json into a class
        # I'm choosing to store all the data in this class, instead of just the formed connections, in the event that
        # I need to remake the connection.
        config_class = Config(
            # General
            logger=logger,  #
            ssl_path_type=json_obj["SSL_PATH_TYPE"],  #
            # Flask
            secret_key=json_obj["SECRET_KEY"],
            testing=json_obj["TESTING"],
            debug=json_obj["DEBUG"],
            flask_host=json_obj["FLASK_HOST"],
            flask_port=json_obj["FLASK_PORT"],
            flask_ssl=json_obj["FLASK_SSL"],  #
            flask_key_file=json_obj["FLASK_KEY_FILE"],
            flask_cert_file=json_obj["FLASK_CERT_FILE"],
            # PostgreSQL
            postgre_addr=json_obj["POSTGRE_ADDRESS"],
            postgre_port=json_obj["POSTGRE_PORT"],
            postgre_user=json_obj["POSTGRE_USER"],
            postgre_passwd=json_obj["POSTGRE_PASS"],
            postgre_database=json_obj["POSTGRE_DATABASE"],
            postgre_ssl=json_obj["POSTGRE_SSL"],  #
            postgre_ca_file=postgre_ca_path,
            postgre_key_file=postgre_key_path,
            postgre_cert_file=postgre_cert_path,
            postgre_con=postgre_connection,
            # Redis
            redis_addr=json_obj["REDIS_ADDRESS"],
            redis_port=json_obj["REDIS_PORT"],
            redis_user=json_obj["REDIS_USER"],
            redis_passwd=json_obj["REDIS_PASS"],
            redis_database=json_obj["REDIS_DATABASE"],
            redis_ssl=json_obj["REDIS_SSL"],  #
            redis_ca_file=redis_ca_path,
            redis_key_file=redis_key_path,
            redis_cert_file=redis_cert_path,
            redis_con=redis_connection,
            # Celery
            celery_redis_addr=json_obj["CELERY_REDIS_ADDRESS"],
            celery_redis_port=json_obj["CELERY_REDIS_PORT"],
            celery_redis_user=json_obj["CELERY_REDIS_USER"],
            celery_redis_passwd=json_obj["CELERY_REDIS_PASS"],
            celery_redis_database=json_obj["CELERY_REDIS_DATABASE"],
            celery_redis_ssl=json_obj["CELERY_REDIS_SSL"],  #
            celery_redis_ca_file=celery_redis_ca_path,
            celery_redis_key_file=celery_redis_key_path,
            celery_redis_cert_file=celery_redis_cert_path,
            celery_dict=celery_dict,
            celery_con=1,  ### Need to change this,
        )
        return config_class
    # Create a file if it doesn't exist
    else:
        default_json = {
            # General
            "SSL_PATH_TYPE": "RELATIVE_ABSOLUTE",
            # Flask
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "TESTING": "TRUE_OR_FALSE",
            "DEBUG": "TRUE_OR_FALSE",
            "FLASK_HOST": "YOUR_FLASK_HOST (local machine only 127.0.0.1 or 0.0.0.0 for other machines)",
            "FLASK_PORT": "YOUR_FLASK_PORT (Default 5000)",
            "FLASK_SSL": "TRUE_OR_FALSE",  # Note that this should only be used in testing. When deploying you'll use gunicorn and nginx, or a similar stack, to serve the application.
            "FLASK_KEY_FILE": "PATH_TO_SSL_KEY",
            "FLASK_CERT_FILE": "PATH_TO_SSL_CERT",
            # PostgreSQL
            "POSTGRE_ADDRESS": "ADDRESS_TO_POSTGRE (local machine 127.0.0.1 or another host)",
            "POSTGRE_PORT": "POSTGRE_PORT (Default 5432)",
            "POSTGRE_USER": "YOUR_POSTGRE_USER",
            "POSTGRE_PASS": "YOUR_POSTGRE_PASSWORD",
            "POSTGRE_DATABASE": "POSTGRE_DATABASE_NAME",
            "POSTGRE_SSL": "NO, PLAIN, CA_CERTIFICATE, FULL_CERTIFICATE",
            "POSTGRE_CA_FILE": "PATH_TO_SSL_CA",
            "POSTGRE_KEY_FILE": "PATH_TO_SSL_KEY",
            "POSTGRE_CERT_FILE": "PATH_TO_SSL_CERT",
            # Redis
            "REDIS_ADDRESS": "ADDRESS_TO_REDIS (local machine 127.0.0.1 or another host)",
            "REDIS_PORT": "REDIS_PORT (Default 6379)",
            "REDIS_USER": "YOUR_REDIS_USER",
            "REDIS_PASS": "YOUR_REDIS_PASSWORD",
            "REDIS_DATABASE": "REDIS_DATABASE_NUMBER",
            "REDIS_SSL": "NO, PLAIN, CERTIFICATE",
            "REDIS_CA_FILE": "PATH_TO_SSL_CA",
            "REDIS_KEY_FILE": "PATH_TO_SSL_KEY",
            "REDIS_CERT_FILE": "PATH_TO_SSL_CERT",
            # Celery Redis
            "CELERY_REDIS_ADDRESS": "ADDRESS_TO_CELERY_REDIS (local machine 127.0.0.1 or another host)",
            "CELERY_REDIS_PORT": "CELERY_REDIS_PORT (Default 6379)",
            "CELERY_REDIS_USER": "YOUR_CELERY_REDIS_USER",
            "CELERY_REDIS_PASS": "YOUR_CELERY_REDIS_PASSWORD",
            "CELERY_REDIS_DATABASE": "CELERY_REDIS_DATABASE_NUMBER",
            "CELERY_REDIS_SSL": "NO, PLAIN, CERTIFICATE",
            "CELERY_REDIS_CA_FILE": "PATH_TO_SSL_CA",
            "CELERY_REDIS_KEY_FILE": "PATH_TO_SSL_KEY",
            "CELERY_REDIS_CERT_FILE": "PATH_TO_SSL_CERT",
        }
        with open(json_path, "w+") as file:
            json_obj = json.dumps(default_json, indent=4, sort_keys=False, default=str)
            file.write(json_obj)
        # Maybe not the bes idea, but it is what it is
        sys.exit("Fill in the config file")


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
