"""
报告生成模块 - 使用 Google Gemini API 生成技术分析报告
"""
import os
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from src.prompts.technical_analysis import get_technical_analysis_prompt
from src.prompts.indicators import (
    get_macd_analysis_prompt,
    get_kdj_analysis_prompt,
    get_rsi_analysis_prompt,
    get_boll_analysis_prompt
)

class ReportGenerator:
    def __init__(self, output_dir: str = "analysis_reports"):
        """
        初始化报告生成器
        
        参数:
            output_dir (str): 报告输出目录
        """
        self.output_dir = output_dir
        self.current_report_dir = None  # 添加当前报告目录的引用
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
        
        # 使用prompt模板生成提示信息
        prompt = get_technical_analysis_prompt(
            stock_name=stock_name,
            latest_price=latest_price,
            price_change=price_change,
            vol_change=vol_change,
            analysis=analysis
        )

        try:
            # 调用API生成报告
            response = self.model.generate_content(prompt)
            
            # 创建并保存报告目录的引用
            self.current_report_dir = self._create_report_directory(stock_name)
            self._save_report(response.text, self.current_report_dir)
            
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
        report_dir = os.path.join(self.output_dir, f"{stock_name}_{current_time}")
        os.makedirs(report_dir, exist_ok=True)
        return report_dir

    def _save_report(self, report: str, report_dir: str):
        """保存报告为Markdown格式"""
        filepath = os.path.join(report_dir, "technical_analysis.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 技术分析报告\n\n")
            f.write(report)
        print(f"\n详细分析报告已保存到: {filepath}")

    def generate_indicator_report(self, stock_name: str, indicator_name: str, 
                                latest_price: float, price_change: float, 
                                vol_change: float, analysis: Dict[str, Any]) -> str:
        """
        生成单个技术指标的分析报告
        
        参数:
            stock_name (str): 股票名称
            indicator_name (str): 技术指标名称
            latest_price (float): 最新收盘价
            price_change (float): 涨跌幅
            vol_change (float): 成交量变化
            analysis (dict): 技术指标分析结果
            
        返回:
            str: 生成的报告内容
        """
        indicator_prompts = {
            'MACD': lambda: get_macd_analysis_prompt(
                dif=analysis['MACD']['DIF'],
                dea=analysis['MACD']['DEA'],
                macd=analysis['MACD']['MACD'],
                long_term_trend=analysis['MACD']['long_term_trend'],
                medium_term_trend=analysis['MACD']['medium_term_trend'],
                short_term_signal=analysis['MACD']['short_term_signal'],
                divergence=analysis['MACD']['divergence'],
                strength=analysis['MACD']['strength'],
                signal=analysis['MACD']['signal']
            ),
            'KDJ': lambda: get_kdj_analysis_prompt(
                k_value=analysis['KDJ']['K'],
                d_value=analysis['KDJ']['D'],
                j_value=analysis['KDJ']['J'],
                analysis_result={
                    'long_term_trend': analysis['KDJ']['long_term_trend'],
                    'medium_term_trend': analysis['KDJ']['medium_term_trend'],
                    'short_term_trend': analysis['KDJ']['short_term_trend'],
                    'cross_pattern': analysis['KDJ']['cross_pattern'],
                    'divergence': analysis['KDJ']['divergence'],
                    'strength': analysis['KDJ']['strength'],
                    'pattern': analysis['KDJ']['pattern'],
                    'signal': analysis['KDJ']['signal']
                }
            ),
            'RSI': lambda: get_rsi_analysis_prompt(
                rsi6=analysis['RSI']['RSI6'],
                rsi12=analysis['RSI']['RSI12'],
                rsi24=analysis['RSI']['RSI24'],
                long_term_trend=analysis['RSI']['long_term_trend'],
                medium_term_trend=analysis['RSI']['medium_term_trend'],
                short_term_signal=analysis['RSI']['short_term_signal'],
                divergence=analysis['RSI']['divergence'],
                strength=analysis['RSI']['strength'],
                pattern=analysis['RSI']['pattern'],
                signal=analysis['RSI']['signal']
            ),
            'BOLL': lambda: get_boll_analysis_prompt(
                upper=analysis['BOLL']['UPPER'],
                mid=analysis['BOLL']['MID'],
                lower=analysis['BOLL']['LOWER'],
                signal=analysis['BOLL']['signal']
            )
        }
        
        if indicator_name not in indicator_prompts:
            raise ValueError(f"不支持的技术指标: {indicator_name}")
            
        # 获取指标的prompt
        indicator_prompt = indicator_prompts[indicator_name]()
        
        # 构建完整的报告模板
        report_template = f"""
# {stock_name} - {indicator_name}技术指标分析报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 市场数据
- 最新收盘价：{latest_price:.2f}
- 涨跌幅：{price_change:.2f}%
- 成交量变化：{vol_change:.2f}%

{indicator_prompt}
"""
        try:
            # 调用Gemini API生成分析报告
            response = self.model.generate_content(report_template)
            return response.text
        except Exception as e:
            error_msg = f"生成{indicator_name}指标报告时发生错误: {str(e)}"
            return f"""
# {stock_name} - {indicator_name}技术指标分析报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 错误信息
{error_msg}
"""

    def save_indicator_report(self, stock_name: str, indicator_name: str, report_content: str) -> str:
        """
        保存单个技术指标的分析报告
        
        参数:
            stock_name (str): 股票名称
            indicator_name (str): 技术指标名称
            report_content (str): 报告内容
            
        返回:
            str: 报告文件路径
        """
        if self.current_report_dir is None:
            # 如果还没有创建目录，创建一个新的
            self.current_report_dir = self._create_report_directory(stock_name)
        
        # 保存报告文件到当前目录
        report_file = os.path.join(self.current_report_dir, f"{indicator_name.lower()}_analysis.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        return report_file 