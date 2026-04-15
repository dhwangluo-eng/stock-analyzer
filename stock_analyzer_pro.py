#!/usr/bin/env python3
"""
完美交易系统 v4.8 - 智能止损优化版
=====================================
优化点：
1. 深套惩罚加强 (>10%亏损强制建议减仓)
2. 反弹空间计算 (明确可操作策略)
3. 自动止损提醒 (跌破止损位主动预警)
4. 减仓时机智能提醒 (接近压力位±1%提醒)
5. 主力信号加重惩罚 (主力出货+深套时预测封顶)
"""
import sqlite3
import json
import urllib.request
from datetime import datetime, timedelta

# 全局新闻输入存储
STOCK_NEWS = {}

def add_stock_news(code, news_text):
    """添加股票新闻"""
    if code not in STOCK_NEWS:
        STOCK_NEWS[code] = []
    STOCK_NEWS[code].append({
        'text': news_text,
        'time': datetime.now().strftime('%H:%M')
    })

def get_stock_news(code):
    """获取股票新闻"""
    return STOCK_NEWS.get(code, [])

class NewsAnalyzer:
    """新闻情绪分析器"""
    
    def __init__(self):
        self.strong_positive = ['涨停','翻倍','暴增','净利润增长超50%','重大合同','中标','收购','并购',
            '重组','借壳','上市','IPO','定增','回购','增持','分红','高送转','技术突破','专利','独家']
        self.positive = ['增长','上涨','盈利','订单','中标','合作','签约','扩产','涨价','供不应求',
            '产能释放','政策支持','补贴','税收优惠','机构买入','评级上调','目标价上调']
        self.strong_negative = ['跌停','暴跌','亏损','业绩暴雷','财务造假','调查','处罚','退市','ST',
            '停牌','债务违约','破产','重组失败','大股东减持','清仓减持','质押爆仓','诉讼']
        self.negative = ['下降','下滑','亏损','减持','解禁','质押','裁员','停产','限产','降价',
            '价格战','毛利率下降','订单取消','客户流失','评级下调','卖出评级','机构卖出']
        
        # 财务暴雷专项词典
        self.financial_bomb = {
            '营收下降': -15,
            '净利润亏损': -20,
            '业绩亏损': -20,
            '由盈转亏': -25,
            '同比下降': -10,
            '营收下滑': -15,
            '利润下滑': -15,
            '净利润下滑': -15,
            '营收同比': -10,
            '利润同比': -10
        }
    
    def analyze(self, text):
        """分析文本情绪"""
        if not text:
            return {'score': 0, 'sentiment': '⚪ 无数据', 'reasons': []}
        
        score = 0
        reasons = []
        text_lower = text.lower()
        
        for word in self.strong_positive:
            if word in text_lower:
                score += 20
                reasons.append(f'🟢 强烈利好: {word}')
        
        for word in self.positive:
            if word in text_lower and word not in [r.split(': ')[1] for r in reasons]:
                score += 10
                reasons.append(f'🟢 利好: {word}')
        
        for word in self.strong_negative:
            if word in text_lower:
                score -= 20
                reasons.append(f'🔴 强烈利空: {word}')
        
        for word in self.negative:
            if word in text_lower and word not in [r.split(': ')[1] for r in reasons]:
                score -= 10
                reasons.append(f'🔴 利空: {word}')
        
        # 财务暴雷额外扣分
        for keyword, penalty in self.financial_bomb.items():
            if keyword in text_lower:
                score += penalty
                if not any(keyword in r for r in reasons):
                    reasons.append(f'🔴 财务利空: {keyword}')
        
        if score >= 20:
            sentiment = '🟢 强烈利好'
        elif score >= 10:
            sentiment = '🟢 利好'
        elif score <= -30:
            sentiment = '🔴 严重利空'
        elif score <= -20:
            sentiment = '🔴 强烈利空'
        elif score <= -10:
            sentiment = '🔴 利空'
        else:
            sentiment = '⚪ 中性'
        
        return {'score': score, 'sentiment': sentiment, 'reasons': reasons[:3]}


