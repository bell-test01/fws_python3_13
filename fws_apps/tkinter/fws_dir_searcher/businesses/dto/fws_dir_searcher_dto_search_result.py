"""
Summary:
    fws_dir_searcher アプリの検索結果DTO。
Description:
    ディレクトリ検索のヒット結果、およびそのディレクトリ内のファイル情報を保持するデータ転送オブジェクトです。
Attachment:
    なし
"""
from typing import List
from dataclasses import dataclass, field

@dataclass
class FwsDirSearcherDtoFileInfo:
    """
    Summary:
        ファイル情報を格納するDTO。
    """
    name: str
    ext: str
    size_bytes: int
    modified_time: str
    absolute_path: str

@dataclass
class FwsDirSearcherDtoDirInfo:
    """
    Summary:
        検索にヒットしたディレクトリ情報と、その直下のファイル情報を格納するDTO。
    """
    dir_name: str
    absolute_path: str
    files: List[FwsDirSearcherDtoFileInfo] = field(default_factory=list)

@dataclass
class FwsDirSearcherDtoSearchResult:
    """
    Summary:
        検索全体の実行結果を格納するDTO。
    """
    is_success: bool
    error_message: str
    directories: List[FwsDirSearcherDtoDirInfo] = field(default_factory=list)
    execution_time_ms: float = 0.0
