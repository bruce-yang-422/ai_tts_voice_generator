# AI TTS Voice Generator

以 Microsoft Edge TTS 將 UTF-8 文字稿轉為 MP3 的命令列工具。它會依句子切分長文、分段生成音訊，並透過 `ffmpeg` 合併為單一 `final.mp3`。目前內建台灣、香港與中國中文語音，並以可擴充的引擎介面設計。

## 需求

- Python 3.7 以上（本專案目前以 Python 3.11 驗證）
- 網際網路連線：Edge TTS 會呼叫 Microsoft 的線上語音服務
- `ffmpeg` 已安裝且可由 `PATH` 呼叫：用於合併分段 MP3

## 安裝

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux：

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

確認 `ffmpeg` 可用：

```bash
ffmpeg -version
```

## 快速開始

將純文字稿存為 UTF-8 編碼的 `input/script.txt`，再執行：

```bash
python main.py
```

工具會將文字依句子切分（每段最多約 80 個字元），輸出各段 `segment_XXX.mp3`，最後在 `output/final.mp3` 產生合併音檔。

## 指令選項

```bash
python main.py [--project 專案名稱 | --input 文稿路徑] [--output-dir 輸出資料夾] \
  [--voice 語音 ID] [--rate 語速]
```

| 選項 | 說明 |
| --- | --- |
| `--project` | 使用 `input/<專案名稱>/` 中的文字稿，並預設輸出至 `output/<專案名稱>/`。 |
| `--input` | 指定文字稿路徑；未指定專案時預設為 `input/script.txt`。 |
| `--output-dir` | 指定輸出資料夾。 |
| `--voice` | 指定 Edge TTS 語音 ID；預設為 `zh-TW-HsiaoYuNeural`。 |
| `--rate` | 指定語速，例如 `+15%`；未指定時預設為 `+25%`。 |

例如，使用台灣男聲並提高語速：

```bash
python main.py --voice zh-TW-YunJheNeural --rate +15%
```

## 專案資料夾模式

適合將每個 Podcast 或配音工作獨立管理：

```text
input/
└── 台灣家庭食用油/
    ├── script.txt                         # 實際送入 TTS 的純文字稿
    └── 台灣家庭食用油全解析_podcast講稿.md # 來源講稿或備查資料
```

```bash
python main.py --project 台灣家庭食用油 --voice zh-TW-YunJheNeural --rate +5%
```

專案模式會優先讀取 `input/<專案名稱>/script.txt`；若該檔案不存在，會改用資料夾內依名稱排序的第一個 `.txt` 檔。輸出位置預設為 `output/<專案名稱>/`。

## 查看語音

```bash
python list_voices.py
```

此指令會查詢 Edge TTS，並列出程式預先整理的中文語音 ID、中文名稱、性別、地區與建議用途。常用台灣語音如下：

| 語音 ID | 名稱 | 適用情境 |
| --- | --- | --- |
| `zh-TW-HsiaoYuNeural` | 曉雨（女） | Podcast、故事；預設語音 |
| `zh-TW-YunJheNeural` | 允哲（男） | Podcast、新聞 |
| `zh-TW-HsiaoChenNeural` | 蕭晨（女） | 清晰的傳統朗讀 |

## 專案結構

```text
.
├── main.py                 # CLI 入口：讀稿、切段、生成與合併
├── list_voices.py          # 列出整理過的中文 Edge TTS 語音
├── engines/
│   ├── base.py             # TTS 引擎抽象介面
│   └── edge_engine.py      # Edge TTS 實作
├── utils/
│   ├── text_processor.py   # 文字切段
│   └── audio_mixer.py      # 以 ffmpeg 合併音訊
├── input/                  # 文字稿與各專案來源資料
└── output/                 # 生成的 MP3（已由 Git 忽略）
```

## 擴充 TTS 引擎

在 `engines/` 新增繼承 `BaseTTSEngine` 的類別，並實作：

```python
def generate(self, text: str, output_path: str, **kwargs) -> str:
    ...
```

再於呼叫端替換 `EdgeTTSEngine` 即可整合其他 TTS 服務或本地模型。

## 注意事項

- Edge TTS 是雲端服務；生成或查詢語音時都需要可用網路。
- 合併流程使用 `ffmpeg -c copy`，不重新編碼 MP3，因此速度快；若系統找不到 `ffmpeg`，程式會顯示安裝提示。
- 產生的音檔與 Python 暫存檔均已在 `.gitignore` 排除。
