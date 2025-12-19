"""
可视化脚本：生成雷达图和柱状图
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def create_radar_chart(df: pd.DataFrame):
    """创建雷达图：展示三个反派在多个维度上的差异"""
    # 选择要展示的指标
    metrics = [
        "power_per_1000",
        "lie_per_1000",
        "ambition_per_1000",
        "avg_sentence_length",
        "complex_ratio",
        "command_ratio"
    ]
    
    metric_labels = {
        "power_per_1000": "权力词汇",
        "lie_per_1000": "谎言词汇",
        "ambition_per_1000": "野心词汇",
        "avg_sentence_length": "平均句长",
        "complex_ratio": "复杂句比例",
        "command_ratio": "指令句比例"
    }
    
    # 归一化数据（0-1范围）
    df_normalized = df.copy()
    for metric in metrics:
        if metric in df.columns:
            max_val = df[metric].max()
            min_val = df[metric].min()
            if max_val > min_val:
                df_normalized[metric] = (df[metric] - min_val) / (max_val - min_val)
            else:
                df_normalized[metric] = 0.5
    
    # 设置雷达图
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # 为每个角色指定明确的颜色，确保对比明显
    character_colors = {
        '克劳狄斯': '#DC143C',  # 深红色
        '麦克白': '#1E90FF',    # 深蓝色
        '伊阿古': '#FF8C00'      # 深橙色
    }
    
    # 如果角色名不在字典中，使用默认颜色
    default_colors = ['#DC143C', '#1E90FF', '#FF8C00']
    
    for idx, row in df.iterrows():
        character = row['character']
        values = [df_normalized.loc[idx, m] for m in metrics]
        values += values[:1]  # 闭合
        
        # 获取角色对应的颜色
        color = character_colors.get(character, default_colors[idx % len(default_colors)])
        
        ax.plot(angles, values, 'o-', linewidth=3, label=character, color=color, markersize=8)
        ax.fill(angles, values, alpha=0.2, color=color)
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([metric_labels[m] for m in metrics])
    ax.set_ylim(0, 1)
    ax.set_title('莎士比亚反派性格量化特征雷达图', size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "radar_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 雷达图已保存: {output_path}")
    plt.close()


def create_bar_charts(df: pd.DataFrame):
    """创建柱状图：展示关键词频次对比"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('莎士比亚反派性格量化特征对比', fontsize=16, fontweight='bold')
    
    characters = df['character'].tolist()
    x = np.arange(len(characters))
    width = 0.35
    
    # 统一的颜色方案
    bar_colors = []
    for char in characters:
        if char == '克劳狄斯':
            bar_colors.append('#DC143C')  # 深红色
        elif char == '麦克白':
            bar_colors.append('#1E90FF')  # 深蓝色
        elif char == '伊阿古':
            bar_colors.append('#FF8C00')  # 深橙色
        else:
            bar_colors.append('#808080')  # 灰色（备用）
    
    # 1. 权力词汇频次
    if 'power_per_1000' in df.columns:
        ax1 = axes[0, 0]
        ax1.bar(x, df['power_per_1000'], width, color=bar_colors)
        ax1.set_xlabel('角色')
        ax1.set_ylabel('每千词频次')
        ax1.set_title('权力类词汇频次')
        ax1.set_xticks(x)
        ax1.set_xticklabels(characters)
        ax1.grid(axis='y', alpha=0.3)
    
    # 2. 谎言词汇频次
    if 'lie_per_1000' in df.columns:
        ax2 = axes[0, 1]
        ax2.bar(x, df['lie_per_1000'], width, color=bar_colors)
        ax2.set_xlabel('角色')
        ax2.set_ylabel('每千词频次')
        ax2.set_title('谎言类词汇频次')
        ax2.set_xticks(x)
        ax2.set_xticklabels(characters)
        ax2.grid(axis='y', alpha=0.3)
    
    # 3. 平均句长
    if 'avg_sentence_length' in df.columns:
        ax3 = axes[1, 0]
        ax3.bar(x, df['avg_sentence_length'], width, color=bar_colors)
        ax3.set_xlabel('角色')
        ax3.set_ylabel('字符数')
        ax3.set_title('平均句长')
        ax3.set_xticks(x)
        ax3.set_xticklabels(characters)
        ax3.grid(axis='y', alpha=0.3)
    
    # 4. 指令句比例
    if 'command_ratio' in df.columns:
        ax4 = axes[1, 1]
        ax4.bar(x, df['command_ratio'], width, color=bar_colors)
        ax4.set_xlabel('角色')
        ax4.set_ylabel('比例')
        ax4.set_title('指令句比例')
        ax4.set_xticks(x)
        ax4.set_xticklabels(characters)
        ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "bar_charts.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 柱状图已保存: {output_path}")
    plt.close()


def main():
    csv_path = OUTPUT_DIR / "villain_features.csv"
    
    if not csv_path.exists():
        print(f"错误: 找不到特征数据文件 {csv_path}")
        print("请先运行 main.py 生成特征数据")
        return
    
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"读取特征数据: {len(df)} 个角色")
    
    # 创建可视化
    create_radar_chart(df)
    create_bar_charts(df)
    
    print("\n✓ 所有可视化图表已生成完成！")


if __name__ == "__main__":
    main()

