"""
生成论文用的格式化报告
"""
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def generate_latex_table():
    """生成LaTeX格式的表格"""
    df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    latex = []
    latex.append("\\begin{table}[h]")
    latex.append("\\centering")
    latex.append("\\caption{莎士比亚反派性格量化特征数据表}")
    latex.append("\\label{tab:villain_features}")
    latex.append("\\begin{tabular}{lcccccc}")
    latex.append("\\toprule")
    latex.append("角色 & 权力词汇 & 谎言词汇 & 野心词汇 & 平均句长 & 复杂句比例 & 指令句比例 \\\\")
    latex.append(" & (每千词) & (每千词) & (每千词) & (字符) & (\\%) & (\\%) \\\\")
    latex.append("\\midrule")
    
    for idx, row in df.iterrows():
        char = row['character']
        power = row['power_per_1000']
        lie = row['lie_per_1000']
        ambition = row['ambition_per_1000']
        sentence_len = row['avg_sentence_length']
        complex_ratio = row['complex_ratio'] * 100
        command_ratio = row['command_ratio'] * 100
        
        latex.append(f"{char} & {power:.2f} & {lie:.2f} & {ambition:.2f} & {sentence_len:.2f} & {complex_ratio:.2f} & {command_ratio:.2f} \\\\")
    
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    
    latex_text = "\n".join(latex)
    output_path = OUTPUT_DIR / "latex_table.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(latex_text)
    
    print("✓ LaTeX表格已生成:", output_path)
    return latex_text


def generate_markdown_report():
    """生成Markdown格式的报告"""
    df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    md = []
    md.append("# 莎士比亚反派性格量化分析结果报告")
    md.append("")
    md.append("## 一、数据概览")
    md.append("")
    md.append(f"- **总台词数**: {df['total_utterances'].sum()} 条")
    md.append(f"- **克劳狄斯**: {df[df['character']=='克劳狄斯']['total_utterances'].values[0]} 条")
    md.append(f"- **麦克白**: {df[df['character']=='麦克白']['total_utterances'].values[0]} 条")
    md.append(f"- **伊阿古**: {df[df['character']=='伊阿古']['total_utterances'].values[0]} 条")
    md.append("")
    
    md.append("## 二、量化特征数据表")
    md.append("")
    md.append("| 角色 | 权力词汇<br>(每千词) | 谎言词汇<br>(每千词) | 野心词汇<br>(每千词) | 平均句长<br>(字符) | 复杂句比例<br>(%) | 指令句比例<br>(%) |")
    md.append("|------|:---:|:---:|:---:|:---:|:---:|:---:|")
    
    for idx, row in df.iterrows():
        char = row['character']
        power = row['power_per_1000']
        lie = row['lie_per_1000']
        ambition = row['ambition_per_1000']
        sentence_len = row['avg_sentence_length']
        complex_ratio = row['complex_ratio'] * 100
        command_ratio = row['command_ratio'] * 100
        
        md.append(f"| {char} | {power:.2f} | {lie:.2f} | {ambition:.2f} | {sentence_len:.2f} | {complex_ratio:.2f} | {command_ratio:.2f} |")
    
    md.append("")
    md.append("## 三、主要发现")
    md.append("")
    
    # 找出各维度的最高值
    power_max = df.loc[df['power_per_1000'].idxmax()]
    ambition_max = df.loc[df['ambition_per_1000'].idxmax()]
    command_max = df.loc[df['command_ratio'].idxmax()]
    
    md.append(f"1. **权力词汇**: {power_max['character']}最高（{power_max['power_per_1000']:.2f}/千词）")
    md.append(f"2. **野心词汇**: {ambition_max['character']}最高（{ambition_max['ambition_per_1000']:.2f}/千词）")
    md.append(f"3. **指令句比例**: {command_max['character']}最高（{command_max['command_ratio']*100:.2f}%）")
    md.append("")
    
    md.append("## 四、可视化图表")
    md.append("")
    md.append("- `radar_chart.png`: 雷达图展示多维度性格差异")
    md.append("- `bar_charts.png`: 柱状图展示单项指标对比")
    md.append("- `correlation_heatmap.png`: 相关性热力图")
    md.append("- `comprehensive_comparison.png`: 综合对比图")
    md.append("")
    
    md_text = "\n".join(md)
    output_path = OUTPUT_DIR / "analysis_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    
    print("✓ Markdown报告已生成:", output_path)
    return md_text


def main():
    print("正在生成论文用报告...")
    
    # LaTeX表格
    generate_latex_table()
    
    # Markdown报告
    generate_markdown_report()
    
    print("\n✓ 报告生成完成！")


if __name__ == "__main__":
    main()

