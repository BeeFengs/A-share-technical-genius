


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

## 当前K线形态解读

### 1. 识别形态
- **形态**: {patterns_str}  # 这里填入识别到的K线形态，例如"看涨吞没形态"或"十字星"等。

### 2. 强度
- **强度**: {strength}  # 这里填入形态的强度评估，例如"强"、"中"、"弱"。

### 3. 交易建议
- **建议**: {suggestion}  # 这里填入基于当前K线形态的交易建议，例如"考虑买入"或"建议观望"等。

# 总结
- 根据当前K线形态的识别、强度和交易建议，投资者可以更好地把握市场情绪和潜在的交易机会。
""" 