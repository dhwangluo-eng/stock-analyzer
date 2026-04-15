# Stock Analyzer Pro v4.8

Professional stock analysis system with **enhanced stop-loss protection**, **rebound space calculation**, and **smart alerts**.

## What's New in v4.8

🛡️ **Enhanced Stop-Loss Protection**
- Deep loss penalty increased (-20 for >10%, -25 for >15%)
- Mandatory "reduce position" advice for deep loss + distribution stocks
- Stop-loss distance display for each holding

📊 **Rebound Space Calculation**
- Auto-calculate rebound percentage to resistance level
- Smart advice based on rebound space (<1%, <2%, >5%)
- Actionable "wait" or "reduce" recommendations

🚨 **Smart Alerts**
- Automatic stop-loss trigger alerts
- Resistance proximity warnings (within 1%)
- Deep loss warnings (>10% loss)
- Pressure/Support level display

## Previous Features (v4.7)

- Intraday prediction engine (morning/noon/afternoon)
- Tomorrow forecast with support/resistance
- Financial bomb detection
- Anti-sell-off protection
- Time-based smart recommendations

## Quick Start

```python
from stock_analyzer_pro import PerfectTradingSystemV48, add_stock_news

system = PerfectTradingSystemV48()
add_stock_news('600406', 'Company wins major contract')

holdings = [
    ('600406', 'Stock Name', 25.0, 1000, 24.0, 28.0),  # code, name, cost, qty, stop, target
]

system.generate_report(holdings)
```

## v4.8 Output Example

```
【国电南瑞 (600406)】
   价格: 26.86元 (今日+0.00%)
   盈亏: 2,604元 (+6.91%)
   
   🎯 关键价位:
      压力位: 27.70元
      支撑位: 26.75元
      反弹空间: 3.13%
      反弹建议: 正常反弹空间，按原策略执行
   
   🛡️ 止损距离: 11.4%
   
   💡 操作建议: 🟢 持有
      理由: 强势，可持有或加仓
```

## Installation

```bash
git clone https://github.com/dhwangluo-eng/stock-analyzer.git
cd stock-analyzer
pip install -r requirements.txt
```

## License

MIT License

## Version History

- **v4.8**: Enhanced stop-loss protection, rebound space calculation, smart alerts
- v4.7: Intraday prediction, tomorrow forecast, anti-sell-off protection
- v4.6: Multi-period MA, fund flow detection, news sentiment

## Author

Created for OpenClaw Stock Analysis System
Version: 4.8