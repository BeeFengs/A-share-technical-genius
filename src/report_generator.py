"""
报告生成模块 - 使用 Google Gemini API 生成技术分析报告
"""
import os
from typing import Dict
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # 配置更高级的思维模型
        self.model = genai.GenerativeModel(
            'gemini-pro',
            generation_config={
                'temperature': 0.9,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 8192,
            }
        )

    def generate_report(self, stock_name: str, analysis: dict, df) -> Dict[str, str]:
        """
        生成技术分析报告
        
        参数:
            stock_name (str): 股票名称
            analysis (dict): 技术指标分析结果
            df: 原始数据DataFrame
            
        返回:
            Dict[str, str]: 包含思维过程和分析结果的字典
        """
        # 准备提示信息
        latest_price = df.iloc[-1]['close']
        price_change = df.iloc[-1]['pct_change']
        vol_change = ((df.iloc[-1]['vol'] - df.iloc[-2]['vol']) / df.iloc[-2]['vol']) * 100
        
        prompt = f"""
作为一名专业的股票技术分析师，请基于以下技术指标数据为{stock_name}生成一份深度技术分析报告。

# 市场数据
## 基础行情
- 最新收盘价：{latest_price:.2f}
- 涨跌幅：{price_change:.2f}%
- 成交量变化：{vol_change:.2f}%

## 技术指标
### MACD指标
- DIF：{analysis['MACD']['DIF']:.2f}
- DEA：{analysis['MACD']['DEA']:.2f}
- MACD：{analysis['MACD']['MACD']:.2f}
- 信号：{analysis['MACD']['signal']}

### KDJ指标
- K值：{analysis['KDJ']['K']:.2f}
- D值：{analysis['KDJ']['D']:.2f}
- J值：{analysis['KDJ']['J']:.2f}
- 信号：{analysis['KDJ']['signal']}

### RSI指标
- RSI6：{analysis['RSI']['RSI6']:.2f}
- RSI12：{analysis['RSI']['RSI12']:.2f}
- RSI24：{analysis['RSI']['RSI24']:.2f}
- 信号：{analysis['RSI']['signal']}

### 布林带指标
- 上轨：{analysis['BOLL']['UPPER']:.2f}
- 中轨：{analysis['BOLL']['MID']:.2f}
- 下轨：{analysis['BOLL']['LOWER']:.2f}
- 信号：{analysis['BOLL']['signal']}

请按照以下思维框架进行分析：

1. 技术形态分析
   - 价格形态特征
   - 成交量配合情况
   - 关键支撑压力位

2. 趋势研判
   - 主趋势判断
   - 次级调整特征
   - 趋势持续性分析

3. 技术指标研判
   - MACD指标信号研判
   - KDJ指标超买超卖分析
   - RSI指标背离分析
   - 布林带位置研判

4. 综合研判
   - 多空力量对比
   - 市场情绪分析
   - 主力资金动向判断

5. 操作建议
   - 短期操作策略
   - 中期布局建议
   - 风险控制要点

注意事项：
- 分析需要客观、专业、严谨
- 必须有具体数据支撑
- 需要明确指出各个指标的信号含义
- 对于重要结论要给出具体依据
"""

        try:
            # 调用API生成报告
            response = self.model.generate_content(prompt)
            
            # 保存报告
            report_dir = self._create_report_directory(stock_name)
            self._save_report(response.text, report_dir)
            
            return {
                "thoughts": "基于多维度技术指标的综合分析完成",
                "analysis": response.text
            }
            
        except Exception as e:
            error_msg = f"生成报告时发生错误: {str(e)}"
            return {
                "thoughts": "分析过程出错",
                "analysis": error_msg
            }

    def _create_report_directory(self, stock_name: str) -> str:
        """创建报告保存目录"""
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = os.path.join("analysis_reports", f"{stock_name}_{current_time}")
        os.makedirs(report_dir, exist_ok=True)
        return report_dir

    def _save_report(self, report: str, report_dir: str):
        """保存报告为Markdown格式"""
        filepath = os.path.join(report_dir, "technical_analysis.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 技术分析报告\n\n")
            f.write(report)
        print(f"\n详细分析报告已保存到: {filepath}") 