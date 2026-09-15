"""
Summary:
    fws_sqlite_viewer アプリのロジックモジュール。
Description:
    画面表示に関連する制御や値の変換処理を配置します。
Attachment:
    なし
"""
from typing import List, Dict
from fws_apps.tkinter.fws_sqlite_viewer.businesses.business import fws_sqlite_viewer_business
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_query_result
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_table_schema

class FwsSqliteViewerLogic:
    """
    Summary:
        ビューアーのロジッククラス。
    Description:
        ビジネスロジックを呼び出し、結果を返します。UIコンポーネント(View)には依存しません。
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
        self.fws_sqlite_viewer_business_obj: fws_sqlite_viewer_business.FwsSqliteViewerBusiness = fws_sqlite_viewer_business.FwsSqliteViewerBusiness()
        """fws_sqlite_viewer_business.FwsSqliteViewerBusiness - ビジネスロジックオブジェクト"""
    #endregion

    #region Public Methods
    def load_db(self, db_path: str) -> Dict[str, List[str]]:
        """
        Summary:
            DBに接続し、テーブル一覧を取得します。
        Args:
            db_path: str - DBファイルパス。
        Returns:
            Dict[str, List[str]] - テーブル名の辞書。
        """
        self.fws_sqlite_viewer_business_obj.connect(db_path)
        return self.fws_sqlite_viewer_business_obj.get_tables()

    def run_query(self, sql: str) -> fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult:
        """
        Summary:
            入力されたSQLを実行し、結果を返します。
        Args:
            sql: str - 実行するSQL文字列。
        Returns:
            fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult - 実行結果DTO。
        """
        return self.fws_sqlite_viewer_business_obj.execute_query(sql)

    def read_table_schema(self, table_name: str, alias: str = "main") -> List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema]:
        """
        Summary:
            選択されたテーブルのスキーマを取得します。
        Args:
            table_name: str - テーブル名。
            alias: str - データベースエイリアス。
        Returns:
            List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema] - スキーマDTOのリスト。
        """
        return self.fws_sqlite_viewer_business_obj.get_table_schema(table_name, alias)

    def close_db(self) -> None:
        """
        Summary:
            DB接続をクローズします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_business_obj.close()

    def get_tables(self) -> Dict[str, List[str]]:
        """
        Summary:
            現在のデータベースのテーブル一覧を再取得します。
        Args:
            なし
        Returns:
            Dict[str, List[str]] - テーブル名の辞書。
        """
        return self.fws_sqlite_viewer_business_obj.get_tables()

    def attach_db(self, db_path: str, alias: str) -> None:
        """
        Summary:
            追加のDBをアタッチします。
        Args:
            db_path: str - DBファイルパス
            alias: str - エイリアス
        """
        self.fws_sqlite_viewer_business_obj.attach_db(db_path, alias)

    def detach_db(self, alias: str) -> None:
        """
        Summary:
            アタッチされたDBをデタッチします。
        Args:
            alias: str - エイリアス
        """
        self.fws_sqlite_viewer_business_obj.detach_db(alias)
    #endregion
