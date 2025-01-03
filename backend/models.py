from dataclasses import dataclass
from typing import List

@dataclass
class Stock:
    ticker: str
    company_name: str
    market_cap: float
    pe_ratio: float
    net_income: float
    revenue: float
    institutional_ownership: float
    current_price: float
    historical_prices: List[float]
    buy_rating: bool

@dataclass
class StockCriteria:
    improving_revenue_years: int
    institutional_ownership: float
    pe_rating: float
    high_market_cap: bool
    net_income_growth_years: int
    price_correction: float
    buy_rating: bool
