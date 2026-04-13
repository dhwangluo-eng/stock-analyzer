#!/usr/bin/env python3
"""
完美交易系统 v4.4 - AI预测版
=====================================
维度：历史趋势 + 技术指标 + 资金流向 + 新闻情绪 + 1-2日走势预测
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
        
        if score >= 20:
            sentiment = '🟢 强烈利好'
        elif score >= 10:
            sentiment = '🟢 利好'
        elif score <= -20:
            sentiment = '🔴 强烈利空'
        elif score <= -10:
            sentiment = '🔴 利空'
        else:
            sentiment = '⚪ 中性'
        
        return {'score': score, 'sentiment': sentiment, 'reasons': reasons[:3]}


class PerfectTradingSystemV4:
    """完美交易系统 v4.4 - 预测版"""
    
    def __init__(self, db_path='/Users/sunjian/.openclaw/workspace/trading_records.db'):
        self.db_path = db_path
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
    
    def get_stock_news(self, code):
        """获取股票相关新闻和公告"""
        try:
            # 使用新浪财经新闻接口
            full_code = f"sh{code}" if code.startswith('6') else f"sz{code}"
            url = f"https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid={code}"
            
            # 简化的新闻分析 - 基于关键词匹配
            news_items = []
            
            # 正面新闻关键词检测
            positive_news = []
            negative_news = []
            
            # 这里简化处理，实际应该抓取网页内容
            # 返回模拟数据用于演示
            return {
                'success': True,
                'bulletins': [],
                'sentiment': 'neutral',
                'keywords': []
            }
        except:
            return {'success': False, 'error': '无法获取新闻'}
    
    def get_kline_tencent(self, code, period='day', days=250):
        """获取多周期K线数据（支持MA120/250）"""
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
            
            closes = [float(item[2]) for item in lines]
            volumes = [float(item[5]) for item in lines] if len(lines[0]) > 5 else []
            
            def ma(data, period):
                if len(data) < period:
                    return None
                return sum(data[-period:]) / period
            
            # 计算各周期均线
            result = {
                'closes': closes,
                'current': closes[-1],
                'ma5': ma(closes, 5),
                'ma10': ma(closes, 10),
                'ma20': ma(closes, 20),
                'ma30': ma(closes, 30),
                'ma60': ma(closes, 60),
                'ma120': ma(closes, 120),
                'ma250': ma(closes, 250),
                'trend': 'up' if closes[-1] > closes[0] else 'down',
                'volatility': (max(closes) - min(closes)) / closes[0] * 100
            }
            
            # 添加成交量分析
            if volumes and len(volumes) >= 5:
                recent_vol = sum(volumes[-5:]) / 5
                prev_vol = sum(volumes[-10:-5]) / 5 if len(volumes) >= 10 else recent_vol
                result['volume_trend'] = 'up' if recent_vol > prev_vol * 1.2 else 'down' if recent_vol < prev_vol * 0.8 else 'flat'
                result['volume_ratio'] = recent_vol / prev_vol if prev_vol > 0 else 1.0
            
            return result
        except:
            return None
    
    def __init__(self):
        self.news_analyzer = NewsAnalyzer()
    
    def analyze_stock(self, code, name, cost, qty, stop_loss, target):
        """综合分析单只股票"""
        data = self.get_stock_data(code)
        if not data['success']:
            return None
        
        price = data['price']
        profit_pct = ((price - cost) / cost) * 100
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
        
        # 评分系统 (满分100)
        score = 50  # 基础分
        score += news_score  # 加入新闻评分
        factors = []
        
        # 添加新闻因素
        if news_score != 0:
            factors.append(f"📰 新闻{news_sentiment} ({news_score:+d})")
            factors.extend(news_reasons[:2])
        
        # 1. 多周期趋势分析 (30分)
        ma_score = 0
        ma_factors = []
        
        if kline:
            price = kline['current']
            # 短期趋势
            if price > kline['ma5']:
                ma_score += 5
                ma_factors.append("📈 站上MA5")
            if kline['ma10'] and price > kline['ma10']:
                ma_score += 5
                ma_factors.append("📈 站上MA10")
            if kline['ma20'] and price > kline['ma20']:
                ma_score += 5
                ma_factors.append("📈 站上MA20")
            
            # 中长期趋势
            if kline['ma30'] and price > kline['ma30']:
                ma_score += 5
                ma_factors.append("📈 站上MA30")
            if kline['ma60'] and price > kline['ma60']:
                ma_score += 5
                ma_factors.append("📈 站上MA60")
            if kline.get('ma120') and price > kline['ma120']:
                ma_score += 5
                ma_factors.append("📈 站上MA120(长线)")
            if kline.get('ma250') and price > kline['ma250']:
                ma_score += 10
                ma_factors.append("🌟 站上年线(牛)")
            
            # 均线多头排列
            if kline['ma5'] > kline.get('ma10', 0) > kline.get('ma20', 0):
                ma_score += 10
                ma_factors.append("🌟 均线多头排列")
            
            # 整体趋势
            if kline['trend'] == 'up':
                ma_score += 5
                ma_factors.append("📈 日线上升趋势")
            
            score += ma_score
            factors.extend(ma_factors[:3])  # 只显示前3个
        
        # 2. 资金流向 (20分)
        turnover = data['turnover']
        change_pct = data['change_pct']
        if turnover > 10 and change_pct > 0:
            score += 15
            factors.append("💰 大资金流入")
        elif turnover > 5 and change_pct > 2:
            score += 10
            factors.append("🟢 资金流入")
        elif turnover > 10 and change_pct < 0:
            score -= 15
            factors.append("🔴 资金出逃")
        elif change_pct < -3:
            score -= 10
            factors.append("⚠️ 大跌")
        
        # 3. 成交量趋势 (15分)
        if kline and 'volume_trend' in kline:
            if kline['volume_trend'] == 'up':
                score += 10
                factors.append(f"📈 成交量放大({kline['volume_ratio']:.1f}x)")
            elif kline['volume_trend'] == 'down':
                score -= 5
                factors.append("📉 成交量萎缩")
        
        # 4. 主力资金精细分析 (15分)
        fund_score = 0
        fund_signal = None
        
        if kline:
            price_position = (price - min(kline['closes'][-20:])) / (max(kline['closes'][-20:]) - min(kline['closes'][-20:]) + 0.001)
            
            # 低位放量上涨 = 主力建仓
            if price_position < 0.3 and change_pct > 2 and turnover > 5:
                fund_score += 15
                fund_signal = "🚀 主力低位建仓"
            # 低位放量滞涨 = 主力吸筹
            elif price_position < 0.3 and abs(change_pct) < 2 and turnover > 8:
                fund_score += 10
                fund_signal = "🟢 主力低位吸筹"
            # 高位放量上涨 = 主力拉升
            elif price_position > 0.7 and change_pct > 3 and turnover > 10:
                fund_score += 12
                fund_signal = "🟢 主力拉升"
            # 高位放量下跌 = 主力出货
            elif price_position > 0.6 and change_pct < -3 and turnover > 8:
                fund_score -= 15
                fund_signal = "🚨 主力高位出货"
            # 高位放量滞涨 = 主力派发
            elif price_position > 0.7 and abs(change_pct) < 2 and turnover > 8:
                fund_score -= 12
                fund_signal = "🔴 主力高位派发"
            # 大跌放量 = 恐慌出逃
            elif change_pct < -5 and turnover > 10:
                fund_score -= 15
                fund_signal = "🚨 恐慌资金出逃"
            # 大涨放量 = 资金抢筹
            elif change_pct > 5 and turnover > 10:
                fund_score += 15
                fund_signal = "🚀 资金抢筹"
            else:
                fund_signal = "⚪ 资金观望"
        
        if fund_signal:
            factors.append(fund_signal)
        score += fund_score
        
        # 5. 深套惩罚
        if profit_pct < -10:
            score -= 15
            factors.append(f"🚨 深套{profit_pct:.1f}%")
        elif profit_pct < -5:
            score -= 5
            factors.append(f"⚠️ 亏损{profit_pct:.1f}%")
        
        # 4. 距离止损位 (20分)
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
        
        # 5. 短期预测 (20分)
        prediction = "观望"
        if score >= 70:
            prediction = "🟢 看涨"
        elif score >= 50:
            prediction = "🟡 震荡偏多"
        elif score >= 30:
            prediction = "🟠 震荡偏空"
        else:
            prediction = "🔴 看跌"
        
        # 决策建议
        if price <= stop_loss:
            action = "🔴 止损卖出"
            action_reason = "触发设定止损位"
        elif score >= 70 and profit_pct > 0:
            action = "🟢 持有"
            action_reason = "强势，可持有或加仓"
        elif score >= 50:
            action = "🟡 观望"
            action_reason = "震荡，等待方向"
        elif score >= 30 and profit_pct < -5:
            action = "🟠 减仓"
            action_reason = "弱势，降低仓位"
        else:
            action = "🔴 卖出"
            action_reason = "趋势向下，离场观望"
        
        return {
            'name': name, 'code': code, 'price': price,
            'profit_pct': profit_pct, 'profit_amount': (price - cost) * qty,
            'score': score, 'factors': factors, 'prediction': prediction,
            'action': action, 'action_reason': action_reason,
            'volume': data['volume'], 'turnover': turnover, 'change_pct': change_pct,
            'kline': kline,  # 保存K线数据
            'news_sentiment': news_sentiment,  # 新闻情绪
            'news_score': news_score,  # 新闻评分
            'news_list': news_list  # 新闻列表
        }
    
    def generate_report(self, holdings):
        """生成报告"""
        print(f"\n{'='*70}")
        print(f"【完美交易系统 v4.6】AI预测报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*70}")
        
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
        
        print(f"\n{'='*70}")
        print(f"【个股详细分析】")
        print(f"{'='*70}")
        
        total_cost = sum(h[2] * h[3] for h in holdings)
        total_value = sum(r['price'] * next(h[3] for h in holdings if h[0] == r['code']) for r in results)
        
        for r in results:
            print(f"\n【{r['name']} ({r['code']})】")
            print(f"   价格: {r['price']}元 (今日{r['change_pct']:+.2f}%)")
            print(f"   盈亏: {r['profit_amount']:,.0f}元 ({r['profit_pct']:+.2f}%)")
            print(f"\n   💹 交易数据:")
            print(f"      成交量: {r['volume']:,.0f}手 ({r['volume']/10000:.2f}万手)")
            print(f"      成交额: {r['turnover']:.2f}亿元")
            
            # 成交量趋势分析显示
            if r.get('kline') and r['kline'].get('volume_ratio'):
                ratio = r['kline']['volume_ratio']
                trend = r['kline']['volume_trend']
                if trend == 'up':
                    print(f"      趋势: 📈 放量 {ratio:.1f}x (近5日 vs 前5日)")
                    if ratio > 1.5:
                        print(f"      信号: 🔥 巨量突破")
                    elif ratio > 1.2:
                        print(f"      信号: 🟢 温和放量")
                elif trend == 'down':
                    print(f"      趋势: 📉 缩量 {ratio:.1f}x")
                    print(f"      信号: ⚪ 成交清淡")
                else:
                    print(f"      趋势: ➡️ 持平 {ratio:.1f}x")
            else:
                print(f"      趋势: ⚪ 数据不足")
                ratio = r['kline']['volume_ratio']
                trend = r['kline']['volume_trend']
                if trend == 'up':
                    print(f"      趋势: 📈 放量 {ratio:.1f}x (近5日 vs 前5日)")
                    if ratio > 1.5:
                        print(f"      信号: 🔥 巨量突破")
                    elif ratio > 1.2:
                        print(f"      信号: 🟢 温和放量")
                elif trend == 'down':
                    print(f"      趋势: 📉 缩量 {ratio:.1f}x")
                    print(f"      信号: ⚪ 成交清淡")
                else:
                    print(f"      趋势: ➡️ 持平 {ratio:.1f}x")
            
            # 多周期MA显示
            if 'kline' in r and r['kline']:
                k = r['kline']
                price = r['price']
                print(f"\n   📊 多周期均线:")
                print(f"      短期: MA5={k['ma5']:.2f}{'✅' if price > k['ma5'] else '❌'} MA10={k['ma10']:.2f}{'✅' if price > k['ma10'] else '❌'} MA20={k['ma20']:.2f}{'✅' if price > k['ma20'] else '❌'}")
                print(f"      中期: MA30={k['ma30']:.2f}{'✅' if price > k['ma30'] else '❌'} MA60={k['ma60']:.2f}{'✅' if price > k['ma60'] else '❌'}")
                if k.get('ma120'): print(f"      长期: MA120={k['ma120']:.2f}{'✅' if price > k['ma120'] else '❌'}")
                if k.get('ma250'): print(f"      年线: MA250={k['ma250']:.2f}{'✅' if price > k['ma250'] else '❌'}")
            
            # 新闻分析显示
            if r.get('news_list'):
                print(f"\n   📰 新闻分析:")
                print(f"      情绪: {r['news_sentiment']} (评分: {r['news_score']:+d})")
                for news in r['news_list'][-2:]:  # 显示最近2条
                    print(f"      [{news['time']}] {news['text'][:30]}...")
            
            print(f"\n   📊 综合评分: {r['score']}/100")
            print(f"   🔮 1-2日预测: {r['prediction']}")
            print(f"\n   📋 关键因素:")
            for f in r['factors'][:5]:
                print(f"      {f}")
            print(f"\n   💡 操作建议: {r['action']}")
            print(f"      理由: {r['action_reason']}")
        
        print(f"\n{'='*70}")
        print(f"【账户汇总】")
        print(f"   总成本: {total_cost:,.0f}元")
        print(f"   总市值: {total_value:,.0f}元")
        total_profit_pct = ((total_value - total_cost) / total_cost) * 100
        print(f"   总盈亏: {total_value - total_cost:,.0f}元 ({total_profit_pct:+.2f}%)")
        print(f"\n   整体评分: {sum(r['score'] for r in results) / len(results):.0f}/100")
        
        # 今日策略
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
        
        print(f"\n{'='*70}")

# 添加今日新闻（演示）
add_stock_news('600406', '国电南瑞中标国家电网智能电网项目10亿元')
add_stock_news('600406', '国电南瑞拟回购5-10亿元股份')
add_stock_news('600150', '中国船舶签订10艘VLCC建造合同金额80-90亿元')
add_stock_news('600150', '中国船舶前三季度净利润同比增长115%')
add_stock_news('002050', '三花智控大股东拟减持不超过2%股份')
add_stock_news('002050', '三花智控2025年净利润增长31%')
add_stock_news('002230', '科大讯飞与Viettel签署战略合作协议')
add_stock_news('002230', '科大讯飞发布AstronClaw升级发布会')
add_stock_news('301468', '博盈特焊越南基地签订土地租赁合同')
add_stock_news('600151', '航天机电2025年营收下降32%净利润亏损4.45亿元')

# 持仓配置
holdings = [
    ('600406', '国电南瑞', 25.124, 1500, 24.12, 27.13),
    ('600150', '中国船舶', 32.090, 200, 30.17, 34.02),
    ('000998', '隆平高科', 9.792, 500, 9.20, 10.38),
    ('600151', '航天机电', 14.153, 400, 13.30, 15.00),
    ('002050', '三花智控', 53.065, 400, 43.0, 44.34),
    ('002230', '科大讯飞', 52.208, 500, 45.85, 51.58),
    ('301468', '博盈特焊', 53.451, 100, 51.04, 58.03),
]

if __name__ == '__main__':
    system = PerfectTradingSystemV4()
    system.generate_report(holdings)
