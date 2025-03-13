# stock_tracker
# Stock Portfolio Tracker

![Website Status](https://img.shields.io/website?url=http%3A%2F%2F152.70.190.66/) at http://152.70.190.66/

This is a simple stock portfolio tracker website built using Django, Nginx, and Gunicorn. It allows users to manage their stock portfolios and provides real-time data for US stocks.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Setting Up SSL](#setting-up-ssl)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication.
- Portfolio management to track stocks.
- Real-time stock data integration.
- Secure HTTPS connection via Let's Encrypt.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/g-fudulov/stock_tracker.git

2. **Build the Docker container:**

    ```bash
    docker compose -f docker-compose.yml up --build

3. **Access the website**

    Open a web browser and navigate to http://localhost

### Usage

- Test the application.
- Register for an account and log in.
- Manage your stock portfolio.
- Buy and Sell stocks.


### Setting Up SSL

1. **Build the Docker container:**

    ```bash
    docker compose -f docker-compose.production.yml build

2. **Run only web container:**

    ```bash
    docker compose -f docker-compose.production.yml up web -d

3. **Collect the static files:**

    ```bash
    docker compose -f docker-compose.production.yml exec web python manage.py collectstatic
   
4. **Migrate the database:**

    ```bash
    docker compose -f docker-compose.production.yml exec web python manage.py migrate

5. **Run nginx container:**
   - If setting up for the first time => remove the redirect in nginx/conf.d/default.conf

       ```bash
       docker compose -f docker-compose.production.yml up nginx -d
  
6. **Obtain the SSL certificate by letsencrypt:**

    ```bash
    docker compose -f docker-compose.production.yml up certbot -d

### Contributing

I welcome contributions from the community. Please feel free to open issues and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
