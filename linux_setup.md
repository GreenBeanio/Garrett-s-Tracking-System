# Note

The bulk of this is assuming you have already set up following the instructions in the [Split Tracker project](https://github.com/GreenBeanio/Garrett-s-Split-Tracker).

## Creating a user to access this project (for backups and stuff)

- Create the user
  - sudo useradd -m -d /home/u_tracking_system -s /bin/bash tracking_system
- Add a password to the user
  - sudo passwd tracking_system
- Create the ssh directory
  - sudo mkdir /home/u_tracking_system/.ssh
- Copy the ssh key in
  - sudo touch /home/u_tracking_system/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/u_tracking_system/.ssh/authorized_keys
      - Vim /home/u_tracking_system/.ssh/authorized_keys
- Set the directory permissions
  - sudo chown -R tracking_system:tracking_system /home/u_tracking_system/.ssh
  - sudo chmod 700 /home/u_tracking_system/.ssh
  - sudo chmod 600 /home/u_tracking_system/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases tracking_system

## Creating a directory for the project

- Switch to the tracking_system user
  - sudo su tracking_system

- Switch the directory
  - cd /projects/
- Make the directory to store the files
  - mkdir tracking_system

- Changing the ownership and permissions
  - Change the ownership
    - chown -R tracking_system:databases tracking_system
  - Change the permissions
    - chmod -R u=rwx,g=rwx,o=rx tracking_system

- Exit the user
  - exit

## Creating a postgres database and user

- Local Admin
  - sudo -u postgres psql
- Create the user for the application
  - CREATE USER tracking_system WITH password 'your_password';
- Create the database for the application
  - CREATE DATABASE tracking_system;
- Grant the user permissions to the database
  - GRANT ALL PRIVILEGES ON DATABASE "tracking_system" to tracking_system;

## Creating a redis user

- Enter the local shell
  - sudo redis-cli -h 127.0.0.1 --tls
    - You may need to login with this command if you've already set up ACL
      - auth username password
- Create the user
  - acl setuser tracking_system on >your_password
- Adding permissions
  - acl setuser tracking_system allcommands ~tracking_system:*
- Saving the ACL users
  - ACL SAVE
