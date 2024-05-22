#!/bin/bash

# Update package list and upgrade all packages
echo "Updating package list and upgrading installed packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Apache
echo "Installing Apache web server..."
sudo apt-get install apache2 -y

# Install PHP
echo "Installing PHP..."
sudo apt-get install php -y

# Install git
echo "Installing Git..."
sudo apt-get install git -y

# Install Composer
echo "Installing Composer..."
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Install Python
echo "Installing Python..."
sudo apt-get install python3 -y

# Install pip for Python 3
echo "Installing pip for Python 3..."
sudo apt-get install python3-pip -y

# package needed for psycopg2
sudo apt-get install libpq-dev -y

#Install python3 packages
echo "Installing Python 3 packages (pip)..."
sudo pip3 install pyserial influxdb-client psycopg2 --break-system-packages

# Install PostgreSQL
echo "Installing PostgreSQL..."
sudo apt-get install postgresql postgresql-contrib php-pgsql -y

# Clone the specified Git repository to /var/www/html
echo "Cloning Git repository to /var/www/html..."
sudo git clone https://github.com/aircarto/ModuleAir_Pi /var/www/html/ModuleAir_Pi

# Restart Apache to apply changes
echo "Restarting Apache web server..."
sudo systemctl restart apache2

# Enable and start PostgreSQL service
echo "Enabling and starting PostgreSQL service..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Set up PostgreSQL user, database, and table
echo "Setting up PostgreSQL user, database, and table..."

# PostgreSQL commands
sudo -u postgres psql <<EOF
-- Create a new user with a password
CREATE USER airlab_test WITH PASSWORD '123plouf';

-- Create a new database
CREATE DATABASE cnrs;

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE cnrs TO airlab_test;

-- Connect to the new database
\c cnrs

-- Create a new table in the database
CREATE TABLE mytable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
EOF

# Confirm installations
echo "Confirming installations..."

apache_version=$(apache2 -v)
python_version=$(python3 --version)
php_version=$(php -v)
postgresql_version=$(psql --version)
pip_version=$(pip3 --version)
composer_version=$(composer --version)

echo "Apache version: $apache_version"
echo "Python version: $python_version"
echo "pip version: $pip_version"
echo "PHP version: $php_version"
echo "PostgreSQL version: $postgresql_version"
echo "Composer version: $composer_version"

echo "**** All installations are complete! ****"
