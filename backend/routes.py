from flask import Blueprint, jsonify, request
from models import Stock, StockCriteria
import yfinance as yf

# Create Flask Blueprint for routes
routes = Blueprint('routes', __name__)

# Sample endpoint to test connection
@routes.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})

# Root route
@routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Caroni Trading API!"})

# Endpoint to scan stocks
@routes.route('/scan-stocks', methods=['POST'])
def scan_stocks():
    try:
        # Parse user-provided criteria from the request body
        data = request.json
        criteria = StockCriteria(
            improving_revenue_years=data.get('improving_revenue_years', 5),
            institutional_ownership=data.get('institutional_ownership', 50.0),
            pe_rating=data.get('pe_rating', 5.0),
            high_market_cap=data.get('high_market_cap', True),
            net_income_growth_years=data.get('net_income_growth_years', 5),
            price_correction=data.get('price_correction', 20.0),
            buy_rating=data.get('buy_rating', True),
        )

        # Fetch S&P 500 stock data (mocked or via an API)
        sp500_stocks = get_sp500_stocks()

        # Apply filtering logic
        matching_stocks = []
        for stock in sp500_stocks:
            if (
                stock.institutional_ownership >= criteria.institutional_ownership
                and stock.pe_ratio >= criteria.pe_rating
                and stock.net_income >= 0
                and stock.market_cap > 1e10 if criteria.high_market_cap else True
                and calculate_price_correction(stock.historical_prices) >= criteria.price_correction
                and stock.buy_rating == criteria.buy_rating
            ):
                matching_stocks.append(stock)

        # Return filtered results
        return jsonify([stock.__dict__ for stock in matching_stocks])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to mock or fetch S&P 500 stocks
def get_sp500_stocks():
    return [
        Stock(
            ticker="AAPL",
            company_name="Apple Inc.",
            market_cap=2.5e12,
            pe_ratio=28.5,
            net_income=100e9,
            revenue=300e9,
            institutional_ownership=65.0,
            current_price=150,
            historical_prices=[180, 170, 160, 155, 150],
            buy_rating=True,
        ),
        Stock(
            ticker="MSFT",
            company_name="Microsoft Corp.",
            market_cap=2.2e12,
            pe_ratio=35.2,
            net_income=90e9,
            revenue=250e9,
            institutional_ownership=70.0,
            current_price=280,
            historical_prices=[310, 290, 285, 280, 270],
            buy_rating=True,
        ),
    ]

# Helper function to calculate price correction
def calculate_price_correction(historical_prices):
    if len(historical_prices) < 2:
        return 0
    return ((max(historical_prices) - historical_prices[-1]) / max(historical_prices)) * 100

