"""Recommendation scoring engine for stock analysis."""

from typing import Any

# Scoring weights (max contribution to composite score)
RSI_WEIGHT = 20
MACD_WEIGHT = 25
MA_WEIGHT = 20
BOLLINGER_WEIGHT = 15
SENTIMENT_WEIGHT = 20

# Recommendation thresholds
STRONG_BUY_THRESHOLD = 60
BUY_THRESHOLD = 20
SELL_THRESHOLD = -20
STRONG_SELL_THRESHOLD = -60


def score_rsi(rsi: float | None) -> float:
    """Score RSI indicator.

    RSI < 30 (oversold) → bullish (+20)
    RSI 30-40 → slightly bullish (+10)
    RSI 40-60 → neutral (0)
    RSI 60-70 → slightly bearish (-10)
    RSI > 70 (overbought) → bearish (-20)

    Args:
        rsi: RSI value (0-100) or None

    Returns:
        Score between -20 and +20
    """
    if rsi is None:
        return 0.0

    if rsi < 30:
        return RSI_WEIGHT  # +20 (oversold = bullish)
    elif rsi < 40:
        return RSI_WEIGHT / 2  # +10
    elif rsi <= 60:
        return 0.0  # neutral
    elif rsi <= 70:
        return -RSI_WEIGHT / 2  # -10
    else:
        return -RSI_WEIGHT  # -20 (overbought = bearish)


def score_macd(macd: dict[str, float] | None) -> float:
    """Score MACD indicator.

    Positive histogram + positive MACD line → strong bullish (+25)
    Positive histogram → bullish (+15)
    Negative histogram → bearish (-15)
    Negative histogram + negative MACD line → strong bearish (-25)

    Args:
        macd: MACD dict with histogram and macd_line keys, or None

    Returns:
        Score between -25 and +25
    """
    if macd is None:
        return 0.0

    histogram = macd.get("histogram", 0.0)
    macd_line = macd.get("macd_line", 0.0)

    if histogram > 0:
        if macd_line > 0:
            return MACD_WEIGHT  # +25 (strong bullish)
        return MACD_WEIGHT * 0.6  # +15 (bullish)
    elif histogram < 0:
        if macd_line < 0:
            return -MACD_WEIGHT  # -25 (strong bearish)
        return -MACD_WEIGHT * 0.6  # -15 (bearish)
    return 0.0


def score_moving_averages(signals: dict[str, Any]) -> float:
    """Score moving average alignment.

    Price > SMA-20 > SMA-50 > SMA-200 → strong uptrend (+20)
    Price > SMA-20, SMA-50 → uptrend (+10)
    Price < SMA-20 < SMA-50 < SMA-200 → strong downtrend (-20)
    Price < SMA-20, SMA-50 → downtrend (-10)
    Mixed → neutral (0)

    Args:
        signals: TechnicalSignals dict with current_price, sma_20, sma_50, sma_200

    Returns:
        Score between -20 and +20
    """
    price = signals.get("current_price", 0.0)
    sma_20 = signals.get("sma_20")
    sma_50 = signals.get("sma_50")
    sma_200 = signals.get("sma_200")

    # Need at least price and SMA-20 to score
    if not price or sma_20 is None:
        return 0.0

    # Check for strong uptrend (all aligned bullish)
    if sma_50 is not None and sma_200 is not None:
        if price > sma_20 > sma_50 > sma_200:
            return MA_WEIGHT  # +20 (strong uptrend)
        if price < sma_20 < sma_50 < sma_200:
            return -MA_WEIGHT  # -20 (strong downtrend)

    # Check for moderate trend
    if sma_50 is not None:
        if price > sma_20 and price > sma_50:
            return MA_WEIGHT / 2  # +10 (uptrend)
        if price < sma_20 and price < sma_50:
            return -MA_WEIGHT / 2  # -10 (downtrend)

    # Just SMA-20 comparison
    if price > sma_20:
        return MA_WEIGHT / 4  # +5 (slight bullish)
    elif price < sma_20:
        return -MA_WEIGHT / 4  # -5 (slight bearish)

    return 0.0


def score_bollinger(bollinger: dict[str, float] | None, current_price: float) -> float:
    """Score Bollinger Bands position.

    Price near lower band → potential bounce (+15)
    Price near upper band → potential pullback (-15)
    Price in middle → neutral (0)

    Args:
        bollinger: BollingerBands dict with upper, middle, lower keys, or None
        current_price: Current stock price

    Returns:
        Score between -15 and +15
    """
    if bollinger is None or current_price <= 0:
        return 0.0

    upper = bollinger.get("upper", 0.0)
    lower = bollinger.get("lower", 0.0)
    middle = bollinger.get("middle", 0.0)

    if upper <= lower or middle <= 0:
        return 0.0

    # Calculate position within bands (0 = lower, 1 = upper)
    band_width = upper - lower
    if band_width <= 0:
        return 0.0

    position = (current_price - lower) / band_width

    # Near lower band (below 20% of range) → bullish
    if position < 0.2:
        return BOLLINGER_WEIGHT  # +15
    # Near upper band (above 80% of range) → bearish
    elif position > 0.8:
        return -BOLLINGER_WEIGHT  # -15
    # Slightly below middle → slightly bullish
    elif position < 0.4:
        return BOLLINGER_WEIGHT / 2  # +7.5
    # Slightly above middle → slightly bearish
    elif position > 0.6:
        return -BOLLINGER_WEIGHT / 2  # -7.5

    return 0.0


