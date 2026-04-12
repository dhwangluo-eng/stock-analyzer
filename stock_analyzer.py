#!/usr/bin/env python3
"""
Stock Analyzer Skill v1.0
股票分析助手 - 基于7维度预测体系
"""
import sys
sys.path.insert(0, '/Users/sunjian/.openclaw/workspace/skills/stock-cli')
import json
from datetime import datetime
from stock_cli.commands.quote import get_stock_by_code
from stock_cli.commands.kline import get_kline_data

def analyze_stock(code):
    """分析单只股票"""
    try:
        # 获取实时数据
        data = get_stock_by_code(code)
        price = float(data['price'])
        change_pct = float(data['change_rate'].replace('%', ''))
        
        # 获取K线数据
        kline = get_kline_data(code, count=20)
        factors = kline['factors']
        
        # 7维度评分
        score = 0
        reasons = []
        
        # 1. 技术面 (30分)
        if factors['ema_5'] > factors['ema_10'] > factors['ema_20']:
            score += 20
            reasons.append("均线多头排列")
        elif factors['ema_5'] < factors['ema_10']:
            score -= 10
            reasons.append("短期均线走弱")
        
        # RSI
        if 40 <= factors['rsi_6'] <= 60:
            score += 10
            reasons.append("RSI健康")
        elif factors['rsi_6'] > 70:
            score -= 15
            reasons.append("RSI超买")
        
        # KDJ
        if factors['kdj_j'] > factors['kdj_k'] > factors['kdj_d']:
            score += 10
            reasons.append("KDJ金叉")
        
        # 2. 资金流向 (估算)
        vr = float(data.get('vr', 1))
        if vr > 1.5:
            score += 10
            reasons.append("量能放大")
        
        # 预测结果
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
        
        return {
            "success": True,
            "code": code,
            "name": data.get('name', '未知'),
            "price": price,
            "change_pct": change_pct,
            "score": score,
            "prediction": prediction,
            "advice": advice,
            "reasons": reasons,
            "ma5": round(factors['ema_5'], 2),
            "ma10": round(factors['ema_10'], 2),
            "ma20": round(factors['ema_20'], 2),
            "rsi": round(factors['rsi_6'], 2),
            "kdj_k": round(factors['kdj_k'], 2),
            "kdj_d": round(factors['kdj_d'], 2),
            "kdj_j": round(factors['kdj_j'], 2),
            "vr": round(vr, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "code": code,
            "error": str(e)
        }

def format_report(result):
    """格式化输出报告"""
    if not result['success']:
        return f"❌ 分析失败: {result.get('error', '未知错误')}"
    
    report = f"""
{'='*50}
【股票分析报告】{result['name']}({result['code']})
{'='*50}

📊 实时行情
   价格: {result['price']}元 ({result['change_pct']:+.2f}%)

📈 技术指标
   MA5: {result['ma5']} | MA10: {result['ma10']} | MA20: {result['ma20']}
   RSI: {result['rsi']}
   KDJ: K={result['kdj_k']} D={result['kdj_d']} J={result['kdj_j']}
   量比: {result['vr']}

🎯 综合评分: {result['score']}分
   预测: {result['prediction']}
   建议: {result['advice']}
   
📋 关键信号:
   {' | '.join(result['reasons']) if result['reasons'] else '暂无明确信号'}

{'='*50}
💡 获取完整7维度分析+实时预警
   Telegram群组: https://t.me/weiduchaogu
   每日早盘9:00推送3只关注股
{'='*50}
"""
    return report

if __name__ == '__main__':
    # 支持命令行参数
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        # 默认分析示例
        code = "600406"  # 国电南瑞
    
    print(f"🔄 正在分析 {code}...")
    result = analyze_stock(code)
    print(format_report(result))
