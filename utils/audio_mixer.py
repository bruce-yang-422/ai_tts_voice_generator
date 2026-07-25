import shutil
import subprocess
from pathlib import Path
from typing import List


def merge_audio_segments(segment_paths: List[str], output_path: str) -> str:
    """使用 ffmpeg concat demuxer 合併多個音訊片段為單一檔案"""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("找不到 ffmpeg,請先安裝並加入 PATH 才能合併音檔: https://ffmpeg.org/download.html")

    list_file = Path(output_path).with_suffix(".txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for path in segment_paths:
            f.write(f"file '{Path(path).resolve().as_posix()}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", output_path],
        check=True,
        capture_output=True,
    )

    list_file.unlink()
    return output_path
