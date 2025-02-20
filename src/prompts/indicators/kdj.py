"""
KDJ指标分析的prompt模板
"""

def get_kdj_analysis_prompt(k_value: float, d_value: float, j_value: float, 
                          analysis_result: dict) -> str:
    """
    生成KDJ指标分析的prompt模板
    
    参数:
        k_value (float): K值
        d_value (float): D值
        j_value (float): J值
        analysis_result (dict): KDJ分析结果，包含以下字段：
            - long_term_trend: 长期趋势
            - medium_term_trend: 中期趋势
            - short_term_trend: 短期趋势
            - cross_pattern: 交叉形态
            - divergence: 背离情况
            - strength: 指标强度
            - pattern: KDJ形态
            - signal: 综合信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### KDJ指标基础数据
当前KDJ指标数据：
- K值：{k_value:.2f}
- D值：{d_value:.2f}
- J值：{j_value:.2f}

### 趋势分析
- 长期趋势：{analysis_result['long_term_trend']}
- 中期趋势：{analysis_result['medium_term_trend']}
- 短期趋势：{analysis_result['short_term_trend']}

### 技术形态特征
- 交叉形态：{analysis_result['cross_pattern']}
- 背离情况：{analysis_result['divergence']}
- KDJ形态：{analysis_result['pattern']}
- 指标强度：{analysis_result['strength']}

### 综合信号
- 建议操作：{analysis_result['signal']}

请基于以上KDJ指标数据进行深入分析：

1. KDJ指标形态特征分析
   - 当前KDJ指标位置判断（超买/超卖区间）
   - KDJ三线交叉形态分析
     * K线与D线的交叉位置
     * J线的摆动幅度
     * 金叉/死叉形态确认
   - 指标背离情况研判
     * 顶背离/底背离识别
     * 背离强度评估
     * 背离持续性分析

2. 多周期趋势研判
   - 长期趋势分析（主趋势）
     * 趋势的持续性评估
     * 趋势强度判断
   - 中期趋势分析（次趋势）
     * 与主趋势的关系
     * 调整空间预判
   - 短期趋势分析（当前趋势）
     * 趋势延续性分析
     * 可能的反转信号

3. 市场情绪研判
   - 基于KDJ位置的市场情绪分析
     * 超买区域（80以上）表现
     * 超卖区域（20以下）表现
     * 中性区域震荡特征
   - 结合K、D、J三线位置关系分析
     * 三线发散/收敛形态
     * 粘合区域分析
   - 指标强度评估
     * 当前强度水平
     * 强度变化趋势

4. 操作建议
   - 交易信号分析
     * 开仓机会判断
     * 减仓时机选择
     * 止损位设置
   - 建仓策略
     * 进场时机选择
     * 仓位控制建议
   - 风险提示
     * 潜在风险点
     * 止损条件设置

注意事项：
1. 本分析基于技术面，建议结合基本面综合判断
2. KDJ指标存在一定滞后性，建议结合其他指标交叉验证
3. 不同市场环境下指标参数敏感度不同，需要灵活调整
4. 任何技术指标都不能保证100%准确，请控制好仓位和风险
""" 