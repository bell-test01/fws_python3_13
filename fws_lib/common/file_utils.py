"""
Summary:
    fws_lib 共通のファイルシステムユーティリティ。
Description:
    ファイルやディレクトリの操作に関する便利なラッパー関数を提供します。
"""
import os
from pathlib import Path
from typing import Union
from fws_lib.core.fws_lib_const import FwsLibConst

class FileUtils:
    """
    Summary:
        ファイルシステム操作のユーティリティクラス。
    """

    @staticmethod
    def ensure_dir(path: Union[str, Path]) -> None:
        """
        Summary:
            指定されたディレクトリが存在しない場合、作成します。
        Args:
            path (Union[str, Path]): 対象のディレクトリパス。
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def read_text(path: Union[str, Path], encoding: str = FwsLibConst.DEFAULT_ENCODING) -> str:
        """
        Summary:
            テキストファイルを読み込みます。
        Args:
            path (Union[str, Path]): 対象のファイルパス。
            encoding (str): エンコーディング (デフォルト: UTF-8)
        Returns:
            str: 読み込んだファイルの内容。
        """
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"{FwsLibConst.ERROR_PREFIX} File not found: {path}")
        return p.read_text(encoding=encoding)

    @staticmethod
    def write_text(path: Union[str, Path], content: str, encoding: str = FwsLibConst.DEFAULT_ENCODING) -> None:
        """
        Summary:
            テキストファイルに内容を書き込みます。
            親ディレクトリが存在しない場合は自動作成します。
        Args:
            path (Union[str, Path]): 対象のファイルパス。
            content (str): 書き込む内容。
            encoding (str): エンコーディング (デフォルト: UTF-8)
        """
        p = Path(path)
        FileUtils.ensure_dir(p.parent)
        p.write_text(content, encoding=encoding)