class PerfectTradingSystemV48:
    """完美交易系统 v4.8 - 智能止损优化版"""
    
    def __init__(self, db_path='/Users/sunjian/.openclaw/workspace/trading_records.db'):
        self.db_path = db_path
        self.news_analyzer = NewsAnalyzer()
        self.init_database()
        
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, code TEXT, name TEXT, action TEXT,
            price REAL, quantity INTEGER, amount REAL, reason TEXT, stop_loss REAL, target REAL,
            pnl REAL, pnl_pct REAL, holding_days INTEGER, prediction TEXT, score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    
    def get_stock_data(self, code):
        """从新浪财经获取数据"""
        try:
            full_code = f"sh{code}" if code.startswith('6') else f"sz{code}"
            url = f"https://hq.sinajs.cn/list={full_code}"
            req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('gbk')
            if '=' in data:
                content = data.split('=')[1].strip('";\n')
                parts = content.split(',')
                if len(parts) >= 33:
                    price = float(parts[3])
                    if price == 0:
                        price = float(parts[2])
                    return {
                        'name': parts[0], 'price': price,
                        'open': float(parts[1]) if float(parts[1]) > 0 else float(parts[2]),
                        'high': float(parts[4]) if float(parts[4]) > 0 else float(parts[2]),
                        'low': float(parts[5]) if float(parts[5]) > 0 else float(parts[2]),
                        'volume': float(parts[8]),
                        'change_pct': float(parts[32]),
                        'turnover': float(parts[8]) * 100 / 100000000,
                        'success': True
                    }
            return {'success': False, 'error': '无数据'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_kline_tencent(self, code, period='day', days=250):
        """获取多周期K线数据"""
        try:
            full_code = f"sh{code}" if code.startswith('6') else f"sz{code}"
            url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={full_code},{period},,,{days},qfq"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            kline = data.get('data', {}).get(full_code, {})
            lines = kline.get('qfqday', []) or kline.get('day', [])
            
            if len(lines) < 10:
                return None
            
            opens = [float(item[1]) for item in lines]
            closes = [float(item[2]) for item in lines]
            lows = [float(item[3]) for item in lines]
            highs = [float(item[4]) for item in lines]
            volumes = [float(item[5]) for item in lines] if len(lines[0]) > 5 else []
            
            def ma(data, period):
                if len(data) < period:
                    return None
                return sum(data[-period:]) / period
            
            # 昨日K线形态分析
            y_open, y_close, y_high, y_low = opens[-2], closes[-2], highs[-2], lows[-2]
            y_body = abs(y_close - y_open)
            y_range = y_high - y_low if y_high > y_low else 0.001
            y_upper_shadow = y_high - max(y_open, y_close)
            y_lower_shadow = min(y_open, y_close) - y_low
            
            candle_pattern = []
            if y_body / y_range < 0.1:
                candle_pattern.append("十字星")
            elif y_close > y_open:
                candle_pattern.append("阳线")
                if y_lower_shadow > y_body * 2 and y_upper_shadow < y_body * 0.5:
                    candle_pattern.append("锤子线")
                if y_body / y_range > 0.8:
                    candle_pattern.append("光头光脚")
            else:
                candle_pattern.append("阴线")
                if y_upper_shadow > y_body * 2 and y_lower_shadow < y_body * 0.5:
                    candle_pattern.append("流星线")
            
            # 成交量异动持续性
            volume_sustain = 1.0
            if volumes and len(volumes) >= 12:
                v_recent = sum(volumes[-3:]) / 3
                v_mid = sum(volumes[-7:-4]) / 3
                v_prev = sum(volumes[-11:-8]) / 3
                if v_mid > 0 and v_prev > 0:
                    r1 = v_recent / v_mid
                    r2 = v_mid / v_prev
                    if r1 > 1.2 and r2 > 1.1:
                        volume_sustain = 1.3
                    elif r1 > 1.2 and r2 < 0.9:
                        volume_sustain = 1.0
                    elif r1 < 0.8 and r2 < 0.9:
                        volume_sustain = 0.6
                    elif r1 < 0.8 and r2 > 1.1:
                        volume_sustain = 0.8
            
            # 计算各周期均线
            result = {
                'closes': closes,
                'opens': opens,
                'highs': highs,
                'lows': lows,
                'current': closes[-1],
                'ma5': ma(closes, 5),
                'ma10': ma(closes, 10),
                'ma20': ma(closes, 20),
                'ma30': ma(closes, 30),
                'ma60': ma(closes, 60),
                'ma120': ma(closes, 120),
                'ma250': ma(closes, 250),
                'trend': 'up' if closes[-1] > closes[0] else 'down',
                'volatility': (max(closes) - min(closes)) / closes[0] * 100,
                'candle_pattern': candle_pattern,
                'volume_sustain': volume_sustain,
                'yesterday_close': y_close,
                'yesterday_open': y_open
            }
            
            if volumes and len(volumes) >= 5:
                recent_vol = sum(volumes[-5:]) / 5
                prev_vol = sum(volumes[-10:-5]) / 5 if len(volumes) >= 10 else recent_vol
                result['volume_trend'] = 'up' if recent_vol > prev_vol * 1.2 else 'down' if recent_vol < prev_vol * 0.8 else 'flat'
                result['volume_ratio'] = recent_vol / prev_vol if prev_vol > 0 else 1.0
            
            return result
        except:
            return None
    
    def get_market_sentiment(self):
        """获取大盘情绪指数"""
        try:
            market_kline = self.get_kline_tencent('000001', days=60)
            if not market_kline:
                return {'score': 0, 'sentiment': '⚪ 中性', 'trend': 'flat'}
            
            m_price = market_kline['current']
            m_ma5 = market_kline.get('ma5')
            m_ma10 = market_kline.get('ma10')
            m_ma20 = market_kline.get('ma20')
            m_y_close = market_kline.get('yesterday_close', m_price)
            m_change = (m_price - m_y_close) / m_y_close * 100 if m_y_close else 0
            
            score = 0
            sentiment = '⚪ 中性'
            factors = []
            
            if m_change > 1.5:
                score += 20
                factors.append("大盘大涨")
            elif m_change > 0.5:
                score += 10
                factors.append("大盘小涨")
            elif m_change < -1.5:
                score -= 20
                factors.append("大盘大跌")
            elif m_change < -0.5:
                score -= 10
                factors.append("大盘小跌")
            
            if m_ma5 and m_price > m_ma5:
                score += 5
                factors.append("大盘站上MA5")
            if m_ma10 and m_price > m_ma10:
                score += 5
                factors.append("大盘站上MA10")
            if m_ma20 and m_price > m_ma20:
                score += 5
                factors.append("大盘站上MA20")
            
            if market_kline.get('volume_sustain', 1.0) > 1.2:
                score += 5
                factors.append("大盘放量")
            
            if score >= 20:
                sentiment = '🟢 强势'
            elif score >= 10:
                sentiment = '🟢 偏多'
            elif score <= -20:
                sentiment = '🔴 弱势'
            elif score <= -10:
                sentiment = '🔴 偏空'
            
            trend = 'up' if score >= 10 else 'down' if score <= -10 else 'flat'
            return {'score': score, 'sentiment': sentiment, 'trend': trend, 'factors': factors, 'change': m_change}
        except:
            return {'score': 0, 'sentiment': '⚪ 中性', 'trend': 'flat', 'factors': [], 'change': 0}
    
    # ============== v4.8 核心优化 ==============
    
    def calculate_rebound_space(self, price, resistance, support):
        """v4.8 新增：计算反弹空间"""
        if resistance and price > 0:
            rebound_pct = (resistance - price) / price * 100
            return rebound_pct
        return 0
    
    def generate_rebound_advice(self, rebound_pct, is_deep_loss, has_distribution):
        """v4.8 新增：基于反弹空间的操作建议"""
        if rebound_pct < 1:
            if is_deep_loss:
                return "🔴 压力位太近，反弹空间<1%，建议开盘即减仓"
            else:
                return "⚠️ 反弹空间有限，不等待反弹"
        elif rebound_pct < 2:
            if is_deep_loss:
                return "🟡 压力位较近，小幅反弹即减仓减亏"
            else:
                return "🟡 反弹空间2%以内，可持有等待"
        elif rebound_pct > 5:
            return "🟢 有5%+做T空间，可等压力位附近减仓"
        else:
            return "➡️ 正常反弹空间，按原策略执行"
    
    def check_stop_loss_alert(self, price, stop_loss, profit_pct, code, name):
        """v4.8 新增：止损提醒检查"""
        alerts = []
        
        # 1. 已跌破止损
        if price <= stop_loss:
            alerts.append(f"🚨【止损触发】{name}({code}) 当前价{price:.2f} 已跌破止损位{stop_loss:.2f}，建议立即卖出！")
        
        # 2. 接近止损（2%以内）
        stop_distance_pct = (price - stop_loss) / stop_loss * 100
        if 0 < stop_distance_pct <= 2:
            alerts.append(f"⚠️【接近止损】{name}({code}) 距离止损位仅{stop_distance_pct:.1f}%，密切关注！")
        
        # 3. 深套股继续恶化
        if profit_pct < -10:
            alerts.append(f"🔴【深套警告】{name}({code}) 已深套{profit_pct:.1f}%，禁止补仓！")
        
        return alerts
    
    def check_resistance_alert(self, price, resistance, code, name):
        """v4.8 新增：压力位减仓提醒"""
        if resistance and price > 0:
            distance_pct = abs(price - resistance) / price * 100
            if distance_pct <= 1:
                if price >= resistance:
                    return f"🎯【压力位到达】{name}({code}) 已达到压力位{resistance:.2f}，建议减仓！"
                else:
                    return f"⏰【接近压力】{name}({code}) 距离压力位{resistance:.2f} 仅{distance_pct:.1f}%"
        return None
    
    # ============== v4.8 分析主函数 ==============
    
    def analyze_stock(self, code, name, cost, qty, stop_loss, target):
        """v4.8 综合分析单只股票"""
        data = self.get_stock_data(code)
        if not data['success']:
            return None
        
        price = data['price']
        profit_pct = ((price - cost) / cost) * 100
        profit_amount = (price - cost) * qty
        kline = self.get_kline_tencent(code)
        
        # 获取并分析新闻
        news_list = get_stock_news(code)
        news_score = 0
        news_sentiment = '⚪ 无新闻'
        news_reasons = []
        
        if news_list:
            combined_news = ' '.join([n['text'] for n in news_list])
            news_result = self.news_analyzer.analyze(combined_news)
            news_score = news_result['score']
            news_sentiment = news_result['sentiment']
            news_reasons = news_result['reasons']
        
        # ========== v4.8 评分系统 ==========
        score = 50
        factors = []
        
        # 新闻评分
        if news_score != 0:
            factors.append(f"📰 新闻{news_sentiment} ({news_score:+d})")
            factors.extend(news_reasons[:2])
        
        # 多周期趋势分析 (30分)
        ma_score = 0
        ma_factors = []
        technical_strength = 0
        
        if kline:
            price = kline['current']
            if price > kline['ma5']:
                ma_score += 5
                ma_factors.append("📈 站上MA5")
                technical_strength += 1
            if kline['ma10'] and price > kline['ma10']:
                ma_score += 5
                ma_factors.append("📈 站上MA10")
                technical_strength += 1
            if kline['ma20'] and price > kline['ma20']:
                ma_score += 5
                ma_factors.append("📈 站上MA20")
                technical_strength += 1
            if kline['ma30'] and price > kline['ma30']:
                ma_score += 5
                ma_factors.append("📈 站上MA30")
                technical_strength += 1
            if kline['ma60'] and price > kline['ma60']:
                ma_score += 5
                ma_factors.append("📈 站上MA60")
                technical_strength += 1
            if kline.get('ma120') and price > kline['ma120']:
                ma_score += 5
                ma_factors.append("📈 站上MA120(长线)")
                technical_strength += 1
            if kline.get('ma250') and price > kline['ma250']:
                ma_score += 10
                ma_factors.append("🌟 站上年线(牛)")
                technical_strength += 1
            
            if kline['ma5'] > kline.get('ma10', 0) > kline.get('ma20', 0):
                ma_score += 10
                ma_factors.append("🌟 均线多头排列")
            
            if kline['trend'] == 'up':
                ma_score += 5
                ma_factors.append("📈 日线上升趋势")
            
            score += ma_score
            factors.extend(ma_factors[:3])
        
        # 资金流向 (20分)
        turnover = data['turnover']
        change_pct = data['change_pct']
        fund_signal = "⚪ 资金观望"
        has_distribution = False  # v4.8 标记主力出货
        
        if kline:
            price_position = (price - min(kline['closes'][-20:])) / (max(kline['closes'][-20:]) - min(kline['closes'][-20:]) + 0.001)
            
            if price_position < 0.3 and change_pct > 2 and turnover > 5:
                fund_score = 15
                fund_signal = "🚀 主力低位建仓"
            elif price_position < 0.3 and abs(change_pct) < 2 and turnover > 8:
                fund_score = 10
                fund_signal = "🟢 主力低位吸筹"
            elif price_position > 0.7 and change_pct > 3 and turnover > 10:
                fund_score = 12
                fund_signal = "🟢 主力拉升"
            elif price_position > 0.6 and change_pct < -3 and turnover > 8:
                fund_score = -15
                fund_signal = "🚨 主力高位出货"
                has_distribution = True  # v4.8 标记
            elif price_position > 0.7 and abs(change_pct) < 2 and turnover > 8:
                fund_score = -12
                fund_signal = "🔴 主力高位派发"
                has_distribution = True  # v4.8 标记
            elif change_pct < -5 and turnover > 10:
                fund_score = -15
                fund_signal = "🚨 恐慌资金出逃"
            elif change_pct > 5 and turnover > 10:
                fund_score = 15
                fund_signal = "🚀 资金抢筹"
            else:
                fund_score = 0
            
            score += fund_score
            factors.append(fund_signal)
        
        # 成交量趋势 (15分)
        if kline and 'volume_trend' in kline:
            if kline['volume_trend'] == 'up':
                score += 10
                factors.append(f"📈 成交量放大({kline['volume_ratio']:.1f}x)")
            elif kline['volume_trend'] == 'down':
                score -= 5
                factors.append("📉 成交量萎缩")
        
        # ========== v4.8 深套惩罚加强 ==========
        is_deep_loss = profit_pct < -10
        is_severe_loss = profit_pct < -15
        
        if is_severe_loss:
            score -= 25  # v4.7是-15，v4.8加强到-25
            factors.append(f"🚨 严重深套{profit_pct:.1f}% (额外-25分)")
        elif is_deep_loss:
            score -= 20  # v4.7是-15，v4.8加强到-20
            factors.append(f"🔴 深套{profit_pct:.1f}% (额外-20分)")
        elif profit_pct < -5:
            score -= 5
            factors.append(f"⚠️ 亏损{profit_pct:.1f}%")
        
        # 距离止损位
        stop_distance = (price - stop_loss) / stop_loss * 100
        if stop_distance < 2:
            score -= 20
            factors.append(f"🚨 接近止损位({stop_distance:.1f}%)")
        elif stop_distance < 5:
            score -= 10
            factors.append(f"⚠️ 靠近止损位")
        elif stop_distance > 10:
            score += 10
            factors.append("✅ 止损位安全")
        
        # 昨日形态
        candle_factor = ""
        if kline and kline.get('candle_pattern'):
            patterns = kline['candle_pattern']
            if '锤子线' in patterns and '阳线' in patterns:
                candle_factor = "🟢 昨日锤子线阳线"
            elif '十字星' in patterns:
                candle_factor = "🟡 昨日十字星"
            elif '流星线' in patterns:
                candle_factor = "🔴 昨日流星线"
            elif '阴线' in patterns and '阳线' not in patterns:
                candle_factor = "🔴 昨日阴线"
            elif '阳线' in patterns:
                candle_factor = "🟢 昨日阳线"
        
        # 成交量持续性
        volume_factor = ""
        volume_strong = False
        if kline and 'volume_sustain' in kline:
            vs = kline['volume_sustain']
            if vs >= 1.3:
                volume_factor = "🔥 成交量持续放大"
                volume_strong = True
            elif vs <= 0.6:
                volume_factor = "📉 成交量持续萎缩"
            elif vs <= 0.8:
                volume_factor = "📉 成交量萎缩"
        
        # 大盘情绪
        market = self.get_market_sentiment()
        market_factor = ""
        if market['factors']:
            market_factor = f"📊 {market['sentiment']}({market['change']:+.2f}%)"
        
        # 预测计算
        pred_score = score
        if '锤子线阳线' in candle_factor:
            pred_score += 8
        elif '十字星' in candle_factor:
            pred_score += 0
        elif '流星线' in candle_factor:
            pred_score -= 8
        elif '阴线' in candle_factor and '阳线' not in candle_factor:
            pred_score -= 5
        elif '阳线' in candle_factor:
            pred_score += 3
        
        if '持续放大' in volume_factor:
            pred_score += 5
        elif '持续萎缩' in volume_factor:
            pred_score -= 5
        
        if market['trend'] == 'up':
            pred_score += 5
        elif market['trend'] == 'down':
            pred_score -= 5
        
        # 识别超跌反弹
        is_oversold_rebound = False
        if news_score <= -30 and technical_strength >= 2 and volume_strong and profit_pct < 0:
            is_oversold_rebound = True
            factors.append("⚠️ 利空后技术反弹，此时割肉容易卖飞")
        
        # v4.8 主力出货+深套封顶
        has_severe_bad_news = news_score <= -30 or news_sentiment in ['🔴 严重利空', '🔴 强烈利空']
        
        # ========== v4.8 主力出货加重惩罚 ==========
        if has_distribution and is_deep_loss:
            # 主力出货且深套，预测封顶为震荡
            if pred_score >= 70:
                prediction = "🟡 震荡偏多 (主力出货，诱多风险)"
            elif pred_score >= 50:
                prediction = "🟠 震荡偏空 (主力出货，谨慎)"
            else:
                prediction = "🔴 看跌 (主力出货+深套，反弹有限)"
        elif is_oversold_rebound:
            prediction = "🟡 技术性反弹"
        elif has_severe_bad_news and pred_score >= 70:
            prediction = "🟡 震荡偏多"
        elif pred_score >= 70:
            prediction = "🟢 看涨"
        elif pred_score >= 50:
            prediction = "🟡 震荡偏多"
        elif pred_score >= 30:
            prediction = "🟠 震荡偏空"
        else:
            prediction = "🔴 看跌"
        
        # ========== v4.8 决策建议优化 ==========
        # 先计算关键价位（resistance/support），再计算反弹空间
        resistance, support = price * 1.03, price * 0.97
        if kline:
            mas = []
            for p in [('ma5',5), ('ma10',10), ('ma20',20), ('ma30',30), ('ma60',60), ('ma120',120), ('ma250',250)]:
                if kline.get(p[0]):
                    mas.append((kline[p[0]], p[1]))
            mas.sort(key=lambda x: x[0])
            for m, label in mas:
                if m > price:
                    resistance = m
                    break
            for m, label in reversed(mas):
                if m < price:
                    support = m
                    break
        
        # v4.8 计算反弹空间（必须在resistance/support计算之后）
        rebound_pct = self.calculate_rebound_space(price, resistance, support)
        rebound_advice = self.generate_rebound_advice(rebound_pct, is_deep_loss, has_distribution)
        
        # v4.8 生成警报
        stop_loss_alerts = self.check_stop_loss_alert(price, stop_loss, profit_pct, code, name)
        resistance_alert = self.check_resistance_alert(price, resistance, code, name)
        
        # 决策逻辑 - v4.8优化
        if price <= stop_loss:
            action = "🔴 立即止损"
            action_reason = f"已触发止损位 {stop_loss:.2f}，严格执行！"
        elif is_severe_loss and has_distribution:
            action = "🔴 减仓为主"
            action_reason = f"严重深套{profit_pct:.1f}%且主力出货，反弹即减仓，不等待"
        elif is_deep_loss and has_distribution:
            action = "🟠 择机减仓"
            action_reason = f"深套{profit_pct:.1f}%且主力出货，{rebound_advice}"
        elif is_deep_loss:
            action = "🟡 观望"
            action_reason = f"深套{profit_pct:.1f}%，禁止补仓！{rebound_advice}"
        elif score >= 70 and profit_pct > 0:
            action = "🟢 持有"
            action_reason = "强势，可持有或加仓"
        elif score >= 50:
            action = "🟡 观望"
            action_reason = "震荡，等待方向"
        elif score >= 30 and profit_pct < -5:
            if prediction in ["🟢 看涨", "🟡 震荡偏多", "🟡 技术性反弹"]:
                action = "🟡 观望"
                action_reason = f"短期有压力，但预测偏乐观，暂不减仓。{rebound_advice}"
            else:
                action = "🟠 减仓"
                action_reason = "弱势，降低仓位"
        else:
            if prediction in ["🟢 看涨", "🟡 震荡偏多", "🟡 技术性反弹"]:
                action = "🟡 观望"
                action_reason = f"score偏低，但预测偏乐观，等待反弹。{rebound_advice}"
            else:
                action = "🔴 卖出"
                action_reason = "趋势向下，离场观望"
        
        # 分时和明日预测
        intraday = self.predict_intraday(news_score, news_sentiment, kline, price, change_pct, profit_pct, is_oversold_rebound, has_severe_bad_news, technical_strength, volume_strong)
        next_day = self.predict_next_day(prediction, intraday, kline, price, cost, resistance, support)
        
        # 时间维度建议
        timed_advice = self.generate_timed_advice(action, action_reason, intraday, next_day, profit_pct, stop_loss, price, rebound_advice)
        
        return {
            'name': name, 'code': code, 'price': price,
            'profit_pct': profit_pct, 'profit_amount': profit_amount,
            'score': score, 'factors': factors, 'prediction': prediction,
            'action': action, 'action_reason': action_reason,
            'timed_advice': timed_advice,
            'volume': data['volume'], 'turnover': turnover, 'change_pct': change_pct,
            'kline': kline,
            'news_sentiment': news_sentiment,
            'news_score': news_score,
            'news_list': news_list,
            'candle_factor': candle_factor,
            'volume_factor': volume_factor,
            'market_factor': market_factor,
            'intraday': intraday,
            'next_day': next_day,
            # v4.8 新增
            'resistance': resistance,
            'support': support,
            'rebound_pct': rebound_pct,
            'rebound_advice': rebound_advice,
            'stop_loss_alerts': stop_loss_alerts,
            'resistance_alert': resistance_alert,
            'is_deep_loss': is_deep_loss,
            'has_distribution': has_distribution,
            'stop_distance': stop_distance
        }
    
    def predict_intraday(self, news_score, news_sentiment, kline, price, change_pct, profit_pct, is_oversold_rebound, has_severe_bad_news, technical_strength, volume_strong):
        """分时预测引擎"""
        if has_severe_bad_news and change_pct < -2:
            morning = "🔴 恐慌低开"
        elif has_severe_bad_news:
            morning = "🟡 低开或平开"
        elif news_score >= 20:
            morning = "🟢 高开"
        elif news_score >= 10:
            morning = "🟡 平开或小高"
        else:
            morning = "⚪ 平开震荡"
        
        if is_oversold_rebound:
            if volume_strong:
                pattern = "📉→📈 先抑后扬（利空出尽，资金抄底）"
                noon = "🟢 震荡反弹"
                afternoon = "🟡 反弹后回落或收高"
            else:
                pattern = "📉→⚪ 弱反弹后横盘"
                noon = "🟡 低位震荡"
                afternoon = "⚪ 收盘平平"
        elif has_severe_bad_news and technical_strength >= 2 and volume_strong:
            pattern = "📉→📈 技术性反弹"
            noon = "🟢 资金抄底反弹"
            afternoon = "🟡 反弹力度决定收盘"
        elif has_severe_bad_news and not volume_strong:
            pattern = "📉→📉 单边承压"
            noon = "🔴 震荡走低"
            afternoon = "🔴 尾盘弱势"
        elif news_score >= 20 and volume_strong:
            pattern = "📈→📈 强势上涨"
            noon = "🟢 强势拉升"
            afternoon = "🟢 高位收盘"
        elif news_score >= 10 and change_pct > 0:
            pattern = "📈→⚪ 冲高回落"
            noon = "🟢 冲高"
            afternoon = "🟡 小幅回落"
        elif change_pct > 3 and not volume_strong:
            pattern = "📈→📉 冲高回落（量能不足）"
            noon = "🟢 冲高"
            afternoon = "🔴 回落"
        elif change_pct < -3 and volume_strong:
            pattern = "📉→📈 V型反转"
            noon = "🟡 探底回升"
            afternoon = "🟢 收复失地"
        else:
            pattern = "⚪ 横盘震荡"
            noon = "🟡 窄幅波动"
            afternoon = "⚪ 收盘附近"
        
        if is_oversold_rebound and volume_strong:
            strength = "🔥 强反弹（可能3-6%）"
        elif is_oversold_rebound:
            strength = "🟢 弱反弹（1-3%）"
        elif volume_strong and news_score > 0:
            strength = "🔥 强势上涨"
        elif volume_strong and news_score <= 0:
            strength = "🟡 有抵抗但空间有限"
        else:
            strength = "⚪ 震荡为主"
        
        return {
            'morning': morning,
            'noon': noon,
            'afternoon': afternoon,
            'pattern': pattern,
            'strength': strength
        }
    
    def predict_next_day(self, prediction, intraday, kline, price, cost, resistance, support):
        """明日预测引擎"""
        if intraday['pattern'].startswith("📉→📈"):
            next_open = "🟡 平开或小幅高开"
            next_noon = "🟡 冲高后承压"
            next_trend = "🟡 震荡偏空"
            reason = "今日反弹后，明日获利盘和解套盘可能抛压"
        elif intraday['pattern'].startswith("📈→📉"):
            next_open = "🔴 低开"
            next_noon = "🔴 惯性下探"
            next_trend = "🔴 看跌"
            reason = "今日冲高回落，明日惯性下探"
        elif intraday['pattern'].startswith("📈→📈"):
            next_open = "🟢 高开"
            next_noon = "🟢 惯性上冲"
            next_trend = "🟢 看涨"
            reason = "强势延续"
        elif prediction == "🔴 看跌":
            next_open = "🔴 低开"
            next_noon = "🔴 弱势震荡"
            next_trend = "🔴 看跌"
            reason = "趋势未改"
        elif prediction == "🟢 看涨":
            next_open = "🟢 高开"
            next_noon = "🟢 继续走强"
            next_trend = "🟢 看涨"
            reason = "趋势延续"
        else:
            next_open = "⚪ 平开"
            next_noon = "⚪ 窄幅震荡"
            next_trend = prediction
            reason = "震荡延续"
        
        return {
            'open': next_open,
            'noon': next_noon,
            'trend': next_trend,
            'reason': reason,
            'resistance': resistance,
            'support': support
        }
    
    def generate_timed_advice(self, action, base_reason, intraday, next_day, profit_pct, stop_loss, price, rebound_advice):
        """生成带时间维度的操作建议"""
        if price <= stop_loss:
            return f"🔴 立即卖出（已触发止损位 {stop_loss}）"
        
        timed = base_reason
        
        if "📉→📈" in intraday['pattern'] and profit_pct < 0:
            timed = f"早盘不卖，等午后反弹高点再考虑减仓。{rebound_advice}"
        elif "📈→📉" in intraday['pattern'] and profit_pct > 0:
            timed = f"冲高时减仓，不要贪。{rebound_advice}"
        elif "📈→📈" in intraday['pattern']:
            timed = f"全天强势，持有为主。{rebound_advice}"
        elif "📉→📉" in intraday['pattern']:
            timed = f"弱势全天，但止损位{stop_loss}未触发则暂观望。{rebound_advice}"
        
        return timed
    
    def generate_report(self, holdings):
        """生成v4.8报告"""
        print(f"\n{'='*70}")
        print(f"【完美交易系统 v4.8】智能止损优化版 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*70}")
        
        market = self.get_market_sentiment()
        if market:
            print(f"\n📊 大盘情绪: {market['sentiment']} ({market['change']:+.2f}%)")
        
        results = []
        for code, name, cost, qty, stop_loss, target in holdings:
            result = self.analyze_stock(code, name, cost, qty, stop_loss, target)
            if result:
                results.append(result)
        
        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n📊 【持仓评分排名】")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']}({r['code']}) - {r['score']}分 - {r['prediction']}")
        
        # v4.8 新增：紧急警报区
        all_alerts = []
        for r in results:
            all_alerts.extend(r.get('stop_loss_alerts', []))
            if r.get('resistance_alert'):
                all_alerts.append(r['resistance_alert'])
        
        if all_alerts:
            print(f"\n{'='*70}")
            print(f"🚨【紧急警报】")
            print(f"{'='*70}")
            for alert in all_alerts:
                print(f"   {alert}")
        
        print(f"\n{'='*70}")
        print(f"【个股详细分析】")
        print(f"{'='*70}")
        
        total_cost = sum(h[2] * h[3] for h in holdings)
        total_value = sum(r['price'] * next(h[3] for h in holdings if h[0] == r['code']) for r in results)
        
        for r in results:
            print(f"\n【{r['name']} ({r['code']})】")
            print(f"   价格: {r['price']}元 (今日{r['change_pct']:+.2f}%)")
            print(f"   盈亏: {r['profit_amount']:,.0f}元 ({r['profit_pct']:+.2f}%)")
            
            # v4.8 新增：深套和主力信号标识
            if r.get('is_deep_loss'):
                print(f"   ⚠️ 状态: 🔴 深套股（亏损>10%）")
            if r.get('has_distribution'):
                print(f"   ⚠️ 状态: 🔴 主力出货中")
            
            print(f"\n   💹 交易数据:")
            print(f"      成交量: {r['volume']:,.0f}手 ({r['volume']/10000:.2f}万手)")
            print(f"      成交额: {r['turnover']:.2f}亿元")
            
            if r.get('kline') and r['kline'].get('volume_ratio'):
                ratio = r['kline']['volume_ratio']
                trend = r['kline']['volume_trend']
                if trend == 'up':
                    print(f"      趋势: 📈 放量 {ratio:.1f}x")
                    if ratio > 1.5:
                        print(f"      信号: 🔥 巨量突破")
                    elif ratio > 1.2:
                        print(f"      信号: 🟢 温和放量")
                elif trend == 'down':
                    print(f"      趋势: 📉 缩量 {ratio:.1f}x")
                    print(f"      信号: ⚪ 成交清淡")
                else:
                    print(f"      趋势: ➡️ 持平 {ratio:.1f}x")
            
            if 'kline' in r and r['kline']:
                k = r['kline']
                price = r['price']
                print(f"\n   📊 多周期均线:")
                print(f"      短期: MA5={k['ma5']:.2f}{'✅' if price > k['ma5'] else '❌'} MA10={k['ma10']:.2f}{'✅' if price > k['ma10'] else '❌'} MA20={k['ma20']:.2f}{'✅' if price > k['ma20'] else '❌'}")
                print(f"      中期: MA30={k['ma30']:.2f}{'✅' if price > k['ma30'] else '❌'} MA60={k['ma60']:.2f}{'✅' if price > k['ma60'] else '❌'}")
                if k.get('ma120'): print(f"      长期: MA120={k['ma120']:.2f}{'✅' if price > k['ma120'] else '❌'}")
                if k.get('ma250'): print(f"      年线: MA250={k['ma250']:.2f}{'✅' if price > k['ma250'] else '❌'}")
            
            # v4.8 新增：压力位/支撑位/反弹空间
            if r.get('resistance') and r.get('support'):
                print(f"\n   🎯 关键价位:")
                print(f"      压力位: {r['resistance']:.2f}元")
                print(f"      支撑位: {r['support']:.2f}元")
                print(f"      反弹空间: {r['rebound_pct']:.2f}%")
                print(f"      反弹建议: {r['rebound_advice']}")
            
            if r.get('news_list'):
                print(f"\n   📰 新闻分析:")
                print(f"      情绪: {r['news_sentiment']} (评分: {r['news_score']:+d})")
                for news in r['news_list'][-2:]:
                    print(f"      [{news['time']}] {news['text'][:30]}...")
            
            print(f"\n   📊 综合评分: {r['score']}/100")
            print(f"   🔮 1-2日预测: {r['prediction']}")
            
            if r.get('intraday'):
                intra = r['intraday']
                print(f"\n   ⏰ 【今日分时预测】")
                print(f"      早盘: {intra['morning']}")
                print(f"      盘中: {intra['noon']}")
                print(f"      尾盘: {intra['afternoon']}")
                print(f"      形态: {intra['pattern']}")
                print(f"      强度: {intra['strength']}")
            
            if r.get('next_day'):
                nd = r['next_day']
                print(f"\n   📅 【明日预测】")
                print(f"      开盘: {nd['open']}")
                print(f"      盘中: {nd['noon']}")
                print(f"      趋势: {nd['trend']}")
                print(f"      压力: {nd['resistance']:.2f}  支撑: {nd['support']:.2f}")
                print(f"      理由: {nd['reason']}")
            
            print(f"\n   📋 关键因素:")
            if r.get('candle_factor'):
                print(f"      {r['candle_factor']}")
            if r.get('volume_factor'):
                print(f"      {r['volume_factor']}")
            if r.get('market_factor'):
                print(f"      {r['market_factor']}")
            for f in r['factors'][:5]:
                print(f"      {f}")
            
            print(f"\n   💡 操作建议: {r['action']}")
            print(f"      理由: {r['action_reason']}")
            if r.get('timed_advice') and r['timed_advice'] != r['action_reason']:
                print(f"      ⏰ 时间策略: {r['timed_advice']}")
            
            # v4.8 新增：止损距离提醒
            if r.get('stop_distance') and r['stop_distance'] > 0:
                print(f"      🛡️ 止损距离: {r['stop_distance']:.1f}%")
        
        print(f"\n{'='*70}")
        print(f"【账户汇总】")
        print(f"   总成本: {total_cost:,.0f}元")
        print(f"   总市值: {total_value:,.0f}元")
        total_profit_pct = ((total_value - total_cost) / total_cost) * 100
        print(f"   总盈亏: {total_value - total_cost:,.0f}元 ({total_profit_pct:+.2f}%)")
        print(f"\n   整体评分: {sum(r['score'] for r in results) / len(results):.0f}/100")
        
        strong = [r for r in results if r['score'] >= 70]
        weak = [r for r in results if r['score'] < 40]
        
        print(f"\n{'='*70}")
        print(f"【今日策略】")
        if strong:
            print(f"   🟢 强势股 ({len(strong)}只): " + ", ".join([r['name'] for r in strong[:3]]))
        if weak:
            print(f"   🔴 弱势股 ({len(weak)}只): " + ", ".join([r['name'] for r in weak[:3]]))
        if not strong and not weak:
            print(f"   🟡 整体震荡，观望为主")
        
        # v4.8 新增：总结提醒
        deep_loss_count = sum(1 for r in results if r.get('is_deep_loss'))
        if deep_loss_count > 0:
            print(f"\n   ⚠️ 提醒: 有{deep_loss_count}只深套股(>10%)，禁止补仓，严格按策略执行！")
        
        print(f"\n{'='*70}")


