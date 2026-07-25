from abc import ABC, abstractmethod


class BaseTTSEngine(ABC):
    @abstractmethod
    def generate(self, text: str, output_path: str, **kwargs) -> str:
        """接收文字並生成音訊檔案,傳回輸出路徑"""
        pass
