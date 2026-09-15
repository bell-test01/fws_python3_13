"""
Summary:
    fws_lib 共通の設定（Config）および履歴管理クラス。
Description:
    JSON などの形式で設定データや履歴データをシリアライズ/デシリアライズします。
"""
import json
from pathlib import Path
from typing import Dict, Any, Union
from fws_lib.core.fws_lib_const import FwsLibConst
from fws_lib.common.file_utils import FileUtils

class ConfigManager:
    """
    Summary:
        設定・履歴管理ユーティリティクラス。
    """

    @staticmethod
    def load_json(path: Union[str, Path]) -> Dict[str, Any]:
        """
        Summary:
            JSON ファイルを読み込み、辞書として返します。
        Args:
            path (Union[str, Path]): 対象のファイルパス。
        Returns:
            Dict[str, Any]: パースされた JSON データ。ファイルが存在しない場合は空の辞書。
        """
        p = Path(path)
        if not p.exists():
            return {}
        
        try:
            content = FileUtils.read_text(p)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"{FwsLibConst.ERROR_PREFIX} Failed to parse JSON at {path}: {e}")

    @staticmethod
    def save_json(path: Union[str, Path], data: Dict[str, Any], indent: int = 4) -> None:
        """
        Summary:
            辞書データを JSON ファイルとして保存します。
        Args:
            path (Union[str, Path]): 保存先のファイルパス。
            data (Dict[str, Any]): 保存するデータ。
            indent (int): JSON のインデント (デフォルト: 4)。
        """
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        FileUtils.write_text(path, content)
