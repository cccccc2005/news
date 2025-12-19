# 莎士比亚反派性格量化分析项目

基于文本数据挖掘的方法，量化解析莎士比亚悲剧中经典反派的性格特征。

## 📋 项目简介

本项目通过构建"词频-句法-互动"三维量化指标体系，对《哈姆雷特》《麦克白》《奥赛罗》三个剧本中的反派角色（克劳狄斯、麦克白、伊阿古）进行性格量化分析。

### 研究目标
- 构建适配中译本的量化分析体系
- 揭示三个反派性格的量化特征差异
- 提供可复现的分析流程和工具包

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 准备数据

将三个Word文档（哈姆雷特、麦克白、奥赛罗）放到项目根目录：
- `哈姆雷特.docx`
- `麦克白.docx`
- `奥赛罗.docx`

**注意**：确保Word文档文件名包含剧本名称，脚本会自动识别。

### 3. 运行分析

#### 步骤1：提取台词数据
```bash
python extract_word.py
```

**作用**：从Word文档中提取三个反派的台词，保存为CSV格式。

**输出**：
- `output/villain_lines.csv` - 原始台词数据（592条）
- `output/raw_text_*.txt` - 各剧本的原始文本（用于调试）

#### 步骤2：计算量化指标
```bash
python main.py
```

**作用**：计算三维指标体系（词频、句法、互动），生成量化特征数据。

**输出**：
- `output/villain_features.csv` - 量化特征数据表

#### 步骤3：生成可视化图表
```bash
python visualize.py
```

**作用**：生成雷达图和柱状图，可视化展示三个角色的性格差异。

**输出**：
- `output/radar_chart.png` - 雷达图（多维度对比）
- `output/bar_charts.png` - 柱状图（单项指标对比）

#### 步骤4（可选）：高级分析
```bash
python advanced_analysis.py
```

**作用**：进行相关性分析，生成热力图和综合对比图。

**输出**：
- `output/correlation_heatmap.png` - 相关性热力图
- `output/comprehensive_comparison.png` - 综合对比图
- `output/statistical_summary.txt` - 统计摘要

#### 步骤5（可选）：提取文本证据
```bash
python extract_evidence.py
```

**作用**：提取每个角色的关键词台词示例，便于论文引用。

**输出**：
- `output/evidence_report.txt` - 文本证据报告

#### 步骤6（可选）：生成论文报告
```bash
python generate_report.py
```

**作用**：生成LaTeX表格和Markdown报告，可直接用于论文。

**输出**：
- `output/latex_table.txt` - LaTeX表格代码
- `output/analysis_report.md` - Markdown报告

---

## 📁 代码文件说明

### 核心分析脚本

#### `extract_word.py` ⭐⭐⭐
**功能**：从Word文档提取台词数据

**主要功能**：
- 自动识别三个Word文档对应的剧本
- 提取角色台词（支持多种格式：`角色名：台词`、`角色名`单独一行等）
- 处理表格中的文本（如麦克白剧本）
- 特殊处理：识别"国王"为克劳狄斯

**输出**：`output/villain_lines.csv`

---

#### `main.py` ⭐⭐⭐
**功能**：计算三维量化指标

**主要功能**：
- **词频维度**：统计权力、谎言、野心等关键词的每千词频次
- **句法维度**：计算平均句长、复杂句比例
- **互动维度**：统计指令句比例、打断次数

**处理流程**：
1. 读取台词数据
2. 中文分词（jieba）
3. 停用词过滤
4. 同义词归并
5. 关键词统计
6. 句法分析
7. 互动特征计算

**输出**：`output/villain_features.csv`

---

#### `visualize.py` ⭐⭐⭐
**功能**：生成可视化图表

**主要功能**：
- 生成雷达图：展示多维度性格差异
- 生成柱状图：展示单项指标对比
- 数据归一化处理
- 颜色方案配置（克劳狄斯-红色、麦克白-蓝色、伊阿古-橙色）

**输出**：
- `output/radar_chart.png`
- `output/bar_charts.png`

---

### 配置文件

#### `config.py` ⭐⭐⭐
**功能**：配置关键词表和参数

**主要内容**：
- `VILLAINS`：三个反派角色列表
- `KEYWORD_GROUPS`：关键词分组（权力、谎言、野心、暴力、恐惧）
- `COMMAND_CUES`：指令句判断词
- `COMPLEX_CLAUSE_MARKERS`：复杂句连接词

**修改建议**：如需调整关键词表，编辑此文件。

---

### 辅助分析脚本

#### `advanced_analysis.py`
**功能**：高级统计分析

