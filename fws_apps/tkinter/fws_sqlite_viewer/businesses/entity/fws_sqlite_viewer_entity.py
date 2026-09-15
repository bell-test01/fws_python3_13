"""
Summary:
    fws_sqlite_viewer アプリのエンティティモジュール。
Description:
    ビジネスロジック内で保持すべき状態（開いているDBのパスなど）を管理します。
Attachment:
    なし
"""
from typing import Optional
from pathlib import Path

class FwsSqliteViewerEntity:
    """
    Summary:
        状態データを保持するエンティティクラス。
    Description:
        現在開かれているデータベースファイルのパスなどを保持します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            変数を初期化します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.current_db_path: Optional[Path] = None
        """Optional[Path] - 現在接続しているデータベースのパス"""
    #endregion
