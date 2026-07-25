import asyncio

import edge_tts

from engines.base import BaseTTSEngine


class EdgeTTSEngine(BaseTTSEngine):
    """免 GPU、免下載模型,適合先跑通整個 pipeline 再考慮換成本地模型引擎"""

    def __init__(self, default_voice: str = "zh-TW-HsiaoYuNeural", default_rate: str = "+25%"):
        self.default_voice = default_voice
        self.default_rate = default_rate

    def generate(self, text: str, output_path: str, voice: str = None, rate: str = None, **kwargs) -> str:
        asyncio.run(self._generate(text, output_path, voice or self.default_voice, rate or self.default_rate))
        return output_path

    @staticmethod
    async def _generate(text: str, output_path: str, voice: str, rate: str) -> None:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)
