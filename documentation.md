# Software Documentation

---

## /auth/functions/auth_functions.py

The python script for authentication functions.

### createSalt

#### Type

Function

#### Description

A function that creates a random salt that is used when creating a user's hashed password.

#### Inputs

    - None

#### Outputs

    - String

#### Example

    - None

### createHashPass

#### Type

Function

#### Description

A function that creates a hashed password (hashpass) for the user.

#### Inputs

    - password: String
    - salt: String

#### Outputs

    - String

#### Example

    - None

### checkUser

#### Type

Function

#### Description

A function that checks if a user exists

#### Inputs

    - username: String
    - conn: PostgreSQL Connection

#### Outputs

    - Boolean

#### Example

    - None
