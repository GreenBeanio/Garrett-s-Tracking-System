# Structure of the project

- Symbols
  - / is a directory
  - @ is a file
  - ! Means it's being worked on
  - & Ignored by git

- /Root: Everything.
  - /src: The main code.
    - &/env: The python venv.
    - &@config.json: Used to hold your configuration information.
    - @main.py: The main file to run the program.
    - @credentials.py: Loads the configuration for the program to use.
    - @requirements.txt: The python packages to load into pip.
    - /b_auth: The flask blueprint to hold all authentication aspect of the software.
      - @auth.py: The main python file for the flask blueprint.
      - @\_\_init\_\_.py: File for a python module.
      - /classes: The classes for authentication.
        - @\_\_init\_\_.py: File for a python module.
        - @auth_classes.py: File for classes used for authorization.
      - /functions: The functions for authentication.
        - @\_\_init\_\_.py: File for a python module.
        - @auth_functions.py: File for functions used for authorization.
      - /static: The static files for authentication.
      - /templates: The jinja templates for authentication.
    - /b_daily_log: The flask blueprint to hold the daily log tracking.
    - /classes: Holds the general classes for the software.
      - @\_\_init\_\_.py: File for a python module.
      - @credentials.py: Holds the credentials in python.
    - /functions: Holds the general functions for the software.
      - @\_\_init\_\_.py: File for a python module.
      - @load_credentials.py: Loads the credentials into python.
    - /static: The static assets.
      - /css: The css.
        - @base.css: The base css for the project.
      - /html: The html.
      - /images: The images.
      - /js: The javascript.
    - /templates: The jinja2 templates for flask.
      - @base.j2: The base jinja template that others build on top of.
      - @home.j2: The home page for the tracking system.
  - /PostgreSQL: Files for creating the PostgreSQL database.
    - @Create_Table_Accounts.sql:  Creates the general database and the tables.
    - @Procedures_Triggers.sql: Procedures and triggers that handle what to do when data is inserted.
    - @ Temp_Data: Inserts test data.
  - @.gitignore: The things git ignores.
  - @.gitattributes: Git stuff.
  - @api_structure.md: The api and the routes it uses.
  - @database_structure.md: The structure of the database.
  - @Development_Log.md: Log documenting the development of the application.
  - @documentation.md: The main documentation for the code of the software.
  - @information.md: Information on what tools and software is used in this software.
  - @project_structure.md: The file structure of this project.
  - @LICENSE: The license that this software is licenses under.
  - @README.md: The general readme of this project.
  - @template.py: A template python file with header and footer comments.
  - &@credentials.md: An untracked file that I'm keeping credentials in.
  - @linux_setup.md: Instructions for setting up linux.
