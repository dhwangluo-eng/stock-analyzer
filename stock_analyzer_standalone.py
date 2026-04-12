#!/usr/bin/env python3
"""
Stock Analyzer GUI - 独立版本
桌面图形界面，内置数据获取，无需外部依赖
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import urllib.request
import urllib.parse
from datetime import datetime

class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股票分析助手 v1.0 - 7维度预测体系")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 11))
        self.style.configure('TLabel', font=('Arial', 11))
        
        self.create_ui()
        
    def create_ui(self):
        title = tk.Label(self.root, text="📊 股票分析助手", font=('Arial', 20, 'bold'))
        title.pack(pady=10)
        
        subtitle = tk.Label(self.root, text="基于7维度预测体系的技术分析工具", font=('Arial', 12))
        subtitle.pack()
        
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
        
        result_frame = tk.LabelFrame(self.root, text="分析结果", font=('Arial', 12))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, font=('Courier', 11), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status = tk.Label(self.root, text="就绪", font=('Arial', 10), 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        footer = tk.Label(self.root, text="Telegram: https://t.me/weiduchaogu | 实时交流，获取最新分析", 
                         font=('Arial', 10), fg='blue', cursor='hand2')
        footer.pack(pady=5)
        footer.bind('<Button-1>', lambda e: self.open_link())
        
    def open_link(self):
        import webbrowser
        webbrowser.open('https://t.me/weiduchaogu')
        
    def get_stock_data(self, code):
        """从新浪财经获取股票数据"""
        try:
            # 格式化代码
            if code.startswith('6'):
                full_code = f"sh{code}"
            elif code.startswith('0') or code.startswith('3'):
                full_code = f"sz{code}"
            else:
                full_code = code
            
            url = f"https://hq.sinajs.cn/list={full_code}"
            headers = {'Referer': 'https://finance.sina.com.cn'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('gbk')
                
            # 解析数据
            if '=' in data:
                content = data.split('=')[1].strip('";\n')
                parts = content.split(',')
                if len(parts) >= 33:
                    name = parts[0]
                    today_open = float(parts[1])
                    yesterday_close = float(parts[2])
                    current_price = float(parts[3])
                    change_pct = (current_price - yesterday_close) / yesterday_close * 100
                    volume = float(parts[4])
                    
                    return {
                        'name': name,
                        'price': current_price,
                        'change_pct': change_pct,
                        'open': today_open,
                        'volume': volume
                    }
            return None
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_stock(self):
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showwarning("提示", "请输入股票代码")
            return
            
        self.status.config(text=f"正在分析 {code}...")
        self.root.update()
        
        thread = threading.Thread(target=self._do_analyze, args=(code,))
        thread.start()
        
    def _do_analyze(self, code):
        try:
            data = self.get_stock_data(code)
            
            if data is None:
                self.root.after(0, lambda: self._show_error("无法获取股票数据，请检查代码是否正确"))
                return
            
            if 'error' in data:
                self.root.after(0, lambda: self._show_error(data['error']))
                return
            
            # 简化评分（仅基于价格和涨跌）
            price = data['price']
            change_pct = data['change_pct']
            
            score = 0
            reasons = []
            
            if change_pct > 0:
                score += 10
                reasons.append("当日上涨")
            elif change_pct < -2:
                score -= 10
                reasons.append("当日大跌")
            
            if change_pct > 5:
                score += 10
                reasons.append("强势上涨")
            elif change_pct < -5:
                score -= 15
                reasons.append("超跌")
            
            if score >= 15:
                prediction = "🟢 偏强"
                advice = "可考虑关注"
            elif score >= 0:
                prediction = "🟡 中性偏强"
                advice = "观望为主"
            elif score >= -10:
                prediction = "⚪ 震荡"
                advice = "谨慎操作"
            else:
                prediction = "🔴 偏弱"
                advice = "建议回避"
            
            report = f"""
{'='*60}
【股票分析报告】{data['name']}({code})
{'='*60}

📊 实时行情
   价格: {price:.2f}元 ({change_pct:+.2f}%)
   今开: {data['open']:.2f}元

🎯 简评评分: {score}分
   预测: {prediction}
   建议: {advice}
   
📋 信号:
   {' | '.join(reasons) if reasons else '暂无明确信号'}

{'='*60}
💡 获取完整7维度深度分析
   Telegram群组: https://t.me/weiduchaogu
   实时交流，获取实时预警和专业分析
{'='*60}

⚠️ 免责声明：本工具仅供参考，不构成投资建议
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
        self.result_text.insert(tk.END, f"❌ 分析失败: {error}\n\n请检查:\n1. 股票代码是否正确（如 600406, 000001）\n2. 网络连接是否正常\n\n支持代码格式:\n- 沪市: 600xxx, 601xxx, 603xxx\n- 深市: 000xxx, 002xxx, 300xxx")
        self.status.config(text="分析失败")

def main():
    root = tk.Tk()
    app = StockAnalyzerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
