"""Technical indicator calculations for stock analysis."""

import numpy as np

from stockagent.models import TechnicalSignals


def calculate_sma(prices: list[float], period: int) -> float | None:
    """Calculate Simple Moving Average.

    Args:
        prices: List of prices (most recent last)
        period: Number of periods for the average

    Returns:
        SMA value, or None if insufficient data
    """
    if len(prices) < period:
        return None

    return float(np.mean(prices[-period:]))


def calculate_rsi(prices: list[float], period: int = 14) -> float | None:
    """Calculate Relative Strength Index.

    RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss

    Args:
        prices: List of prices (most recent last)
        period: RSI period (default 14)

    Returns:
        RSI value (0-100), or None if insufficient data
    """
    if len(prices) < period + 1:
        return None

    # Calculate price changes
    prices_arr = np.array(prices)
    deltas = np.diff(prices_arr)

    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    # Use only the last 'period' changes
    recent_gains = gains[-(period):]
    recent_losses = losses[-(period):]

    # Calculate averages
    avg_gain = np.mean(recent_gains)
    avg_loss = np.mean(recent_losses)

    # Avoid division by zero
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0

    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return float(rsi)


def calculate_ema(prices: list[float], period: int) -> float | None:
    """Calculate Exponential Moving Average.

    Args:
        prices: List of prices (most recent last)
        period: EMA period

    Returns:
        EMA value, or None if insufficient data
    """
    if len(prices) < period:
        return None

    prices_arr = np.array(prices)
    multiplier = 2 / (period + 1)

    # Start with SMA for first EMA value
    ema = np.mean(prices_arr[:period])

    # Calculate EMA for remaining prices
    for price in prices_arr[period:]:
        ema = (price - ema) * multiplier + ema

    return float(ema)


def calculate_macd(prices: list[float]) -> dict | None:
    """Calculate MACD (Moving Average Convergence Divergence).

    Uses standard parameters: 12-period EMA, 26-period EMA, 9-period signal.

    Args:
        prices: List of prices (most recent last)

    Returns:
        dict with macd_line, signal_line, histogram, or None if insufficient data
    """
    if len(prices) < 26:
        return None

    # Calculate EMAs for MACD line
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)

    if ema_12 is None or ema_26 is None:
        return None

    macd_line = ema_12 - ema_26

    # Calculate MACD values for signal line
    # We need enough history to calculate 9-period EMA of MACD
    macd_values = []
    for i in range(26, len(prices) + 1):
        subset = prices[:i]
        e12 = calculate_ema(subset, 12)
        e26 = calculate_ema(subset, 26)
        if e12 is not None and e26 is not None:
            macd_values.append(e12 - e26)

    if len(macd_values) < 9:
        # Not enough for signal line, but we can return MACD line
        return {
            "macd_line": macd_line,
            "signal_line": macd_line,  # Use MACD as signal when insufficient data
            "histogram": 0.0,
        }

    # Calculate signal line (9-period EMA of MACD)
    signal_line = calculate_ema(macd_values, 9)
    if signal_line is None:
        signal_line = macd_line

    histogram = macd_line - signal_line

    return {
        "macd_line": float(macd_line),
        "signal_line": float(signal_line),
        "histogram": float(histogram),
    }


def calculate_bollinger_bands(
    prices: list[float], period: int = 20, std_dev: int = 2
) -> dict | None:
    """Calculate Bollinger Bands.

    Args:
        prices: List of prices (most recent last)
        period: Period for SMA and standard deviation (default 20)
        std_dev: Number of standard deviations (default 2)

    Returns:
        dict with upper, middle, lower bands, or None if insufficient data
    """
    if len(prices) < period:
        return None

    recent_prices = prices[-period:]
    middle = float(np.mean(recent_prices))
    std = float(np.std(recent_prices, ddof=0))

    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)

    return {
        "upper": upper,
        "middle": middle,
        "lower": lower,
    }


def interpret_rsi(rsi: float | None) -> str:
    """Interpret RSI value.

    Args:
        rsi: RSI value (0-100)

    Returns:
        Interpretation: "overbought", "oversold", or "neutral"
    """
    if rsi is None:
        return "neutral"

    if rsi > 70:
        return "overbought"
    elif rsi < 30:
        return "oversold"
    else:
        return "neutral"


def interpret_macd(macd: dict | None) -> str:
    """Interpret MACD values.

    Args:
        macd: MACD dict with histogram

    Returns:
        Interpretation: "bullish", "bearish", or "neutral"
    """
    if macd is None:
        return "neutral"

    histogram = macd.get("histogram", 0)

    if histogram > 0:
        return "bullish"
    elif histogram < 0:
        return "bearish"
    else:
        return "neutral"


def calculate_all_indicators(bars: list[dict]) -> TechnicalSignals:
    """Calculate all technical indicators from OHLCV bars.

    Args:
        bars: List of OHLCV dicts with 'close' prices

    Returns:
        TechnicalSignals dict with all indicator values and interpretations
    """
    # Extract close prices
    prices = [bar["close"] for bar in bars if "close" in bar]

    if not prices:
        return {
            "rsi": None,
            "rsi_interpretation": "neutral",
            "macd": None,
            "macd_interpretation": "neutral",
            "bollinger": None,
            "sma_20": None,
            "sma_50": None,
            "sma_200": None,
            "current_price": 0.0,
        }

    # Get current price
    current_price = prices[-1] if prices else 0.0

    # Calculate indicators
    rsi = calculate_rsi(prices, 14)
    macd = calculate_macd(prices)
    bollinger = calculate_bollinger_bands(prices, 20, 2)
    sma_20 = calculate_sma(prices, 20)
    sma_50 = calculate_sma(prices, 50)
    sma_200 = calculate_sma(prices, 200)

    return {
        "rsi": rsi,
        "rsi_interpretation": interpret_rsi(rsi),
        "macd": macd,
        "macd_interpretation": interpret_macd(macd),
        "bollinger": bollinger,
        "sma_20": sma_20,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "current_price": current_price,
    }
