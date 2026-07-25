import argparse
import glob
import os
import sys

from engines.edge_engine import EdgeTTSEngine
from utils.audio_mixer import merge_audio_segments
from utils.text_processor import split_text_for_tts

if sys.platform == "win32":
    # Windows 主控台常用非 UTF-8 編碼(如 Big5/cp950),中文字元 print() 時容易亂碼或崩潰
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

DEFAULT_INPUT = "input/script.txt"


def resolve_project_input(project: str) -> str:
    project_dir = os.path.join("input", project)
    if not os.path.isdir(project_dir):
        raise FileNotFoundError(f"找不到專案資料夾: {project_dir}")

    default_script = os.path.join(project_dir, "script.txt")
    if os.path.exists(default_script):
        return default_script

    txt_files = sorted(glob.glob(os.path.join(project_dir, "*.txt")))
    if not txt_files:
        raise FileNotFoundError(f"{project_dir} 裡沒有找到任何 .txt 文稿檔案")
    return txt_files[0]


def main():
    parser = argparse.ArgumentParser(description="AI TTS Voice Generator")
    parser.add_argument("--project", default=None, help="專案名稱,對應 input/<專案名>/ 與 output/<專案名>/")
    parser.add_argument("--input", default=None, help=f"文稿檔案路徑 (預設: {DEFAULT_INPUT},與 --project 二擇一)")
    parser.add_argument("--voice", default=None, help="語音角色,可用 python list_voices.py 查詢清單 (預設: zh-TW-HsiaoYuNeural)")
    parser.add_argument("--rate", default=None, help="語速調整,如 +15%% (預設: +0%%)")
    parser.add_argument("--output-dir", default=None, help="輸出目錄 (預設: output,若指定 --project 則預設 output/<專案名>)")
    args = parser.parse_args()

    if args.project:
        input_path = resolve_project_input(args.project)
        output_dir = args.output_dir or os.path.join("output", args.project)
    else:
        input_path = args.input or DEFAULT_INPUT
        output_dir = args.output_dir or "output"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到文稿檔案: {input_path}\n請把文字稿放到這個路徑,或用 --input 指定其他路徑")

    with open(input_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    os.makedirs(output_dir, exist_ok=True)

    chunks = split_text_for_tts(input_text)
    print(f"文本已切分為 {len(chunks)} 個段落進行處理...")

    engine = EdgeTTSEngine(default_voice=args.voice) if args.voice else EdgeTTSEngine()

    segment_paths = []
    for idx, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f"segment_{idx:03d}.mp3")
        print(f"正在生成第 {idx + 1}/{len(chunks)} 段: {chunk[:15]}...")
        engine.generate(chunk, output_path, rate=args.rate)
        segment_paths.append(output_path)

    final_path = os.path.join(output_dir, "final.mp3")
    print("正在合併音訊段落...")
    merge_audio_segments(segment_paths, final_path)

    print(f"\n全部語音生成完成！合併後音檔: {final_path}")


if __name__ == "__main__":
    main()
