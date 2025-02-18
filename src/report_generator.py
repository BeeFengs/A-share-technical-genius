"""
报告生成模块 - 使用 Google Gemini API 生成技术分析报告
"""
import os
from typing import Dict
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from src.prompts.technical_analysis import get_technical_analysis_prompt

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