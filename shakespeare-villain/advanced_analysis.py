"""
高级分析：相关性分析、统计检验、热力图等
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def correlation_analysis():
    """相关性分析"""
    df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    # 选择数值列
    numeric_cols = [
        'power_per_1000', 'lie_per_1000', 'ambition_per_1000',
        'violence_per_1000', 'fear_per_1000',
        'avg_sentence_length', 'complex_ratio', 'command_ratio'
    ]
    
    corr_matrix = df[numeric_cols].corr()
    
    # 绘制热力图
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('角色特征相关性热力图', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "correlation_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 相关性热力图已保存: {output_path}")
    plt.close()
    
    return corr_matrix


def create_comparison_chart():
    """创建综合对比图"""
    df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('莎士比亚反派性格量化特征综合对比', fontsize=16, fontweight='bold')
    
    characters = df['character'].tolist()
    colors = {
        '克劳狄斯': '#DC143C',
        '麦克白': '#1E90FF',
        '伊阿古': '#FF8C00'
    }
    bar_colors = [colors[char] for char in characters]
    
    x = np.arange(len(characters))
    width = 0.25
    
    # 1. 关键词频次对比（三个维度）
    ax1 = axes[0, 0]
    power_vals = df['power_per_1000'].values
    lie_vals = df['lie_per_1000'].values
    ambition_vals = df['ambition_per_1000'].values
    
    ax1.bar(x - width, power_vals, width, label='权力词汇', color=bar_colors, alpha=0.8)
    ax1.bar(x, lie_vals, width, label='谎言词汇', color=bar_colors, alpha=0.6)
    ax1.bar(x + width, ambition_vals, width, label='野心词汇', color=bar_colors, alpha=0.4)
    
    ax1.set_xlabel('角色')
    ax1.set_ylabel('每千词频次')
    ax1.set_title('关键词频次对比')
    ax1.set_xticks(x)
    ax1.set_xticklabels(characters)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. 句法特征对比
    ax2 = axes[0, 1]
    sentence_len = df['avg_sentence_length'].values
    complex_ratio = df['complex_ratio'].values * 100  # 转换为百分比
    
    ax2_twin = ax2.twinx()
    bars1 = ax2.bar(x - width/2, sentence_len, width, label='平均句长', color=bar_colors, alpha=0.8)
    bars2 = ax2_twin.bar(x + width/2, complex_ratio, width, label='复杂句比例', color=bar_colors, alpha=0.6)
    
    ax2.set_xlabel('角色')
    ax2.set_ylabel('平均句长（字符）', color='black')
    ax2_twin.set_ylabel('复杂句比例（%）', color='black')
    ax2.set_title('句法特征对比')
    ax2.set_xticks(x)
    ax2.set_xticklabels(characters)
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. 互动特征对比
    ax3 = axes[1, 0]
    command_ratio = df['command_ratio'].values * 100
    
    bars = ax3.bar(x, command_ratio, width=0.6, color=bar_colors, alpha=0.8)
    ax3.set_xlabel('角色')
    ax3.set_ylabel('指令句比例（%）')
    ax3.set_title('指令句比例对比（控制欲指标）')
    ax3.set_xticks(x)
    ax3.set_xticklabels(characters)
    ax3.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    # 4. 综合雷达图（简化版）
    ax4 = axes[1, 1]
    
    # 归一化数据用于对比
    metrics = ['power_per_1000', 'lie_per_1000', 'ambition_per_1000', 'command_ratio']
    metric_labels = ['权力', '谎言', '野心', '指令']
    
    normalized_data = []
    for metric in metrics:
        vals = df[metric].values
        if metric == 'command_ratio':
            vals = vals * 100  # 转换为百分比
        max_val = vals.max()
        min_val = vals.min()
        if max_val > min_val:
            normalized = (vals - min_val) / (max_val - min_val)
        else:
            normalized = np.ones_like(vals) * 0.5
        normalized_data.append(normalized)
    
    x_pos = np.arange(len(metric_labels))
    for i, char in enumerate(characters):
        values = [normalized_data[j][i] for j in range(len(metrics))]
        ax4.plot(x_pos, values, 'o-', label=char, color=colors[char], linewidth=2, markersize=8)
    
    ax4.set_xlabel('特征维度')
    ax4.set_ylabel('归一化值（0-1）')
    ax4.set_title('综合特征对比')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(metric_labels)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1.1)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "comprehensive_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 综合对比图已保存: {output_path}")
    plt.close()


def generate_statistical_summary():
    """生成统计摘要"""
    df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    summary = []
    summary.append("="*80)
    summary.append("统计分析摘要")
    summary.append("="*80)
    summary.append("")
    
    # 描述性统计
    summary.append("【描述性统计】")
    numeric_cols = ['power_per_1000', 'lie_per_1000', 'ambition_per_1000',
                    'avg_sentence_length', 'complex_ratio', 'command_ratio']
    
    for col in numeric_cols:
        values = df[col].values
        summary.append(f"\n{col}:")
        summary.append(f"  均值: {np.mean(values):.4f}")
        summary.append(f"  标准差: {np.std(values):.4f}")
        summary.append(f"  最大值: {np.max(values):.4f} ({df.loc[df[col].idxmax(), 'character']})")
        summary.append(f"  最小值: {np.min(values):.4f} ({df.loc[df[col].idxmin(), 'character']})")
    
    # 排名统计
    summary.append("\n\n【各维度排名】")
    for col in numeric_cols:
        ranked = df.sort_values(col, ascending=False)
        summary.append(f"\n{col}排名:")
        for i, (idx, row) in enumerate(ranked.iterrows(), 1):
            summary.append(f"  {i}. {row['character']}: {row[col]:.4f}")
    
    summary_text = "\n".join(summary)
    output_path = OUTPUT_DIR / "statistical_summary.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    print("✓ 统计摘要已保存:", output_path)
    print("\n摘要预览:")
    print(summary_text[:500])
    
    return summary_text


def main():
    print("正在进行高级分析...")
    
    # 相关性分析
    corr_matrix = correlation_analysis()
    print("\n相关性矩阵:")
    print(corr_matrix)
    
    # 综合对比图
    create_comparison_chart()
    
    # 统计摘要
    generate_statistical_summary()
    
    print("\n✓ 高级分析完成！")


if __name__ == "__main__":
    main()

