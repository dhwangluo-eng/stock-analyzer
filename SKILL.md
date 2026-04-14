# Stock Analyzer Pro v4.7

Professional stock analysis system with **intraday prediction engine**, tomorrow forecast, and anti-sell-off protection.

## What's New in v4.7

### 🚀 Intraday Prediction Engine
Three-dimensional prediction system:
- **Today's Session**: Morning / Noon / Afternoon forecasts
- **Pattern Recognition**: Dip-then-rally / Rally-then-drop / One-way trends
- **Rebound Strength**: Strong (3-6%) / Weak (1-3%) / Oscillation

### 📅 Tomorrow Forecast
- Next-day opening prediction
- Intraday trend forecast
- Support/Resistance levels (auto-calculated from MA)
- Reasoning for prediction

### 🛡️ Anti-Sell-Off Protection
- **Financial Bomb Detection**: Enhanced penalty for revenue decline, profit loss (-15 to -25 extra points)
- **Severe Bad News Cap**: When news is extremely bearish, prediction capped at "technical rebound" (no "bullish")
- **Oversold Rebound Identification**: Recognizes "bad news exhaustion + technical support + volume surge" patterns
- **Time-Based Advice**: "Don't sell in morning, wait for afternoon rebound"

## Description

Stock Analyzer Pro is a comprehensive stock analysis tool that combines:
- Multi-period technical analysis (MA5/10/20/30/60/120/250)
- Volume trend analysis with sustainability detection
- Fund flow detection (8 types of signals)
- News sentiment analysis with financial bomb detection
- **AI scoring system (0-100 points)**
- **1-2 day trend prediction**
- **Intraday session prediction** ⭐ NEW
- **Tomorrow forecast with support/resistance** ⭐ NEW
- **Smart time-based recommendations** ⭐ NEW

## Installation

```bash
git clone https://github.com/yourusername/stock-analyzer-pro.git
cd stock-analyzer-pro
pip install -r requirements.txt
```

## Usage

### Basic Analysis

```python
from stock_analyzer_pro import PerfectTradingSystemV4, add_stock_news

# Initialize system
system = PerfectTradingSystemV4()

# Add news for sentiment analysis
add_stock_news('600406', 'Company wins 1 billion contract')
add_stock_news('600406', 'Company announces buyback plan')

# Define holdings: (code, name, cost_price, quantity, stop_loss, target)
holdings = [
    ('600406', '国电南瑞', 25.124, 1500, 24.12, 27.13),
    ('600150', '中国船舶', 32.090, 200, 30.17, 34.02),
]

# Generate report
system.generate_report(holdings)
```

### Command Line

```bash
python stock_analyzer_pro.py
```

## Features

### 1. Multi-Period Moving Averages
- Short-term: MA5, MA10, MA20
- Medium-term: MA30, MA60
- Long-term: MA120, MA250 (yearly)

### 2. Volume Analysis ⭐ Enhanced
- Volume trend comparison (recent 5 days vs previous 5 days)
- **Volume sustainability detection** (consecutive amplification)
- Volume ratio detection
- Signals: 🔥 Massive Breakthrough / 🟢 Moderate Increase / ⚪ Flat / 📉 Decrease

### 3. Fund Flow Detection
Detects 8 types of fund movements:
- 🚀 Main Force Low Position Building
- 🟢 Main Force Low Position Accumulation
- 🟢 Main Force Pulling Up
- 🔴 Main Force High Position Distribution
- 🚨 Main Force High Position Selling
- 🚀 Capital Snatching
- 🚨 Panic Selling
- ⚪ Capital Waiting

### 4. News Sentiment Analysis ⭐ Enhanced
**Keyword detection:**
- Strong positive: 涨停, 翻倍, 中标, 回购, etc.
- Positive: 增长, 上涨, 盈利, etc.
- Strong negative: 跌停, 亏损, 减持, etc.
- Negative: 下降, 裁员, 停产, etc.

**Financial Bomb Detection (v4.7):**
- 营收下降: -15 points
- 净利润亏损: -20 points
- 业绩亏损: -20 points
- 由盈转亏: -25 points

