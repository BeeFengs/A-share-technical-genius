# 慧眼识股：基于AI的股票技术分析工具

## 项目简介

慧眼识股是一个专注于股票技术分析的Python工具，它结合了传统技术指标分析和现代AI技术，为投资者提供深入的市场洞察。目前主要提供股票的技术面分析报告，包括均线、MACD、KDJ等技术指标的智能解读。

## 功能特点

- **技术指标分析**：自动计算并解读K线形态、MA、MACD、KDJ、RSI、Boll带等核心技术指标
- **AI辅助解读**：利用多个AI模型对技术指标进行智能解读
- **自动报告生成**：生成包含详细分析的markdown格式报告
- **数据可视化**：使用Plotly生成交互式K线和技术指标图表

## 项目结构

```
.
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── data_fetcher.py    # 数据获取模块
│   ├── visualizer.py      # 数据可视化模块
│   ├── report_generator.py # 报告生成模块
│   ├── analyzers/         # 分析器模块
│   │   ├── technical_indicators.py  # 技术指标分析器基类
│   │   └── indicators/    # 具体指标分析器
│   │       ├── ma_system_analyzer.py  # 均线系统分析
│   │       ├── macd_analyzer.py       # MACD指标分析
│   │       ├── kdj_analyzer.py        # KDJ指标分析
│   │       ├── rsi_analyzer.py        # RSI指标分析
│   │       ├── boll_analyzer.py       # 布林带分析
│   │       └── candlestick_analyzer.py # K线图分析
│   └── prompts/           # AI提示词模板
│       ├── technical_analysis.py      # 技术分析主提示词
│       └── indicators/    # 各指标的AI分析提示词
│           ├── ma_system.py   # 均线系统分析提示词
│           ├── macd.py        # MACD分析提示词
│           ├── kdj.py         # KDJ分析提示词
│           ├── rsi.py         # RSI分析提示词
│           ├── boll.py        # 布林带分析提示词
│           └── candlestick.py  # K线图分析提示词
├── data/                   # 数据存储目录
├── analysis_reports/       # 分析报告输出目录
├── requirements.txt        # 项目依赖
└── .env                   # 环境变量配置
```

### 核心模块说明

#### 1. 分析器模块 (analyzers/)
- **technical_indicators.py**: 定义了技术指标分析的基础类和接口
- **indicators/**: 包含各个具体的技术指标分析器
  - **ma_system_analyzer.py**: 实现了移动平均线系统（MA5/10/20/30/60）的分析逻辑
  - **macd_analyzer.py**: 实现MACD指标的计算和分析
  - **kdj_analyzer.py**: 实现KDJ随机指标的分析
  - **rsi_analyzer.py**: 实现相对强弱指标(RSI)的分析
  - **boll_analyzer.py**: 实现布林带指标的分析
  - **candlestick_analyzer.py**: 实现K线图的分析

#### 2. AI提示词模块 (prompts/)
- **technical_analysis.py**: 包含整体技术分析的AI提示模板
- **indicators/**: 包含各个技术指标的专门AI分析提示词
  - **ma_system.py**: 均线系统分析的AI提示词模板
  - **macd.py**: MACD指标分析的AI提示词模板
  - **kdj.py**: KDJ指标分析的AI提示词模板
  - **rsi.py**: RSI指标分析的AI提示词模板
  - **boll.py**: 布林带分析的AI提示词模板
  - **candlestick.py**: K线图分析的AI提示词模板

#### 3. 其他核心模块
- **data_fetcher.py**: 负责从Tushare获取股票数据
- **visualizer.py**: 使用Plotly实现交互式图表绘制
- **report_generator.py**: 生成markdown格式的分析报告
- **main.py**: 程序主入口，协调各模块工作

## 环境要求

- Python 3.8+
- Tushare Pro API Token（需要在[Tushare Pro](https://tushare.pro/)注册获取）
- Google AI Studio API Key（用于Gemini模型访问）
  - 访问 [Google AI Studio](https://makersuite.google.com/app/apikey) 获取免费API密钥
  - 每个账号每分钟可以进行60次免费调用
  - 支持多语言分析，可以生成中文分析报告

## 环境变量配置

在项目根目录创建 `.env` 文件，添加以下配置：
```bash
# Tushare API配置
TUSHARE_TOKEN=你的Tushare_token

# Google AI配置
GOOGLE_API_KEY=你的Google_API_Key
```

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖包：
- tushare >= 1.2.89
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- plotly >= 5.3.0
- python-dotenv >= 0.19.0
- google-generativeai >= 0.3.0

## 快速开始

1. 克隆项目到本地
   ```bash
   git clone https://github.com/your-username/share_content_matrix.git
   cd share_content_matrix
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量
   按照上述"环境变量配置"部分设置 `.env` 文件

4. 运行分析
   ```python
   python src/main.py
   ```

5. 查看结果
   分析报告将生成在 `analysis_reports` 目录下，以md格式保存

## 示例报告

目前已支持生成的分析报告包括：
- technical_analysis_000002.SZ.html
- technical_analysis_000007.SZ.html

## 开发计划

- [x] 基础技术指标分析
- [x] AI智能解读
- [x] markdown报告生成
- [ ] 更多技术指标支持
- [ ] 实时行情分析
- [ ] 板块分析功能

## 免责声明

本工具仅供学习和研究使用，不构成任何投资建议。投资者应对自己的投资行为负责。股市有风险，投资需谨慎。

## 联系方式

- 邮箱：qishen_zhen@163.com

## 许可证

MIT License


