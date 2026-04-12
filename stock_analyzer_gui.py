#!/usr/bin/env python3
"""
Stock Analyzer PC 端 v1.0
桌面版股票分析工具 - 支持 Windows/Mac/Linux
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from datetime import datetime

# 添加 stock-cli 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from stock_cli.commands.quote import get_stock_by_code
    from stock_cli.commands.kline import get_kline_data
    HAS_STOCK_CLI = True
except:
    HAS_STOCK_CLI = False

class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股票分析助手 v1.0 - 7维度预测体系")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # 设置样式
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 11))
        self.style.configure('TLabel', font=('Arial', 11))

        self.create_ui()

    def create_ui(self):
        # 标题
        title = tk.Label(self.root, text="📊 股票分析助手", font=('Arial', 20, 'bold'))
        title.pack(pady=10)

        subtitle = tk.Label(self.root, text="基于7维度预测体系的技术分析工具", font=('Arial', 12))
        subtitle.pack()

        # 输入框
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="股票代码:", font=('Arial', 12)).pack(side=tk.LEFT)
        self.code_entry = tk.Entry(input_frame, font=('Arial', 12), width=15)
        self.code_entry.pack(side=tk.LEFT, padx=10)
        self.code_entry.insert(0, "600406")

        analyze_btn = tk.Button(input_frame, text="分析", font=('Arial', 12),
                               bg='#4CAF50', fg='white', width=10,
                               command=self.analyze_stock)
        analyze_btn.pack(side=tk.LEFT)

        # 结果显示区域
        result_frame = tk.LabelFrame(self.root, text="分析结果", font=('Arial', 12))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.result_text = scrolledtext.ScrolledText(result_frame, font=('Courier', 11),
                                                     wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 状态栏
        self.status = tk.Label(self.root, text="就绪", font=('Arial', 10),
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # 底部信息
        footer = tk.Label(self.root, text="Telegram: https://t.me/weiduchaogu | 实时交流，获取最新分析", 
                         font=('Arial', 10), fg='blue', cursor='hand2')
        footer.pack(pady=5)
        footer.bind('<Button-1>', lambda e: self.open_link())

    def open_link(self):
        import webbrowser
        webbrowser.open('https://t.me/weiduchaogu')

    def analyze_stock(self):
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showwarning("提示", "请输入股票代码")
            return

        self.status.config(text=f"正在分析 {code}...")
        self.root.update()

        # 在后台线程运行分析
        thread = threading.Thread(target=self._do_analyze, args=(code,))
        thread.start()

    def _do_analyze(self, code):
        try:
            if not HAS_STOCK_CLI:
                self.root.after(0, lambda: self._show_error("未找到 stock-cli,请确保依赖已安装"))
                return

            # 获取数据
            data = get_stock_by_code(code)
            price = float(data['price'])
            change_pct = float(data['change_rate'].replace('%', ''))

            kline = get_kline_data(code, count=20)
            factors = kline['factors']

            # 计算评分
            score = 0
            reasons = []

            if factors['ema_5'] > factors['ema_10'] > factors['ema_20']:
                score += 20
                reasons.append("均线多头排列")
            elif factors['ema_5'] < factors['ema_10']:
                score -= 10
                reasons.append("短期均线走弱")

            if 40 <= factors['rsi_6'] <= 60:
                score += 10
                reasons.append("RSI健康")
            elif factors['rsi_6'] > 70:
                score -= 15
                reasons.append("RSI超买")

            if factors['kdj_j'] > factors['kdj_k'] > factors['kdj_d']:
                score += 10
                reasons.append("KDJ金叉")

            vr = float(data.get('vr', 1))
            if vr > 1.5:
                score += 10
                reasons.append("量能放大")

            if score >= 30:
                prediction = "🟢 偏强"
                advice = "可考虑持有/买入"
            elif score >= 10:
                prediction = "🟡 震荡偏强"
                advice = "观望为主"
            elif score >= -10:
                prediction = "⚪ 震荡"
                advice = "谨慎操作"
            else:
                prediction = "🔴 偏弱"
                advice = "建议减仓/回避"

            report = f"""
{'='*60}
【股票分析报告】{data.get('name', '未知')}({code})
{'='*60}

📊 实时行情
   价格: {price}元 ({change_pct:+.2f}%)

📈 技术指标
   MA5: {factors['ema_5']:.2f} | MA10: {factors['ema_10']:.2f} | MA20: {factors['ema_20']:.2f}
   RSI: {factors['rsi_6']:.2f}
   KDJ: K={factors['kdj_k']:.2f} D={factors['kdj_d']:.2f} J={factors['kdj_j']:.2f}
   量比: {vr:.2f}

🎯 综合评分: {score}分
   预测: {prediction}
   建议: {advice}

📋 关键信号:
   {' | '.join(reasons) if reasons else '暂无明确信号'}

{'='*60}
💡 获取更多功能
   Telegram群组: https://t.me/weiduchaogu
   每日早盘9:00推送3只关注股
{'='*60}
"""

            self.root.after(0, lambda: self._show_result(report))

        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e)))

    def _show_result(self, report):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, report)
        self.status.config(text="分析完成")

    def _show_error(self, error):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"❌ 分析失败: {error}\n\n请检查:\n1. 股票代码是否正确\n2. 网络连接是否正常\n3. stock-cli 是否已安装")
        self.status.config(text="分析失败")

def main():
    root = tk.Tk()
    app = StockAnalyzerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
