# Stock Analyzer Pro

Professional stock analysis system with multi-dimensional AI scoring, fund flow detection, and news sentiment analysis.

## Description

Stock Analyzer Pro is a comprehensive stock analysis tool that combines:
- Multi-period technical analysis (MA5/10/20/30/60/120/250)
- Volume trend analysis
- Fund flow detection (8 types of signals)
- News sentiment analysis
- AI scoring system (0-100 points)
- 1-2 day trend prediction
- Smart stop-loss/take-profit recommendations

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

### 2. Volume Analysis
- Volume trend comparison (recent 5 days vs previous 5 days)
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

### 4. News Sentiment Analysis
Automatic keyword detection for:
- Strong positive: 涨停, 翻倍, 中标, 回购, etc.
- Positive: 增长, 上涨, 盈利, etc.
- Strong negative: 跌停, 亏损, 减持, etc.
- Negative: 下降, 裁员, 停产, etc.

### 5. AI Scoring System (0-100)
- Base score: 50
- Technical trend: +30 max
- Volume trend: +15 max
- Fund flow: +15 max
- News sentiment: variable
- Deep loss penalty: -15 (if >10% loss)

### 6. Trend Prediction
- 🟢 Bullish (score ≥70)
- 🟡 Oscillating Bullish (score 50-69)
- 🟠 Oscillating Bearish (score 30-49)
- 🔴 Bearish (score <30)

## Output Example

```
【国电南瑞 (600406)】
   价格: 25.72元 (今日+0.00%)
   盈亏: 894元 (+2.37%)

   💹 交易数据:
      成交量: 48,352,399手 (4835.24万手)
      成交额: 48.35亿元
      趋势: ➡️ 持平 1.1x

   📊 多周期均线:
      短期: MA5=26.03❌ MA10=26.13❌ MA20=26.86❌
      中期: MA30=27.79❌ MA60=26.66❌
      长期: MA120=24.96✅
      年线: MA250=23.46✅

   📰 新闻分析:
      情绪: 🟢 强烈利好 (评分: +40)

   📊 综合评分: 120/100
   🔮 1-2日预测: 🟢 看涨

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

## License

MIT License

## Author

Created for OpenClaw Stock Analysis System
Version: 4.6
