# Stock Analyzer Pro v4.6

Professional stock analysis system with multi-dimensional AI scoring.

## Features

- ✅ Multi-period moving averages (MA5/10/20/30/60/120/250)
- ✅ Volume trend analysis with ratio detection
- ✅ 8-type fund flow detection (accumulation/distribution/pulling/selling)
- ✅ News sentiment analysis with keyword detection
- ✅ AI scoring system (0-100 points)
- ✅ 1-2 day trend prediction
- ✅ Smart stop-loss/take-profit recommendations

## Quick Start

```python
from stock_analyzer_pro import PerfectTradingSystemV4, add_stock_news

system = PerfectTradingSystemV4()

# Add news for analysis
add_stock_news('600406', 'Company wins major contract')

# Define holdings
holdings = [
    ('600406', 'Stock Name', 25.0, 1000, 24.0, 28.0),
]

# Generate report
system.generate_report(holdings)
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

## Version History

- v4.6: Enhanced fund flow detection, volume trend analysis
- v4.5: Added MA120/250, news sentiment analysis
- v4.4: Base version with multi-period MA and AI scoring

## License

MIT
