"""
均线系统分析的prompt模板
"""

from typing import Dict, Any

def get_ma_system_analysis_prompt(analysis_results: Dict[str, Any]) -> str:
    """
    生成均线系统分析的prompt模板
    
    参数:
        analysis_results (Dict[str, Any]): 均线分析结果，包含以下字段：
            - ma_values: 各均线当前值
            - long_term_trend: 长期趋势分析结果
            - medium_term_trend: 中期趋势分析结果
            - short_term_signal: 短期信号分析
            - formation: 均线形态
            - strength: 均线系统强度
            - support_resistance: 支撑阻力位
            - signal: 综合信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### 趋势分析
- 长期趋势：{analysis_results['long_term_trend']['trend']}
- 中期趋势：{analysis_results['medium_term_trend']['trend']}
- 短期信号：{analysis_results['short_term_signal']['summary']}

### 短期技术特征
{_format_short_term_details(analysis_results['short_term_signal'])}

### 均线形态特征
- 形态类型：{analysis_results['formation']['type']}
- 形态强度：{analysis_results['formation']['strength']}
- 均线分散度：{analysis_results['formation']['dispersion']:.4f}

### 支撑与阻力
{_format_support_resistance(analysis_results['support_resistance'])}

### 系统强度与综合信号
- 均线系统强度：{analysis_results['strength']['strength']}
- 综合研判信号：{analysis_results['signal']}

请基于以上均线系统数据进行深入分析：

1. 均线系统形态分析
   - 均线排列形态研判
     * 多空头排列确认
     * 排列强度评估
     * 形态转换迹象
   - 均线交叉信号分析
     * 重要均线交叉位置
     * 交叉信号可信度
     * 假突破风险评估
   - 均线密集区分析
     * 密集区形成位置
     * 突破可能性研判
     * 支撑阻力有效性

2. 多周期趋势研判
   - 长期趋势分析（250日均线）
     * 趋势方向确认
     * 趋势强度评估
     * 趋势持续性分析
   - 中期趋势分析（60日均线）
     * 与长期趋势的协调性
     * 调整空间预判
     * 趋势转折信号
   - 短期趋势分析（20日均线）
     * 短线机会把握
     * 反转信号确认
     * 风险点识别

3. 均线系统特征分析
   - 均线乖离度分析
     * 价格与均线距离
     * 超买超卖判断
     * 回归概率评估
   - 均线拐点特征
     * 关键均线拐点
     * 趋势加速/减速
     * 转势信号研判
   - 成交量配合
     * 突破成交量确认
     * 支撑阻力有效性
     * 量能变化特征

4. 操作建议
   - 交易信号分析
     * 开仓机会判断
     * 减仓时机选择
     * 止损位设置
   - 建仓策略
     * 进场时机选择
     * 仓位控制建议
     * 分批操作建议
   - 风险控制
     * 关键支撑位止损
     * 均线止损方案
     * 风险规避建议

注意事项：
1. 均线系统分析需要结合市场环境和行业特征
2. 不同周期均线的权重应随市场环境灵活调整
3. 建议结合其他技术指标交叉验证
4. 重要均线突破需要成交量配合确认
5. 均线系统信号可能存在滞后，需要综合判断
"""

def _format_short_term_details(short_term: Dict[str, Any]) -> str:
    """格式化短期技术特征"""
    details = []
    
    # 添加均线交叉信号
    if short_term['cross_signals']:
        details.append("均线交叉信号：")
        for signal in short_term['cross_signals']:
            short_ma = signal['short_ma'].replace('ma_qfq_', '')
            long_ma = signal['long_ma'].replace('ma_qfq_', '')
            signal_type = "金叉" if signal['type'] == 'golden_cross' else "死叉"
            details.append(f"  - {short_ma}日线与{long_ma}日线形成{signal['strength']}{signal_type}")
    
    # 添加拐点信号
    if short_term['turning_signals']:
        details.append("\n拐点信号：")
        for ma, info in short_term['turning_signals'].items():
            ma_days = ma.replace('ma_qfq_', '')
            details.append(f"  - {ma_days}日均线{info['type']}")
    
    # 添加突破信号
    if short_term['breakthrough']['type'] != 'no_breakthrough':
        details.append("\n突破信号：")
        direction = "向上" if short_term['breakthrough']['type'] == 'upward_breakthrough' else "向下"
        strength = "强势" if short_term['breakthrough'].get('strength') == 'strong' else "普通"
        details.append(f"  - 均线密集区{direction}突破（{strength}）")
        if 'price_change_pct' in short_term['breakthrough']:
            details.append(f"  - 价格变动：{short_term['breakthrough']['price_change_pct']:.2f}%")
        if 'volume_change' in short_term['breakthrough']:
            details.append(f"  - 成交量放大：{short_term['breakthrough']['volume_change']:.2f}倍")
    
    # 添加趋势强度
    details.append("\n趋势强度：")
    momentum_dir = "上涨" if short_term['trend_strength']['momentum'] > 0 else "下跌"
    details.append(f"  - 动能方向：{momentum_dir}")
    details.append(f"  - 动能强度：{short_term['trend_strength']['strength']}")
    details.append(f"  - 动能值：{short_term['trend_strength']['momentum']:.2f}%")
    
    # 添加乖离状态
    details.append("\n乖离状态：")
    details.append(f"  - 当前状态：{short_term['deviation']['status']}")
    details.append(f"  - 平均乖离率：{short_term['deviation']['average_deviation']:.2f}%")
    details.append(f"  - 最大乖离率：{short_term['deviation']['max_deviation']:.2f}%")
    
    return "\n".join(details)

def _format_support_resistance(sr_data: Dict[str, Any]) -> str:
    """格式化支撑阻力位信息"""
    details = []
    
    # 添加支撑位信息
    if sr_data['support_levels']:
        details.append("支撑位：")
        for level in sr_data['support_levels'][:3]:  # 只显示前3个支撑位
            ma_days = level['ma'].replace('ma_qfq_', '')
            details.append(f"  - {ma_days}日均线：{level['value']:.2f}")
    
    # 添加阻力位信息
    if sr_data['resistance_levels']:
        details.append("\n阻力位：")
        for level in sr_data['resistance_levels'][:3]:  # 只显示前3个阻力位
            ma_days = level['ma'].replace('ma_qfq_', '')
            details.append(f"  - {ma_days}日均线：{level['value']:.2f}")
    
    # 添加当前价格信息
    details.append(f"\n当前价格：{sr_data['current_price']:.2f}")
    
    return "\n".join(details)
