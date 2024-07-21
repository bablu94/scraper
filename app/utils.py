import re

def clean_price(price_str):
    # Remove currency symbol and other non-numeric characters
    cleaned_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned_str)
    except ValueError:
        return 0.0
