# Stock Analyzer Pro v4.8

Professional stock analysis system with **enhanced stop-loss protection**, **rebound space calculation**, and **smart alerts**.

## What's New in v4.8

### 🛡️ Enhanced Stop-Loss Protection
- Deep loss penalty: -20 points (>10% loss), -25 points (>15% loss)
- Mandatory "reduce position" for deep loss + distribution stocks
- Real-time stop-loss distance calculation for each holding

### 📊 Rebound Space Calculation
- Auto-calculate: `(resistance - current_price) / current_price * 100%`
- Smart advice tiers:
  - <1%: "开盘即减仓，不等待"
  - <2%: "小幅反弹即减仓"
  - >5%: "有做T空间，等压力位"

### 🚨 Smart Alerts System
- **Stop-loss alerts**: Triggered when price ≤ stop_loss
- **Resistance alerts**: Warning when within 1% of resistance
- **Deep loss alerts**: Warning when loss >10%
- **Pressure/Support display**: Real-time key levels

## Previous v4.7 Features
- Intraday prediction (morning/noon/afternoon)
- Tomorrow forecast with support/resistance
- Financial bomb detection
- Anti-sell-off protection
- Time-based recommendations

## Installation

```bash
git clone https://github.com/dhwangluo-eng/stock-analyzer.git
cd stock-analyzer
pip install -r requirements.txt
```

## Usage

```python
from stock_analyzer_pro import PerfectTradingSystemV48, add_stock_news

system = PerfectTradingSystemV48()
add_stock_news('600406', 'Company wins major contract')

holdings = [
    ('600406', 'Stock Name', 25.0, 1000, 24.0, 28.0),
]

system.generate_report(holdings)
```

## Output Format

```
【股票名称 (代码)】
   价格: XX.XX元
   盈亏: X,XXX元 (+X.XX%)
   
   🎯 关键价位:
      压力位: XX.XX元
      支撑位: XX.XX元
      反弹空间: X.XX%
      反弹建议: [根据空间生成]
   
   📊 综合评分: XX/100
   🔮 1-2日预测: [预测结果]
   
   💡 操作建议: [操作建议]
      理由: [操作理由]
      🛡️ 止损距离: X.X%
```

## Data Sources
- Real-time price: Sina Finance API
- K-line data: Tencent Finance API
- News: User input via `add_stock_news()`

## Requirements
- Python 3.7+
- No external dependencies (standard library only)

## Changelog

### v4.8.0 (2026-04-15)
- ✅ Enhanced stop-loss protection
- ✅ Rebound space calculation
- ✅ Smart alerts system
- ✅ Pressure/Support level display

### v4.7.0 (2026-04-14)
- ✅ Intraday prediction engine
- ✅ Tomorrow forecast
- ✅ Financial bomb detection
- ✅ Anti-sell-off protection

### v4.6.0 (2026-04-12)
- Multi-period MA analysis
- Volume trend detection
- Fund flow detection
- News sentiment analysis

## License

MIT License

## Author

Created for OpenClaw Stock Analysis System
Version: 4.8