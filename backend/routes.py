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
        # Parse and validate user-provided criteria
        data = request.json
        print("Request Data:", data)  # Log the incoming request data
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Extract filtering criteria
        criteria = StockCriteria(
            improving_revenue_years=data.get('improving_revenue_years', 5),
            institutional_ownership=data.get('institutional_ownership', 50.0),
            pe_rating=data.get('pe_rating', 5.0),
            high_market_cap=data.get('high_market_cap', True),
            net_income_growth_years=data.get('net_income_growth_years', 5),
            price_correction=data.get('price_correction', 20.0),
            buy_rating=data.get('buy_rating', True),
        )

        # Fetch S&P 500 stock data
        sp500_stocks = get_sp500_stocks()
        print(f"Fetched {len(sp500_stocks)} stocks.")  # Log the number of stocks fetched

        # Filter stocks based on criteria
        matching_stocks = filter_stocks(sp500_stocks, criteria)

        # Return filtered results
        if not matching_stocks:
            return jsonify({"message": "No stocks matched the criteria"}), 200
        return jsonify([stock.__dict__ for stock in matching_stocks]), 200

    except Exception as e:
        print("Error in /scan-stocks:", str(e))  # Log the error
        return jsonify({"error": str(e)}), 500


# Helper function to fetch S&P 500 stock data using yfinance
def get_sp500_stocks():
    tickers = ["AAPL", "MSFT", "GOOGL"]
    stocks = []

    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}")  # Log the ticker being processed
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            historical_data = stock.history(period="6mo")['Close'].tolist()

            fetched_stock = Stock(
                ticker=ticker,
                company_name=info.get("shortName", "Unknown"),
                market_cap=info.get("market_cap", 0),
                pe_ratio=info.get("trailing_pe", 0),
                net_income=info.get("net_income_to_common", 0),
                revenue=info.get("total_revenue", 0),
                institutional_ownership=info.get("held_percent_institutions", 0) * 100,
                current_price=info.get("current_price", 0),
                historical_prices=historical_data,
                buy_rating=True
            )
            stocks.append(fetched_stock)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return stocks


# Helper function to filter stocks based on user-provided criteria
def filter_stocks(stocks, criteria):
    matching_stocks = []
    for stock in stocks:
        try:
            print(f"Evaluating Stock: {stock.ticker}")  # Log stock details
            correction = calculate_price_correction(stock.historical_prices)  # Calculate correction
            print(f"Price Correction for {stock.ticker}: {correction}%")  # Log correction

            # Debug each criterion
            print(f"Checking Institutional Ownership: {stock.institutional_ownership} >= {criteria.institutional_ownership}")
            print(f"Checking P/E Ratio: {stock.pe_ratio} >= {criteria.pe_rating}")
            print(f"Checking Market Cap: {stock.market_cap > 1e10 if criteria.high_market_cap else True}")
            print(f"Checking Price Correction: {correction >= criteria.price_correction}")
            print(f"Checking Buy Rating: {stock.buy_rating == criteria.buy_rating}")

            if (
                stock.institutional_ownership >= criteria.institutional_ownership
                and stock.pe_ratio >= criteria.pe_rating
                and stock.net_income > 0
                and (stock.market_cap > 1e10 if criteria.high_market_cap else True)
                and correction >= criteria.price_correction
                and stock.buy_rating == criteria.buy_rating
            ):
                print(f"Stock {stock.ticker} matches criteria")  # Log matched stock
                matching_stocks.append(stock)
            else:
                print(f"Stock {stock.ticker} does NOT match criteria")
        except Exception as e:
            print(f"Error filtering stock {stock.ticker}: {e}")
    print(f"Matching Stocks: {len(matching_stocks)}")  # Log the number of matches
    return matching_stocks

# Helper function to calculate price correction
def calculate_price_correction(historical_prices):
    if len(historical_prices) < 2:
        return 0
    correction = ((max(historical_prices) - historical_prices[-1]) / max(historical_prices)) * 100
    return correction
