# Stock Analyzer Pro v4.7

Professional stock analysis system with **intraday prediction engine**, tomorrow forecast, and anti-sell-off protection.

## What's New in v4.7

🚀 **Intraday Prediction Engine** - Predict morning/noon/afternoon sessions
📅 **Tomorrow Forecast** - Next-day opening, trend, support/resistance
🛡️ **Anti-Sell-Off Protection** - Financial bomb detection + oversold rebound identification
⏰ **Time-Based Advice** - "Don't sell in morning, wait for afternoon rebound"

## Features

- ✅ **Multi-period moving averages** (MA5/10/20/30/60/120/250)
- ✅ **Volume trend analysis** with sustainability detection
- ✅ **8-type fund flow detection** (accumulation/distribution/pulling/selling)
- ✅ **News sentiment analysis** with financial bomb detection
- ✅ **AI scoring system** (0-100 points)
- ✅ **1-2 day trend prediction**
- ✅ **Intraday session prediction** ⭐ NEW in v4.7
- ✅ **Tomorrow forecast** with support/resistance ⭐ NEW in v4.7
- ✅ **Smart time-based recommendations** ⭐ NEW in v4.7

## Quick Start

```python
from stock_analyzer_pro import PerfectTradingSystemV4, add_stock_news

system = PerfectTradingSystemV4()

# Add news for analysis
add_stock_news('600406', 'Company wins major contract')

# Define holdings: (code, name, cost, qty, stop_loss, target)
holdings = [
    ('600406', 'Stock Name', 25.0, 1000, 24.0, 28.0),
]

# Generate report
system.generate_report(holdings)
```

## v4.7 Intraday Prediction Example

```
⏰ 【今日分时预测】
   早盘: 🟢 高开
   盘中: 🟡 窄幅波动
   尾盘: ⚪ 收盘附近
   形态: ⚪ 横盘震荡
   强度: 🔥 强反弹(3-6%)

📅 【明日预测】
   开盘: 🟢 高开
   盘中: 🟢 继续走强
   趋势: 🟢 看涨
   压力: 26.18  支撑: 24.98
   理由: 趋势延续

💡 操作建议: 🟢 持有
   ⏰ 时间策略: 全天强势，持有为主
```

## Fund Flow Signals

| Signal | Description |
|--------|-------------|
| 🚀 Main Force Low Building | Accumulating at low price |
| 🟢 Main Force Accumulation | Secretly buying at low |
| 🟢 Main Force Pulling Up | Driving price up |
| 🔴 Main Force Distribution | Selling at high |
| 🚨 Main Force Selling | Dumping at high |
| 🚀 Capital Snatching | Aggressive buying |
| 🚨 Panic Selling | Massive sell-off |
| ⚪ Capital Waiting | No significant movement |

## Anti-Sell-Off Protection (v4.7)

**Financial Bomb Detection:**
- Revenue decline: -15 points
- Net profit loss: -20 points
- Profit turning to loss: -25 points

**Severe Bad News Cap:**
When news is extremely bearish, prediction capped at "Technical Rebound" (no "Bullish")

**Oversold Rebound Identification:**
- Bad news exhaustion + Technical support + Volume surge + Loss position
- Warning: "Don't sell on panic, wait for rebound"

## Pattern Recognition (v4.7)

| Pattern | Description | Strategy |
|---------|-------------|----------|
| 📉→📈 Dip-then-rally | Bad news exhausted, bargain hunting | Don't sell morning |
| 📈→📉 Rally-then-drop | Profit-taking, distribution | Sell on rally |
| 📈→📈 One-way up | Strong trend | Hold position |
| 📉→📉 One-way down | Trend deterioration | Cut loss if stop hit |

## Version History

- **v4.7**: Intraday prediction, tomorrow forecast, financial bomb detection, time-based advice
- v4.6: Enhanced fund flow detection, volume trend analysis
- v4.5: Added MA120/250, news sentiment analysis
- v4.4: Base version with multi-period MA and AI scoring

## License

MIT
