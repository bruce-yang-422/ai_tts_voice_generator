import asyncio
import sys

import edge_tts

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

REGION_MAP = {
    "zh-TW": "台灣",
    "zh-HK": "香港",
    "zh-CN": "中國",
    "zh-CN-liaoning": "中國(遼寧)",
    "zh-CN-shaanxi": "中國(陝西)",
}

VOICE_MAP = {
    # 台灣繁體中文
    "zh-TW-HsiaoYuNeural": {"name": "曉雨", "gender": "女", "desc": "自然起伏、情感豐富(推薦 Podcast / 故事)"},
    "zh-TW-YunJheNeural": {"name": "允哲", "gender": "男", "desc": "沉穩專業、廣播感(推薦 Podcast / 新聞)"},
    "zh-TW-HsiaoChenNeural": {"name": "蕭晨", "gender": "女", "desc": "傳統朗讀、標準清晰"},

    # 香港粵語
    "zh-HK-HiuGaaiNeural": {"name": "曉佳", "gender": "女", "desc": "香港粵語女聲"},
    "zh-HK-HiuMaanNeural": {"name": "曉曼", "gender": "女", "desc": "香港粵語女聲"},
    "zh-HK-WanLungNeural": {"name": "雲龍", "gender": "男", "desc": "香港粵語男聲"},

    # 大陸普通話與方言
    "zh-CN-XiaoxiaoNeural": {"name": "曉曉", "gender": "女", "desc": "多語氣、活潑廣泛"},
    "zh-CN-XiaoyiNeural": {"name": "曉伊", "gender": "女", "desc": "溫柔平緩"},
    "zh-CN-YunjianNeural": {"name": "雲健", "gender": "男", "desc": "影視解說、影評感"},
    "zh-CN-YunxiNeural": {"name": "雲希", "gender": "男", "desc": "熱門有聲書、戲劇情感"},
    "zh-CN-YunxiaNeural": {"name": "雲夏", "gender": "男", "desc": "少年感、輕鬆陽光"},
    "zh-CN-YunyangNeural": {"name": "雲揚", "gender": "男", "desc": "專業新聞播報、嚴肅大氣"},
    "zh-CN-liaoning-XiaobeiNeural": {"name": "曉北", "gender": "女", "desc": "東北方言口音"},
    "zh-CN-shaanxi-XiaoniNeural": {"name": "曉妮", "gender": "女", "desc": "陝西方言口音"},
}


async def list_voices_formatted():
    voices = await edge_tts.list_voices()

    print(f"\n{'系統 ID':<30} | {'中文名':<6} | {'性別':<4} | {'地區':<10} | {'特色說明'}")
    print("-" * 90)

    for v in voices:
        short_name = v["ShortName"]
        if short_name in VOICE_MAP:
            info = VOICE_MAP[short_name]
            region = REGION_MAP.get(v["Locale"], v["Locale"])
            print(f"{short_name:<30} | {info['name']:<6} | {info['gender']:<4} | {region:<10} | {info['desc']}")


if __name__ == "__main__":
    asyncio.run(list_voices_formatted())