# 新闻数据
add_stock_news('600406', '国电南瑞中标国家电网智能电网项目10亿元')
add_stock_news('600406', '国电南瑞拟回购5-10亿元股份')
add_stock_news('600150', '中国船舶签订10艘VLCC建造合同金额80-90亿元')
add_stock_news('600150', '中国船舶前三季度净利润同比增长115%')
add_stock_news('002050', '三花智控大股东拟减持不超过2%股份')
add_stock_news('002050', '三花智控2025年净利润增长31%')
add_stock_news('002230', '科大讯飞与Viettel签署战略合作协议')
add_stock_news('002230', '科大讯飞发布AstronClaw升级发布会')
add_stock_news('301468', '博盈特焊越南基地签订土地租赁合同')

# 持仓配置
holdings = [
    ('600406', '国电南瑞', 25.124, 1500, 24.12, 27.13),
    ('600150', '中国船舶', 32.090, 200, 30.17, 34.02),
    ('000998', '隆平高科', 9.792, 500, 9.20, 10.38),
    ('002050', '三花智控', 53.065, 400, 43.0, 44.34),
    ('002230', '科大讯飞', 52.208, 500, 45.85, 51.58),
    ('301468', '博盈特焊', 53.451, 100, 51.04, 58.03),
]

if __name__ == '__main__':
    system = PerfectTradingSystemV48()
    system.generate_report(holdings)
