from static import api_config
import requests


def check_stock_exists(symbol):
    querystring = {"country": "United States", "symbol": f"{symbol}", "format": "json"}

    try:
        # Make a GET request to the API
        response = requests.get(api_config.url, headers=api_config.headers, params=querystring)

        if response.status_code == 200:
            # Parse the JSON response
            parsed_response = response.json()

            # Check if the response contains valid stock data
            if not parsed_response['data']:
                return False  # Does not exist
            else:
                return parsed_response  # Exists

        else:
            # Handle API request error (e.g., API key is invalid)
            return False

    except requests.exceptions.RequestException:
        # Handle network-related errors
        return False


def calculate_avg_price_per_share_buy(existing_quantity, bought_quantity, existing_avg_price, bought_price):
    total_quantity = existing_quantity + bought_quantity
    total_cost = ((existing_quantity * existing_avg_price) + (bought_quantity * bought_price))
    average_purchase_price = total_cost / total_quantity

    return average_purchase_price, total_quantity


def calculate_realised_pnl(existing_pnl, existing_avg_price, selling_price, selling_quantity):
    realised_pnl = (selling_price - existing_avg_price) * selling_quantity
    new_pnl = existing_pnl + realised_pnl

    return new_pnl


def update_quantity(existing_quantity, selling_quantity):
    remaining_quantity = existing_quantity - selling_quantity
    new_quantity = remaining_quantity

    return new_quantity