**主要功能**：
- 相关性分析：计算各指标间的相关性
- 生成相关性热力图
- 生成综合对比图（4个子图）
- 生成统计摘要

**输出**：
- `output/correlation_heatmap.png`
- `output/comprehensive_comparison.png`
- `output/statistical_summary.txt`

---

#### `extract_evidence.py`
**功能**：提取文本证据

**主要功能**：
- 为每个角色提取关键词台词示例
- 高亮显示关键词
- 标注剧本、幕次、场次信息

**输出**：`output/evidence_report.txt`

---

#### `generate_report.py`
**功能**：生成论文报告

**主要功能**：
- 生成LaTeX格式表格
- 生成Markdown格式报告
- 包含数据概览、数据表、主要发现

**输出**：
- `output/latex_table.txt`
- `output/analysis_report.md`

---

## 📊 输出文件说明

### 数据文件
- `output/villain_lines.csv` - 原始台词数据（592条）
- `output/villain_features.csv` - 量化特征数据表

### 可视化图表
- `output/radar_chart.png` - 雷达图（多维度对比）
- `output/bar_charts.png` - 柱状图（单项指标对比）
- `output/correlation_heatmap.png` - 相关性热力图
- `output/comprehensive_comparison.png` - 综合对比图

### 报告文件
- `output/evidence_report.txt` - 文本证据报告
- `output/statistical_summary.txt` - 统计摘要
- `output/analysis_report.md` - Markdown报告
- `output/latex_table.txt` - LaTeX表格代码

---

## 🔧 配置说明

### 修改关键词表

编辑 `config.py` 文件中的 `KEYWORD_GROUPS`：

```python
KEYWORD_GROUPS = {
    "power": ["权力", "王冠", "王座", ...],  # 权力类关键词
    "lie": ["谎言", "欺骗", "蒙蔽", ...],    # 谎言类关键词
    "ambition": ["野心", "欲望", "图谋", ...], # 野心类关键词
    # ...
}
```

### 修改角色列表

编辑 `config.py` 文件中的 `VILLAINS`：

```python
VILLAINS = ["克劳狄斯", "麦克白", "伊阿古"]
```

---

## 📈 分析结果

### 主要发现

1. **权力词汇**：伊阿古最高（4.56/千词），符合其对职位升迁的关注
2. **野心词汇**：麦克白最高（2.52/千词），符合其野心勃勃的特征
3. **指令句比例**：麦克白最高（34.38%），体现其强烈的控制欲

### 数据概览

| 角色 | 权力词汇 | 谎言词汇 | 野心词汇 | 平均句长 | 复杂句比例 | 指令句比例 |
|------|---------|---------|---------|----------|-----------|-----------|
| 克劳狄斯 | 1.82 | 1.22 | 0.61 | 31.04 | 18.09% | 32.00% |
| 麦克白 | 1.40 | 1.40 | 2.52 | 30.43 | 17.42% | 34.38% |
| 伊阿古 | 4.56 | 1.52 | 2.43 | 27.31 | 18.10% | 21.64% |

---

## 🛠️ 技术栈

- **Python 3.9**
- **pandas** - 数据处理
- **jieba** - 中文分词
- **matplotlib** - 基础可视化
- **seaborn** - 高级可视化
- **python-docx** - Word文档处理
- **scipy** - 统计分析

---

## 📝 使用流程总结

```
1. 准备Word文档 → 2. 提取台词(extract_word.py) 
   → 3. 计算指标(main.py) → 4. 生成图表(visualize.py)
   → 5. 高级分析(advanced_analysis.py) [可选]
   → 6. 提取证据(extract_evidence.py) [可选]
   → 7. 生成报告(generate_report.py) [可选]
```

---

## ⚠️ 注意事项

1. **Word文档格式**：
   - 确保文件名包含剧本名称（如"哈姆雷特.docx"）
   - 如果文本在表格中，脚本会自动处理

2. **角色名称**：
   - 哈姆雷特中克劳狄斯可能以"国王"标识，脚本会自动识别

3. **数据质量**：
   - 台词数据越完整，分析结果越可靠
   - 建议每个角色至少50-100条台词

4. **关键词表**：
   - 可根据实际需要调整 `config.py` 中的关键词
   - 避免使用过于宽泛的词汇

---

## 🎯 项目特点

1. **中译适配性**：针对中文译本特点，建立同义表达归并规则
2. **三维指标体系**：词频+句法+互动，全面量化性格特征
3. **可复现性**：完整的代码流程，可迁移到其他文学作品
4. **可视化完善**：多种图表展示，直观呈现分析结果

---