### 5. AI Scoring System (0-100)
- Base score: 50
- Technical trend: +30 max
- Volume trend: +15 max
- Fund flow: +15 max
- News sentiment: variable
- Deep loss penalty: -15 (if >10% loss)
- **Financial bomb penalty: -10 to -25** ⭐ NEW

### 6. Trend Prediction ⭐ Enhanced

**1-2 Day Prediction:**
- 🟢 Bullish (score ≥70)
- 🟡 Oscillating Bullish (score 50-69)
- 🟠 Oscillating Bearish (score 30-49)
- 🔴 Bearish (score <30)
- **🟡 Technical Rebound** (oversold + bad news exhaustion) ⭐ NEW

**Intraday Prediction (v4.7):**
```
⏰ 【今日分时预测】
   早盘: 🟢 高开 / 🟡 低开 / ⚪ 平开
   盘中: 🟢 反弹 / 🔴 下跌 / ⚪ 震荡
   尾盘: 🟢 收高 / 🔴 收低 / ⚪ 持平
   形态: 📉→📈 先抑后扬 / 📈→📉 冲高回落 / etc.
   强度: 🔥 强反弹 / 🟢 弱反弹 / ⚪ 震荡
```

**Tomorrow Forecast (v4.7):**
```
📅 【明日预测】
   开盘: 🟢 高开 / 🔴 低开 / ⚪ 平开
   盘中: 🟢 继续走强 / 🔴 承压 / ⚪ 震荡
   趋势: 🟢 看涨 / 🔴 看跌 / 🟡 震荡
   压力: XX.XX  支撑: XX.XX
   理由: [derivation logic]
```

### 7. Time-Based Recommendations ⭐ NEW
Smart advice based on intraday patterns:
- `"Don't sell in morning, wait for afternoon rebound"` (dip-then-rally)
- `"Sell on rally, don't be greedy"` (rally-then-drop)
- `"Strong all day, hold position"` (one-way up)
- `"Weak all day, but don't panic sell if stop-loss not hit"` (one-way down)

## Output Example ⭐ v4.7 Format

```
【国电南瑞 (600406)】
   价格: 26.11元 (今日+0.00%)
   盈亏: +3.92%

   📊 综合评分: 125/100
   🔮 1-2日预测: 🟢 看涨

   ⏰ 【今日分时预测】
      早盘: 🟢 高开
      盘中: 🟡 窄幅波动
      尾盘: ⚪ 收盘附近
      形态: ⚪ 横盘震荡
      强度: ⚪ 震荡为主

   📅 【明日预测】
      开盘: 🟢 高开
      盘中: 🟢 继续走强
      趋势: 🟢 看涨
      压力: 26.18  支撑: 24.98
      理由: 趋势延续

   💡 操作建议: 🟢 持有
      理由: 强势，可持有或加仓
```

## Data Sources

- Real-time price: Sina Finance API
- K-line data: Tencent Finance API
- News: User input via `add_stock_news()`

## Configuration

Edit holdings in `stock_analyzer_pro.py`:

```python
holdings = [
    ('code', 'name', cost_price, quantity, stop_loss, target),
    # Add more stocks...
]
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Changelog

### v4.7.0 (2026-04-14)
- ✅ Added intraday prediction engine (morning/noon/afternoon)
- ✅ Added tomorrow forecast with support/resistance
- ✅ Added financial bomb detection (enhanced penalty)
- ✅ Added oversold rebound identification
- ✅ Added time-based smart recommendations
- ✅ Added volume sustainability analysis
- ✅ Added market sentiment index (based on Shanghai Composite)

### v4.6.0 (2026-04-12)
- Multi-period MA analysis
- Volume trend detection
- Fund flow signals
- News sentiment analysis
- 1-2 day trend prediction

## 💬 Community

Join our Telegram group for real-time discussion and updates:

📎 **https://t.me/weiduchaogu**

## License

MIT License

## Author

Created for OpenClaw Stock Analysis System
Version: 4.7
