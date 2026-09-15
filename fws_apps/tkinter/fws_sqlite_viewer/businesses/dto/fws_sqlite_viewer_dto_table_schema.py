"""
Summary:
    fws_sqlite_viewer アプリのDTOモジュール（テーブルスキーマ用）。
Description:
    テーブルのスキーマ情報を転送するためのオブジェクトを定義します。
Attachment:
    なし
"""
from typing import Any

class FwsSqliteViewerDtoTableSchema:
    """
    Summary:
        テーブルのスキーマ情報（カラム定義など）を保持するDTOクラス。
    Description:
        PRAGMA table_info の結果を格納します。
    """
    #region Constructor
    def __init__(self, cid: int, name: str, type_name: str, notnull: int, dflt_value: Any, pk: int) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            変数を初期化します。
        Args:
            cid: int - カラムID
            name: str - カラム名
            type_name: str - データ型
            notnull: int - NOT NULL制約 (1 なら NOT NULL)
            dflt_value: Any - デフォルト値
            pk: int - プライマリキー (1 以上なら PK)
        Returns:
            None - 戻り値なし。
        """
        self.cid: int = cid
        """int - カラムID"""
        self.name: str = name
        """str - カラム名"""
        self.type_name: str = type_name
        """str - データ型"""
        self.notnull: int = notnull
        """int - NOT NULL制約 (1 なら NOT NULL)"""
        self.dflt_value: Any = dflt_value
        """Any - デフォルト値"""
        self.pk: int = pk
        """int - プライマリキー (1 以上なら PK)"""
    #endregion
