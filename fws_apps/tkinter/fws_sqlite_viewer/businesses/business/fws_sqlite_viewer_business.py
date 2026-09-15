"""
Summary:
    fws_sqlite_viewer アプリのビジネスロジックモジュール。
Description:
    SQLiteデータベースへの接続およびクエリ実行、スキーマ取得を行います。
Attachment:
    なし
"""
import sqlite3
import time
from typing import List, Optional
from pathlib import Path
from fws_apps.tkinter.fws_sqlite_viewer.businesses.entity import fws_sqlite_viewer_entity
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_query_result
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_table_schema

class FwsSqliteViewerBusiness:
    """
    Summary:
        データベース操作を担うビジネスロジッククラス。
    Description:
        DBの開閉、テーブル一覧取得、スキーマ取得、SQL実行処理を提供します。
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
        self.fws_sqlite_viewer_entity_obj: fws_sqlite_viewer_entity.FwsSqliteViewerEntity = fws_sqlite_viewer_entity.FwsSqliteViewerEntity()
        """fws_sqlite_viewer_entity.FwsSqliteViewerEntity - エンティティ"""
        
        self.connection: Optional[sqlite3.Connection] = None
        """Optional[sqlite3.Connection] - SQLiteコネクション"""
    #endregion

    #region Public Methods
    def connect(self, db_path: str) -> None:
        """
        Summary:
            指定されたパスのSQLiteデータベースに接続します。
        Description:
            既に接続がある場合は閉じ、新しい接続を開きます。
        Args:
            db_path: str - データベースファイルのパス文字列。
        Returns:
            None - 戻り値なし。
        """
        self.close()
        # パスが存在しなくても新規作成を避ける場合は os.path.exists などでチェックが必要ですが
        # sqlite3はデフォルトで新規作成してしまうため、アプリ側での事前チェックを想定します。
        # 今回の要件（Viewer）として、指定されたパスに接続します。
        self.connection = sqlite3.connect(db_path)
        self.fws_sqlite_viewer_entity_obj.current_db_path = Path(db_path)

    def close(self) -> None:
        """
        Summary:
            データベース接続を閉じます。
        Description:
            コネクションが存在する場合、クローズ処理を行います。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.connection:
            self.connection.close()
            self.connection = None
        self.fws_sqlite_viewer_entity_obj.current_db_path = None

    def get_tables(self) -> List[str]:
        """
        Summary:
            データベース内のテーブル一覧を取得します。
        Description:
            sqlite_masterからtype='table'のnameを抽出して返します。
        Args:
            なし
        Returns:
            List[str] - テーブル名のリスト。
        """
        if not self.connection:
            return []
            
        cursor: sqlite3.Cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()

    def get_table_schema(self, table_name: str) -> List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema]:
        """
        Summary:
            指定されたテーブルのスキーマ情報を取得します。
        Description:
            PRAGMA table_info() を使用してカラム定義等を取得します。
        Args:
            table_name: str - スキーマを取得するテーブル名。
        Returns:
            List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema] - スキーマDTOのリスト。
        """
        if not self.connection:
            return []
            
        cursor: sqlite3.Cursor = self.connection.cursor()
        try:
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            rows = cursor.fetchall()
            schema_list: List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema] = []
            for row in rows:
                dto = fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema(
                    cid=row[0],
                    name=row[1],
                    type_name=row[2],
                    notnull=row[3],
                    dflt_value=row[4],
                    pk=row[5]
                )
                schema_list.append(dto)
            return schema_list
        finally:
            cursor.close()

    def _split_queries(self, sql_script: str) -> List[str]:
        """
        Summary:
            クエリ文字列をセミコロンで分割します。
        Description:
            シングルクォーテーション('')またはダブルクォーテーション("")に囲まれた
            セミコロンは区切り文字として扱いません。
        Args:
            sql_script: str - 分割するSQL文字列全体。
        Returns:
            List[str] - 分割された個別のSQL文のリスト。空文字は除外します。
        """
        queries = []
        current_query = []
        in_single_quote = False
        in_double_quote = False
        
        for char in sql_script:
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                current_query.append(char)
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                current_query.append(char)
            elif char == ';' and not in_single_quote and not in_double_quote:
                queries.append("".join(current_query).strip())
                current_query = []
            else:
                current_query.append(char)
                
        # 最後のセミコロンがない場合のクエリを追加
        if current_query:
            last_query = "".join(current_query).strip()
            if last_query:
                queries.append(last_query)
                
        # 空のクエリを除外して返す
        return [q for q in queries if q]

    def execute_query(self, sql_query: str) -> fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult:
        """
        Summary:
            任意のSQLクエリ（複数クエリ対応）を実行します。
        Description:
            セミコロン区切りの複数クエリを順番に実行します。
            最後に実行されたSELECT系の結果行、およびすべてのクエリの実行履歴（件数）を返します。
            エラー発生時は全体をロールバックしてメッセージを返します。
        Args:
            sql_query: str - 実行するSQL文。
        Returns:
            fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult - 実行結果を格納したDTO。
        """
        result_dto: fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult = fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult()
        
        if not self.connection:
            result_dto.error_message = "Not connected to a database."
            return result_dto
            
        queries = self._split_queries(sql_query)
        if not queries:
            result_dto.error_message = "Query is empty."
            return result_dto

        start_time: float = time.perf_counter()
        cursor: sqlite3.Cursor = self.connection.cursor()
        
        last_columns = []
        last_rows = []
        has_select_result = False

        try:
            for q in queries:
                cursor.execute(q)
                
                # SELECT文の場合はデータが存在する
                if cursor.description:
                    last_columns = [description[0] for description in cursor.description]
                    last_rows = cursor.fetchall()
                    has_select_result = True
                    result_dto.execution_history.append((q, len(last_rows)))
                else:
                    # INSERT, UPDATE, DELETE などの場合は変更行数を取得
                    rowcount = cursor.rowcount
                    result_dto.execution_history.append((q, rowcount))
            
            # すべて成功した場合のみコミット（トランザクション制御されていない場合を想定）
            self.connection.commit()
            
            if has_select_result:
                result_dto.columns = last_columns
                result_dto.rows = last_rows
                result_dto.rowcount = len(last_rows)
            else:
                # 最後のクエリのrowcount、または更新系の合計値を設定
                # （ただし詳細履歴は execution_history にあるため、ここでは最後のrowcountを代表としてセット）
                result_dto.rowcount = cursor.rowcount
                
        except sqlite3.Error as e:
            result_dto.error_message = str(e)
            if self.connection:
                self.connection.rollback()
        finally:
            cursor.close()
            
        end_time: float = time.perf_counter()
        result_dto.execution_time_ms = (end_time - start_time) * 1000.0
        
        return result_dto
    #endregion
