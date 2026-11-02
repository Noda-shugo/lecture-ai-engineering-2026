"""第2回 宿題（発展）: 用語集から SFT 用の Q&A データ（JSONL）を作る。

使い方:
    uv run python scripts/make_sft_dataset.py > glossary_sft.jsonl

できたファイルを Colab にアップロードし、LoRA 学習のデータとして使う。
質問の言い回しを増やす、別名でも質問を作る、検証用に一部を分ける、などを工夫してみよう。
"""

import json
import sys
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent.parent / "data" / "glossary.json"
# 通常の質問テンプレート
TEMPLATES = [
    "「{term}」とは何ですか？",
    "{term}について簡単に説明してください。",
    "{term}の意味を教えて。"
]

# categoryを文脈として与えるテンプレート
CATEGORY_TEMPLATES = [
    "{category}に関する用語「{term}」について教えてください。",
    "講座の{category}で出てくる「{term}」とはどういう意味ですか？"
]

def main() -> None:
    terms = json.loads(GLOSSARY.read_text(encoding="utf-8"))["terms"]
    
    for t in terms:
        #質問の対象とする単語リスト
        target_words = [t["term"]] + t.get("aliases", [])
        
        category = t.get("category", "")
        related = t.get("related", [])
        
        #回答文の作成
        answer_text = t["definition"]
        if related:
            answer_text += f"\n\nあわせて確認したい関連用語: {', '.join(related)}"
            
        #組み合わせの全パターンを生成
        for word in target_words:
            #通常パターン
            for template in TEMPLATES:
                record = {
                    "messages": [
                        {"role": "user", "content": template.format(term=word)},
                        {"role": "assistant", "content": answer_text},
                    ]
                }
                sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")
                
            #カテゴリ付きパターン
            if category:
                for template in CATEGORY_TEMPLATES:
                    record = {
                        "messages": [
                            {"role": "user", "content": template.format(term=word, category=category)},
                            {"role": "assistant", "content": answer_text},
                        ]
                    }
                    sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")
if __name__ == "__main__":
    main()
