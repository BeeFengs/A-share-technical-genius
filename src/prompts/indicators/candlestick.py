


def get_candlestick_analysis_prompt(
    patterns: list,
    strength: str,
    suggestion: str
) -> str:
    """
    生成K线形态分析的prompt模板
    
    参数:
        patterns (list): 识别到的K线形态列表
        strength (str): K线形态分析的强度
        suggestion (str): 交易建议
    
    返回:
        str: 格式化后的分析报告模板
    """
    patterns_str = ', '.join(patterns) if patterns else '无'
    return f"""
# K线形态分析报告

## 一、当前K线形态数据
### 1.1 识别形态
- 形态: {patterns_str}

### 1.2 强度
- 强度: {strength}

### 1.3 交易建议
- 建议: {suggestion}

## 二、形态分析
### 2.1 形态特征
- 形态的市场含义

### 2.2 交易信号
- 交易信号的可靠性
- 交易信号的时效性

### 2.3 风险提示
- 形态分析的局限性
- 可能存在的风险因素
""" 