def score_sentiment(sentiment: dict[str, Any] | None) -> float:
    """Score news sentiment.

    Maps sentiment score (-1 to +1) to (-20 to +20).

    Args:
        sentiment: SentimentResult dict with overall_score key, or None

    Returns:
        Score between -20 and +20
    """
    if sentiment is None:
        return 0.0

    overall_score = sentiment.get("overall_score", 0.0)

    # Linear scaling: -1 to +1 → -20 to +20
    return overall_score * SENTIMENT_WEIGHT


def calculate_composite_score(
    technical_signals: dict[str, Any], sentiment: dict[str, Any]
) -> float:
    """Calculate composite score from all signals.

    Args:
        technical_signals: TechnicalSignals dict
        sentiment: SentimentResult dict

    Returns:
        Composite score between -100 and +100
    """
    score = 0.0

    # RSI score
    score += score_rsi(technical_signals.get("rsi"))

    # MACD score
    score += score_macd(technical_signals.get("macd"))

    # Moving average score
    score += score_moving_averages(technical_signals)

    # Bollinger score
    score += score_bollinger(
        technical_signals.get("bollinger"),
        technical_signals.get("current_price", 0.0),
    )

    # Sentiment score
    score += score_sentiment(sentiment)

    # Clamp to range [-100, +100]
    return max(-100.0, min(100.0, score))


def generate_recommendation(score: float) -> tuple[str, float]:
    """Generate recommendation and confidence from composite score.

    Thresholds:
    - score > 60 → STRONG BUY
    - score > 20 → BUY
    - score -20 to 20 → HOLD
    - score < -20 → SELL
    - score < -60 → STRONG SELL

    Confidence = abs(score) as percentage.

    Args:
        score: Composite score (-100 to +100)

    Returns:
        Tuple of (recommendation, confidence)
    """
    # Determine recommendation
    if score > STRONG_BUY_THRESHOLD:
        recommendation = "STRONG BUY"
    elif score > BUY_THRESHOLD:
        recommendation = "BUY"
    elif score >= SELL_THRESHOLD:
        recommendation = "HOLD"
    elif score >= STRONG_SELL_THRESHOLD:
        recommendation = "SELL"
    else:
        recommendation = "STRONG SELL"

    # Calculate confidence (abs(score) as percentage, capped at 100)
    confidence = min(abs(score), 100.0)

    return recommendation, confidence


def get_explanation_factors(
    technical_signals: dict[str, Any], sentiment: dict[str, Any]
) -> list[str]:
    """Generate human-readable explanation factors.

    Args:
        technical_signals: TechnicalSignals dict
        sentiment: SentimentResult dict

    Returns:
        List of explanation strings sorted by absolute contribution
    """
    factors: list[tuple[float, str]] = []

    # RSI factor
    rsi = technical_signals.get("rsi")
    rsi_score = score_rsi(rsi)
    if rsi is not None and rsi_score != 0:
        if rsi_score > 0:
            factors.append((rsi_score, f"RSI at {rsi:.1f} indicates oversold (bullish)"))
        else:
            factors.append((rsi_score, f"RSI at {rsi:.1f} indicates overbought (bearish)"))

    # MACD factor
    macd = technical_signals.get("macd")
    macd_score = score_macd(macd)
    if macd is not None and macd_score != 0:
        histogram = macd.get("histogram", 0.0)
        if macd_score > 0:
            factors.append((macd_score, f"MACD histogram positive at {histogram:.2f} (bullish)"))
        else:
            factors.append((macd_score, f"MACD histogram negative at {histogram:.2f} (bearish)"))

    # Moving average factor
    ma_score = score_moving_averages(technical_signals)
    if ma_score != 0:
        price = technical_signals.get("current_price", 0.0)
        sma_20 = technical_signals.get("sma_20")
        if ma_score > 10:
            factors.append((ma_score, f"Price ${price:.2f} above all moving averages (strong uptrend)"))
        elif ma_score > 0:
            factors.append((ma_score, f"Price ${price:.2f} above SMA-20 ${sma_20:.2f} (uptrend)"))
        elif ma_score < -10:
            factors.append((ma_score, f"Price ${price:.2f} below all moving averages (strong downtrend)"))
        else:
            factors.append((ma_score, f"Price ${price:.2f} below SMA-20 ${sma_20:.2f} (downtrend)"))

    # Bollinger factor
    bollinger = technical_signals.get("bollinger")
    current_price = technical_signals.get("current_price", 0.0)
    bb_score = score_bollinger(bollinger, current_price)
    if bollinger is not None and bb_score != 0:
        if bb_score > 0:
            factors.append((bb_score, f"Price near lower Bollinger Band (potential bounce)"))
        else:
            factors.append((bb_score, f"Price near upper Bollinger Band (potential pullback)"))

    # Sentiment factor
    sentiment_score = score_sentiment(sentiment)
    if sentiment is not None and sentiment_score != 0:
        overall = sentiment.get("overall_score", 0.0)
        label = sentiment.get("overall_label", "neutral")
        headline_count = sentiment.get("headline_count", 0)
        if sentiment_score > 0:
            factors.append((sentiment_score, f"News sentiment {label} ({overall:.2f}) from {headline_count} headlines (bullish)"))
        else:
            factors.append((sentiment_score, f"News sentiment {label} ({overall:.2f}) from {headline_count} headlines (bearish)"))

    # Sort by absolute contribution (descending)
    factors.sort(key=lambda x: abs(x[0]), reverse=True)

    return [factor[1] for factor in factors]
