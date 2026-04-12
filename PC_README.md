# PC 端打包指南

## 📦 Stock Analyzer PC 端

桌面图形界面版本，支持 Windows/Mac/Linux。

## 🎯 功能特点

- ✅ 图形界面（GUI），无需命令行
- ✅ 输入股票代码，一键分析
- ✅ 实时显示7维度评分报告
- ✅ 支持所有A股代码

## 📥 下载地址

### 预编译版本（推荐）

| 系统 | 下载 | 说明 |
|:---:|:---:|:---|
| **Windows** | [下载 stock-analyzer-win.exe](https://github.com/dhwangluo-eng/stock-analyzer/releases) | 双击运行 |
| **Mac** | [下载 stock-analyzer-mac.app](https://github.com/dhwangluo-eng/stock-analyzer/releases) | 拖入应用程序 |
| **Linux** | [下载 stock-analyzer-linux](https://github.com/dhwangluo-eng/stock-analyzer/releases) | 命令行运行 |

### 源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/dhwangluo-eng/stock-analyzer.git
cd stock-analyzer

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 运行 GUI 版本
python3 stock_analyzer_gui.py
```

## 🔨 自行打包

### Windows 打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 打包
pyinstaller --onefile --windowed --name stock-analyzer-win stock_analyzer_gui.py

# 3. 输出在 dist/stock-analyzer-win.exe
```

### Mac 打包

```bash
# 1. 安装 PyInstaller
pip3 install pyinstaller

# 2. 打包
pyinstaller --onefile --windowed --name stock-analyzer-mac stock_analyzer_gui.py

# 3. 输出在 dist/stock-analyzer-mac.app
```

### Linux 打包

```bash
# 1. 安装 PyInstaller
pip3 install pyinstaller

# 2. 打包
pyinstaller --onefile --name stock-analyzer-linux stock_analyzer_gui.py

# 3. 输出在 dist/stock-analyzer-linux
```

## 📋 打包注意事项

### 包含依赖

创建 `requirements.txt`:
```
stock-cli @ git+https://github.com/openclaw/stock-cli.git
```

或使用 `--add-data` 包含 stock-cli:
```bash
pyinstaller --onefile --windowed \
  --add-data "skills/stock-cli:lib/stock-cli" \
  --name stock-analyzer-win \
  stock_analyzer_gui.py
```

### 减小体积

使用 UPX 压缩:
```bash
pyinstaller --onefile --windowed --upx-dir /path/to/upx ...
```

## 🖥️ 界面预览

```
┌─────────────────────────────────────────┐
│  📊 股票分析助手 v1.0                    │
│  基于7维度预测体系的技术分析工具          │
├─────────────────────────────────────────┤
│  股票代码: [600406    ] [  分析  ]      │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │ 【股票分析报告】国电南瑞(600406) │    │
│  │                                 │    │
│  │ 📊 实时行情                     │    │
│  │    价格: 26.36元 (+1.54%)       │    │
│  │                                 │    │
│  │ 📈 技术指标                     │    │
│  │    MA5: 26.21 | MA10: 26.41     │    │
│  │    RSI: 48.01                   │    │
│  │                                 │    │
│  │ 🎯 综合评分: 10分               │    │
│  │    预测: 🟡 震荡偏强             │    │
│  │    建议: 观望为主                │    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│  Telegram: https://t.me/weiduchaogu    │
└─────────────────────────────────────────┘
```

## ⚠️ 注意事项

1. **首次运行慢**：打包后的 .exe 启动需要解压，首次运行较慢
2. **杀毒软件**：部分杀毒软件可能误报，请添加信任
3. **网络依赖**：需要联网获取实时行情数据
4. **系统要求**：Windows 7+/macOS 10.12+/Linux

## 📞 支持

- **Telegram群组**: https://t.me/weiduchaogu
- **GitHub Issues**: https://github.com/dhwangluo-eng/stock-analyzer/issues

## 📄 许可证

MIT License
