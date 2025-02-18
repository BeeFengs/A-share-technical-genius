"""
技术指标prompt模板包
"""

from .kdj import get_kdj_analysis_prompt
from .macd import get_macd_analysis_prompt
from .rsi import get_rsi_analysis_prompt
from .boll import get_boll_analysis_prompt

__all__ = [
    'get_kdj_analysis_prompt',
    'get_macd_analysis_prompt',
    'get_rsi_analysis_prompt',
    'get_boll_analysis_prompt'
] 