"""
主分析脚本：从CSV数据计算三维指标（词频-句法-互动）
"""
import os
import json
from collections import Counter
import pandas as pd
import numpy as np
import jieba
from config import VILLAINS, KEYWORD_GROUPS, COMMAND_CUES, COMPLEX_CLAUSE_MARKERS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_stopwords(path: str) -> set:
    """加载停用词表"""
    if not os.path.exists(path):
        # 创建基础停用词表
        default_stopwords = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
            "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
            "自己", "这", "那", "他", "她", "它", "们", "这", "那", "这", "那"
        }
        return default_stopwords
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def load_synonyms(path: str) -> dict:
    """加载同义词映射表"""
    if not os.path.exists(path):
        # 创建基础同义词映射
        default_synonyms = {
            "王冠": "权力",
            "王座": "权力",
            "王位": "权力",
            "统治": "权力",
            "主宰": "权力",
            "掌控": "权力",
            "控制": "权力",
            "支配": "权力",
            "欺骗": "谎言",
            "蒙蔽": "谎言",
            "隐瞒": "谎言",
            "伪装": "谎言",
            "虚假": "谎言",
            "虚伪": "谎言",
            "假象": "谎言",
            "掩饰": "谎言",
            "欲望": "野心",
            "企图": "野心",
            "图谋": "野心",
            "贪婪": "野心",
            "渴望": "野心",
            "追求": "野心",
        }
        return default_synonyms
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_token(token: str, synonyms: dict) -> str:
    """将同义词归一化"""
    return synonyms.get(token, token)


def tokenize_text(text: str, stopwords: set, synonyms: dict):
    """分词并处理"""
    tokens = jieba.lcut(text)
    processed = []
    for tok in tokens:
        tok = tok.strip()
        if not tok or len(tok) < 2:  # 过滤单字
            continue
        if tok in stopwords:
            continue
        tok = normalize_token(tok, synonyms)
        processed.append(tok)
    return processed


def is_command_sentence(text: str) -> bool:
    """判断是否为指令句"""
    for cue in COMMAND_CUES:
        if cue in text:
            return True
    stripped = text.strip()
    if stripped.startswith(("去", "给", "把", "让", "叫")):
        return True
    return False


def is_complex_sentence(text: str) -> bool:
    """判断是否为复杂句"""
    return any(marker in text for marker in COMPLEX_CLAUSE_MARKERS)


def compute_features_for_group(df_group: pd.DataFrame,
                               stopwords: set,
                               synonyms: dict) -> dict:
    """
    针对某个角色的全部台词，计算三类指标
    """
    all_text = "。".join(df_group["text"].astype(str).tolist())
    
    tokens = tokenize_text(all_text, stopwords, synonyms)
    total_tokens = len(tokens) if tokens else 1
    
    # --- 1. 词频维度 ---
    token_counter = Counter(tokens)
    keyword_stats = {}
    for group_name, keywords in KEYWORD_GROUPS.items():
        raw_count = sum(token_counter.get(k, 0) for k in keywords)
        per_1000 = raw_count / total_tokens * 1000 if total_tokens > 0 else 0
        keyword_stats[group_name] = {
            "count": int(raw_count),
            "per_1000": round(per_1000, 2)
        }
    
    # --- 2. 句法维度（简化版） ---
    sentences = [s for s in all_text.replace("？", "。").replace("！", "。").split("。") if s.strip()]
    sentence_lengths = [len(s) for s in sentences] if sentences else [0]
    avg_sentence_length = float(np.mean(sentence_lengths)) if sentence_lengths else 0.0
    complex_sentences = [s for s in sentences if is_complex_sentence(s)]
    complex_ratio = len(complex_sentences) / len(sentences) if sentences else 0.0
    
    # --- 3. 互动维度 ---
    total_utterances = len(df_group)
    command_count = 0
    interrupt_count = 0
    
    for _, row in df_group.iterrows():
        text = str(row["text"])
        if is_command_sentence(text):
            command_count += 1
        if "is_interrupt" in row and pd.notna(row["is_interrupt"]) and int(row["is_interrupt"]) == 1:
            interrupt_count += 1
    
    command_ratio = command_count / total_utterances if total_utterances > 0 else 0.0
    
    return {
        "total_tokens": total_tokens,
        "keyword_stats": keyword_stats,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "complex_ratio": round(complex_ratio, 4),
        "command_ratio": round(command_ratio, 4),
        "interrupt_count": interrupt_count,
        "total_utterances": total_utterances,
    }


def main():
    # 1. 读数据
    csv_path = os.path.join(OUTPUT_DIR, "villain_lines.csv")
    if not os.path.exists(csv_path):
        print(f"错误: 找不到数据文件 {csv_path}")
        print("请先运行 extract_pdf.py 提取台词数据")
        return
    
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"读取数据: {len(df)} 条记录")
    
    # 只保留目标反派
    df = df[df["character"].isin(VILLAINS)].copy()
    print(f"筛选后: {len(df)} 条反派台词")
    
    # 2. 加载停用词 & 同义词映射
    stopwords_path = os.path.join(DATA_DIR, "stopwords.txt")
    synonyms_path = os.path.join(DATA_DIR, "synonyms.json")
    stopwords = load_stopwords(stopwords_path)
    synonyms = load_synonyms(synonyms_path)
    
    # 保存同义词表到文件（如果不存在）
    if not os.path.exists(synonyms_path):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(synonyms_path, "w", encoding="utf-8") as f:
            json.dump(synonyms, f, ensure_ascii=False, indent=2)
        print(f"已创建同义词表: {synonyms_path}")
    
    # 3. 按角色分组计算指标
    results = {}
    for villain in VILLAINS:
        group_df = df[df["character"] == villain]
        if group_df.empty:
            print(f"警告: 未找到 {villain} 的台词")
            continue
        print(f"\n正在分析 {villain}...")
        feats = compute_features_for_group(group_df, stopwords, synonyms)
        results[villain] = feats
        print(f"  总词数: {feats['total_tokens']}")
        print(f"  平均句长: {feats['avg_sentence_length']}")
        print(f"  复杂句比例: {feats['complex_ratio']:.2%}")
        print(f"  指令句比例: {feats['command_ratio']:.2%}")
    
    # 4. 汇总成表格
    rows = []
    for villain, feats in results.items():
        row = {"character": villain}
        for group_name, stat in feats["keyword_stats"].items():
            row[f"{group_name}_per_1000"] = stat["per_1000"]
        row["avg_sentence_length"] = feats["avg_sentence_length"]
        row["complex_ratio"] = feats["complex_ratio"]
        row["command_ratio"] = feats["command_ratio"]
        row["interrupt_count"] = feats["interrupt_count"]
        row["total_utterances"] = feats["total_utterances"]
        rows.append(row)
    
    result_df = pd.DataFrame(rows)
    out_path = os.path.join(OUTPUT_DIR, "villain_features.csv")
    result_df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n✓ 已保存角色特征数据表到: {out_path}")
    print("\n数据预览:")
    print(result_df.to_string())
    
    return result_df


if __name__ == "__main__":
    main()

