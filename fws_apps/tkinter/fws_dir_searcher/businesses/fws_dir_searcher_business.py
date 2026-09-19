"""
Summary:
    fws_dir_searcher アプリのビジネスロジック。
Description:
    ディレクトリの再帰的走査、曖昧検索、およびファイル情報の取得を行います。
Attachment:
    なし
"""
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List

from fws_apps.tkinter.fws_dir_searcher.businesses.dto.fws_dir_searcher_dto_search_result import (
    FwsDirSearcherDtoSearchResult,
    FwsDirSearcherDtoDirInfo,
    FwsDirSearcherDtoFileInfo
)

class FwsDirSearcherBusiness:
    """
    Summary:
        検索処理を担うビジネスクラス。
    """

    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        """
        pass

    def search_directories(self, root_path: str, keyword: str) -> FwsDirSearcherDtoSearchResult:
        """
        Summary:
            指定されたルートディレクトリ以下を検索し、キーワードに部分一致するディレクトリを取得します。
        Description:
            ヒットしたディレクトリの直下にあるファイル情報も併せて取得します。
        Args:
            root_path: str - 検索を開始するルートディレクトリのパス。
            keyword: str - 検索キーワード（大文字小文字を区別しない）。
        Returns:
            FwsDirSearcherDtoSearchResult - 検索結果DTO。
        """
        start_time = time.time()
        result = FwsDirSearcherDtoSearchResult(is_success=False, error_message="", directories=[])

        root_dir = Path(root_path)
        if not root_dir.exists() or not root_dir.is_dir():
            result.error_message = f"Invalid root directory: {root_path}"
            return result

        keyword_lower = keyword.lower()
        matched_dirs = []

        try:
            for current_dir, dirs, files in os.walk(root_dir):
                current_path = Path(current_dir)
                dir_name = current_path.name
                
                # ルートディレクトリ自身は検索ヒットから除外するか？
                # 今回は除外せず、名前が一致すればヒットとする
                if keyword_lower in dir_name.lower():
                    dir_info = FwsDirSearcherDtoDirInfo(
                        dir_name=dir_name,
                        absolute_path=str(current_path),
                        files=self._get_file_infos(current_path)
                    )
                    matched_dirs.append(dir_info)
            
            result.directories = matched_dirs
            result.is_success = True
        except Exception as e:
            result.error_message = f"Error during search: {e}"

        result.execution_time_ms = (time.time() - start_time) * 1000
        return result

    def _get_file_infos(self, dir_path: Path) -> List[FwsDirSearcherDtoFileInfo]:
        """
        Summary:
            指定ディレクトリ直下のファイル情報を取得します。
        Args:
            dir_path: Path - ディレクトリのパス。
        Returns:
            List[FwsDirSearcherDtoFileInfo] - ファイル情報のリスト。
        """
        file_infos = []
        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    stat = item.stat()
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    file_info = FwsDirSearcherDtoFileInfo(
                        name=item.name,
                        ext=item.suffix,
                        size_bytes=stat.st_size,
                        modified_time=mod_time,
                        absolute_path=str(item)
                    )
                    file_infos.append(file_info)
        except Exception as e:
            # 権限エラー等はスキップ
            pass
        return file_infos
