"""
提取文本证据：为每个角色的关键特征找出具体台词示例
"""
import pandas as pd
import re
from pathlib import Path
from config import KEYWORD_GROUPS

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def find_keyword_examples(df, character, keyword_group, keyword_list, max_examples=3):
    """找出包含特定关键词的台词示例"""
    char_df = df[df['character'] == character]
    examples = []
    
    for keyword in keyword_list:
        matches = char_df[char_df['text'].str.contains(keyword, na=False, regex=False)]
        for idx, row in matches.head(max_examples).iterrows():
            text = row['text'].strip()
            # 高亮关键词
            highlighted = text.replace(keyword, f"【{keyword}】")
            examples.append({
                'keyword': keyword,
                'text': text,
                'highlighted': highlighted,
                'play': row['play'],
                'act': row['act'],
                'scene': row['scene']
            })
            if len(examples) >= max_examples * len(keyword_list):
                break
        if len(examples) >= max_examples * len(keyword_list):
            break
    
    return examples[:max_examples]


def generate_evidence_report():
    """生成文本证据报告"""
    df = pd.read_csv(OUTPUT_DIR / "villain_lines.csv", encoding="utf-8-sig")
    features_df = pd.read_csv(OUTPUT_DIR / "villain_features.csv", encoding="utf-8-sig")
    
    report = []
    report.append("="*80)
    report.append("莎士比亚反派性格量化分析 - 文本证据报告")
    report.append("="*80)
    report.append("")
    
    for idx, row in features_df.iterrows():
        character = row['character']
        report.append(f"\n【{character}】")
        report.append("-"*80)
        
        # 权力词汇证据
        if row['power_per_1000'] > 0:
            report.append(f"\n1. 权力词汇特征（频次: {row['power_per_1000']:.2f}/千词）")
            examples = find_keyword_examples(
                df, character, "power", KEYWORD_GROUPS["power"], max_examples=2
            )
            if examples:
                for i, ex in enumerate(examples, 1):
                    report.append(f"   示例{i}: {ex['highlighted'][:100]}...")
            else:
                report.append("   （未找到直接关键词，可能使用间接表达）")
        
        # 野心词汇证据
        if row['ambition_per_1000'] > 0:
            report.append(f"\n2. 野心词汇特征（频次: {row['ambition_per_1000']:.2f}/千词）")
            examples = find_keyword_examples(
                df, character, "ambition", KEYWORD_GROUPS["ambition"], max_examples=2
            )
            if examples:
                for i, ex in enumerate(examples, 1):
                    report.append(f"   示例{i}: {ex['highlighted'][:100]}...")
        
        # 谎言词汇证据
        if row['lie_per_1000'] > 0:
            report.append(f"\n3. 谎言/欺骗词汇特征（频次: {row['lie_per_1000']:.2f}/千词）")
            examples = find_keyword_examples(
                df, character, "lie", KEYWORD_GROUPS["lie"], max_examples=2
            )
            if examples:
                for i, ex in enumerate(examples, 1):
                    report.append(f"   示例{i}: {ex['highlighted'][:100]}...")
        
        # 句法特征
        report.append(f"\n4. 句法特征")
        report.append(f"   平均句长: {row['avg_sentence_length']:.2f} 字符")
        report.append(f"   复杂句比例: {row['complex_ratio']*100:.2f}%")
        
        # 找出长句示例
        char_df = df[df['character'] == character]
        long_sentences = char_df[char_df['text'].str.len() > 50].head(2)
        if len(long_sentences) > 0:
            report.append(f"   长句示例:")
            for i, (idx2, row2) in enumerate(long_sentences.iterrows(), 1):
                report.append(f"     示例{i}: {row2['text'][:80]}...")
        
        # 互动特征
        report.append(f"\n5. 互动特征")
        report.append(f"   指令句比例: {row['command_ratio']*100:.2f}%")
        
        # 找出指令句示例
        from main import is_command_sentence
        command_examples = []
        for idx2, row2 in char_df.iterrows():
            if is_command_sentence(row2['text']):
                command_examples.append(row2['text'])
                if len(command_examples) >= 2:
                    break
        
        if command_examples:
            report.append(f"   指令句示例:")
            for i, ex in enumerate(command_examples, 1):
                report.append(f"     示例{i}: {ex[:80]}...")
    
    # 保存报告
    report_text = "\n".join(report)
    output_path = OUTPUT_DIR / "evidence_report.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print("✓ 文本证据报告已生成:", output_path)
    print("\n报告预览（前500字符）:")
    print(report_text[:500])
    
    return report_text


if __name__ == "__main__":
    generate_evidence_report()

