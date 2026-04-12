# Stock Analyzer Skill for OpenClaw

基于7维度预测体系的股票技术分析工具，为 OpenClaw 开发的技能插件。

## 🎯 功能特点

- ✅ **7维度评分体系**：技术面、RSI、KDJ、资金流向、新闻、大盘、板块
- ✅ **实时数据**：连接新浪/东方财富，数据实时更新  
- ✅ **智能预测**：基于历史数据回测，给出买卖建议
- ✅ **简单易用**：命令行一键分析，输出清晰

## 📊 7维度评分体系

| 维度 | 权重 | 说明 |
|:---:|:---:|:---|
| MA均线 | 30% | 5日/10日/20日均线排列 |
| RSI指标 | 15% | 超买超卖判断 |
| KDJ指标 | 15% | 金叉死叉信号 |
| 资金流向 | 20% | 量比、换手率 |
| 新闻舆情 | 10% | 利好利空分析 |
| 大盘环境 | 5% | 市场强弱 |
| 板块轮动 | 5% | 所属板块表现 |

## 🚀 安装

### 方式1：OpenClaw 技能市场（推荐）
```bash
openclaw skills install stock-analyzer
```

### 方式2：手动安装
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/dhwangluo-eng/stock-analyzer.git
```

### 依赖
- Python 3.9+
- OpenClaw ≥ 2026.4.0
- stock-cli 插件（OpenClaw 自带）

## 💡 使用方法

### 命令行
```bash
# 分析单只股票
python3 stock_analyzer.py 600406

# 分析多只股票
python3 stock_analyzer.py 600406
python3 stock_analyzer.py 000001
python3 stock_analyzer.py 000998
```

### 作为 OpenClaw Skill 调用
```
用户: 分析股票 600406
Skill: [自动调用 stock_analyzer.py 返回报告]
```

## 📈 输出示例

```
==================================================
【股票分析报告】国电南瑞(600406)
==================================================

📊 实时行情
   价格: 26.36元 (+1.54%)

📈 技术指标
   MA5: 26.21 | MA10: 26.41 | MA20: 26.83
   RSI: 48.01
   KDJ: K=37.19 D=24.44 J=62.69
   量比: 0.96

🎯 综合评分: 10分
   预测: 🟡 震荡偏强
   建议: 观望为主
   
📋 关键信号:
   短期均线走弱 | RSI健康 | KDJ金叉

==================================================
💡 获取更多功能
   加入Telegram群组获取完整7维度分析
   加入免费群：每日早盘9:00推送3只关注股
==================================================
```

## 🎯 评分标准

| 分数 | 预测 | 建议 |
|:---:|:---:|:---|
| ≥30分 | 🟢 偏强 | 可考虑买入/持有 |
| 10-29分 | 🟡 震荡偏强 | 观望为主 |
| -10-9分 | ⚪ 震荡 | 谨慎操作 |
| <-10分 | 🔴 偏弱 | 建议减仓/回避 |

## 🔧 自定义配置

编辑 `stock_analyzer.py` 修改底部引流信息：

```python
# 第117-118行，替换为你的信息
print("   Telegram群组: https://t.me/weiduchaogu")
print("   加入免费群: [你的群链接]")
```

## 📚 相关项目

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 操作系统
- [stock-cli](https://github.com/openclaw/stock-cli) - 股票行情 CLI 工具

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0.0 (2026-04-12)
- 初始版本发布
- 实现7维度评分体系
- 支持实时行情获取
- 支持技术指标分析

## ⚠️ 免责声明

本工具仅供参考，不构成投资建议。股市有风险，投资需谨慎。

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 💬 联系

- **Telegram群组**: https://t.me/weiduchaogu
- **GitHub Issues**: https://github.com/dhwangluo-eng/stock-analyzer/issues

---

⭐ 如果这个项目对你有帮助，请给个 Star！
