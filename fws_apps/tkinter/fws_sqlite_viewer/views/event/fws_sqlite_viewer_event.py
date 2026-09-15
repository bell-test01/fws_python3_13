"""
Summary:
    fws_sqlite_viewer アプリのイベントモジュール。
Description:
    各UIのイベントバインドおよび処理の呼び出しを行います。
ScreenName:
    SQLite Viewer メイン画面
Attachment:
    なし
"""
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import List

from fws_apps.tkinter.fws_sqlite_viewer.views.view import fws_sqlite_viewer_view
from fws_apps.tkinter.fws_sqlite_viewer.views.logic import fws_sqlite_viewer_logic
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_query_result
from fws_apps.tkinter.fws_sqlite_viewer.businesses.dto import fws_sqlite_viewer_dto_table_schema


class FwsSqliteViewerEvent:
    """
    Summary:
        イベントハンドラクラス。
    Description:
        各クラスをインスタンス化し、イベントをバインドします。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各クラスを生成し、イベントを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_view_obj: fws_sqlite_viewer_view.FwsSqliteViewerView = fws_sqlite_viewer_view.FwsSqliteViewerView()
        """fws_sqlite_viewer_view.FwsSqliteViewerView - ビューオブジェクト"""
        
        self.fws_sqlite_viewer_logic_obj: fws_sqlite_viewer_logic.FwsSqliteViewerLogic = fws_sqlite_viewer_logic.FwsSqliteViewerLogic()
        """fws_sqlite_viewer_logic.FwsSqliteViewerLogic - ロジックオブジェクト"""

        self._bind_events()

    def _bind_events(self) -> None:
        """
        Summary:
            UIイベントをバインドします。
        Description:
            ボタンクリックやツリー選択などを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_view_obj.btn_open_db.config(command=self.btn_open_db_click)
        self.fws_sqlite_viewer_view_obj.btn_run_query.config(command=self.btn_run_query_click)
        self.fws_sqlite_viewer_view_obj.trv_tables.bind("<<TreeviewSelect>>", self.trv_tables_select)
        
        # テキスト入力欄でEnterキーを押した際にもDBを読み込む
        self.fws_sqlite_viewer_view_obj.ent_db_path.bind("<Return>", self.ent_db_path_return)
        
        # クリップボードコピー
        self.fws_sqlite_viewer_view_obj.trv_schema.bind("<Control-c>", self.copy_schema_to_clipboard)
        self.fws_sqlite_viewer_view_obj.trv_results.bind("<Control-c>", self.copy_results_to_clipboard)
        
        # ダブルクリックでセル単体・テーブル名コピー
        self.fws_sqlite_viewer_view_obj.trv_tables.bind("<Double-1>", self.copy_table_name_to_clipboard)
        self.fws_sqlite_viewer_view_obj.trv_schema.bind("<Double-1>", self.copy_schema_cell_to_clipboard)
        self.fws_sqlite_viewer_view_obj.trv_results.bind("<Double-1>", self.copy_results_cell_to_clipboard)
        
        # SQLエディタのオートインデントとショートカット
        self.fws_sqlite_viewer_view_obj.txt_sql.bind("<Return>", self.txt_sql_return)
        self.fws_sqlite_viewer_view_obj.txt_sql.bind("<Alt-x>", self.btn_run_query_click)
        
        self.fws_sqlite_viewer_view_obj.protocol("WM_DELETE_WINDOW", self.win_main_close)
    #endregion

    #region Public Methods
    def btn_open_db_click(self) -> None:
        """
        Summary:
            Open DBボタンクリック時の処理。
        Description:
            ファイルダイアログを開き、選択されたDBのパスを入力欄にセットして読み込みます。
        UserAction:
            「Open DB」ボタンをクリック - ファイルダイアログが開き、選択したDBを読み込む。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        file_path = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[("SQLite DB", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
        )
        if file_path:
            self._load_db(file_path)

    def ent_db_path_return(self, event: tk.Event) -> None:
        """
        Summary:
            テキスト入力欄でのEnterキー押下時の処理。
        Description:
            入力されているパス文字列を取得し、DBを読み込みます。
        UserAction:
            DB Path の入力欄でEnterキーを押下 - 入力されたパスのDBを読み込む。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        db_path = self._get_db_path()
        if db_path and Path(db_path).exists():
            self._load_db(db_path)
        else:
            self._set_status("Error: Invalid database path.", is_error=True)

    def txt_sql_return(self, event: tk.Event) -> str:
        """
        Summary:
            SQLエディタでEnterキーを押した際のオートインデント処理。
        Description:
            前の行の先頭の空白（スペース・タブ）を引き継いで改行します。
        UserAction:
            SQLエディタ内でEnterキーを押下 - 前の行のインデントを引き継いで改行される。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            str - デフォルトの改行イベントをキャンセルするため "break" を返す。
        """
        current_line = event.widget.get("insert linestart", "insert lineend")
        leading_whitespace = ""
        for char in current_line:
            if char in (' ', '\t'):
                leading_whitespace += char
            else:
                break
        
        event.widget.insert("insert", "\n" + leading_whitespace)
        return "break"

    def btn_run_query_click(self, event: tk.Event = None) -> None:
        """
        Summary:
            Run Queryボタンクリック（またはAlt+X）時の処理。
        Description:
            入力されたSQLを実行し、結果をビューに反映します。
        UserAction:
            「Run Query」ボタンをクリックするかAlt+Xを押下 - 入力されたSQLを実行し結果を表示する。
        Args:
            event: tk.Event - イベントオブジェクト（省略可）
        Returns:
            None - 戻り値なし。
        """
        sql = self._get_sql_query()
        if not sql:
            self._set_status("Error: Query is empty.", is_error=True)
            return
            
        result_dto = self.fws_sqlite_viewer_logic_obj.run_query(sql)
        self._update_results(result_dto)

    def trv_tables_select(self, event: tk.Event) -> None:
        """
        Summary:
            テーブル一覧でアイテムが選択された時の処理。
        Description:
            選択されたテーブルのスキーマを表示し、SELECT * クエリをセットして実行します。
        UserAction:
            テーブル一覧のテーブル名を選択 - そのテーブルのスキーマを表示し、全件取得クエリを準備する。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        trv = self.fws_sqlite_viewer_view_obj.trv_tables
        selection = trv.selection()
        if not selection:
            return
            
        item_id = selection[0]
        table_name = trv.item(item_id, "text")
        
        # スキーマ表示
        try:
            schema_list = self.fws_sqlite_viewer_logic_obj.read_table_schema(table_name)
            self._update_schema_list(schema_list)
        except Exception as e:
            self._set_status(f"Error reading table: {e}", is_error=True)

    def copy_schema_to_clipboard(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細の選択行をコピーします。
        UserAction:
            スキーマ詳細リストでCtrl+Cを押下 - 選択行のデータがクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_treeview_selection(self.fws_sqlite_viewer_view_obj.trv_schema)

    def copy_results_to_clipboard(self, event: tk.Event) -> None:
        """
        Summary:
            クエリ結果の選択行をコピーします。
        UserAction:
            クエリ結果リストでCtrl+Cを押下 - 選択行のデータがクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_treeview_selection(self.fws_sqlite_viewer_view_obj.trv_results)

    def copy_schema_cell_to_clipboard(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細のセルをコピーします。
        UserAction:
            スキーマ詳細リストのセルをダブルクリック - セルの値がクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_cell_value(self.fws_sqlite_viewer_view_obj.trv_schema, event)

    def copy_results_cell_to_clipboard(self, event: tk.Event) -> None:
        """
        Summary:
            クエリ結果のセルをコピーします。
        UserAction:
            クエリ結果リストのセルをダブルクリック - セルの値がクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_cell_value(self.fws_sqlite_viewer_view_obj.trv_results, event)

    def copy_table_name_to_clipboard(self, event: tk.Event) -> None:
        """
        Summary:
            ダブルクリックされたテーブル名をクリップボードにコピーします。
        UserAction:
            テーブル一覧のテーブル名をダブルクリック - テーブル名がクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        trv = self.fws_sqlite_viewer_view_obj.trv_tables
        item = trv.identify_row(event.y)
        if item:
            table_name = trv.item(item, "text")
            self.fws_sqlite_viewer_view_obj.clipboard_clear()
            self.fws_sqlite_viewer_view_obj.clipboard_append(table_name)
            self._set_status(f"Copied table name: '{table_name}'")

    def win_main_close(self) -> None:
        """
        Summary:
            ウィンドウ終了時の処理。
        Description:
            DB接続をクローズし、画面を破棄します。
        UserAction:
            ウィンドウの「閉じる（×）」ボタンをクリック - DB接続を切断しアプリケーションを終了する。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        try:
            self.fws_sqlite_viewer_logic_obj.close_db()
        except Exception as e:
            print(f"Error in win_main_close: {e}")
        finally:
            self.fws_sqlite_viewer_view_obj.destroy()
    #endregion

    #region Private Methods
    def _set_db_path(self, db_path: str) -> None:
        """
        Summary:
            テキスト入力欄にDBパスをセットします。
        Description:
            エントリの内容を上書きします。
        Args:
            db_path: str - DBパス
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_view_obj.ent_db_path.delete(0, tk.END)
        self.fws_sqlite_viewer_view_obj.ent_db_path.insert(0, db_path)

    def _get_db_path(self) -> str:
        """
        Summary:
            テキスト入力欄からDBパスを取得します。
        Returns:
            str - 入力されたDBパス。
        """
        return self.fws_sqlite_viewer_view_obj.ent_db_path.get().strip()

    def _get_sql_query(self) -> str:
        """
        Summary:
            テキストエリアからSQLクエリを取得します。
            テキストが選択（ハイライト）されている場合は、その選択範囲のテキストを返します。
            選択されていない場合は、エディタ全体のテキストを返します。
        Returns:
            str - 入力（または選択）されたSQL。
        """
        sel_ranges = self.fws_sqlite_viewer_view_obj.txt_sql.tag_ranges(tk.SEL)
        if sel_ranges:
            return self.fws_sqlite_viewer_view_obj.txt_sql.get(sel_ranges[0], sel_ranges[1]).strip()
        else:
            return self.fws_sqlite_viewer_view_obj.txt_sql.get("1.0", tk.END).strip()

    def _set_sql_query(self, sql: str) -> None:
        """
        Summary:
            テキストエリアにSQLをセットします。
        Args:
            sql: str - セットするSQL。
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_view_obj.txt_sql.delete("1.0", tk.END)
        self.fws_sqlite_viewer_view_obj.txt_sql.insert("1.0", sql)

    def _update_tables_list(self, tables: List[str]) -> None:
        """
        Summary:
            テーブル一覧ツリーを更新します。
        Args:
            tables: List[str] - テーブル名のリスト。
        Returns:
            None - 戻り値なし。
        """
        trv: tk.ttk.Treeview = self.fws_sqlite_viewer_view_obj.trv_tables
        for item in trv.get_children():
            trv.delete(item)
            
        for table in tables:
            trv.insert("", tk.END, text=table, values=(table,))

    def _update_schema_list(self, schema_list: List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema]) -> None:
        """
        Summary:
            スキーマリスト表示を更新します。
        Args:
            schema_list: List[fws_sqlite_viewer_dto_table_schema.FwsSqliteViewerDtoTableSchema] - スキーマDTOのリスト。
        Returns:
            None - 戻り値なし。
        """
        trv: tk.ttk.Treeview = self.fws_sqlite_viewer_view_obj.trv_schema
        for item in trv.get_children():
            trv.delete(item)
            
        for index, schema in enumerate(schema_list):
            tag = "even" if index % 2 == 0 else "odd"
            trv.insert("", tk.END, values=(
                schema.name,
                schema.type_name,
                "YES" if schema.pk > 0 else "",
                "YES" if schema.notnull == 1 else ""
            ), tags=(tag,))

    def _clear_results(self) -> None:
        """
        Summary:
            結果データグリッドをクリアします。
        Returns:
            None - 戻り値なし。
        """
        trv: tk.ttk.Treeview = self.fws_sqlite_viewer_view_obj.trv_results
        trv.delete(*trv.get_children())
        trv["columns"] = ()

    def _update_results(self, result_dto: fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult) -> None:
        """
        Summary:
            クエリ実行結果を画面に反映します。
        Args:
            result_dto: fws_sqlite_viewer_dto_query_result.FwsSqliteViewerDtoQueryResult - 実行結果DTO。
        Returns:
            None - 戻り値なし。
        """
        self._clear_results()
        
        if not result_dto.is_success:
            self._set_status(f"Error: {result_dto.error_message}", is_error=True)
            return

        trv: tk.ttk.Treeview = self.fws_sqlite_viewer_view_obj.trv_results
        
        # カラム設定
        if result_dto.columns:
            trv["columns"] = result_dto.columns
            for col in result_dto.columns:
                trv.heading(col, text=col)
                trv.column(col, width=100, anchor=tk.W)
                
            # データ行挿入
            for index, row in enumerate(result_dto.rows):
                tag = "even" if index % 2 == 0 else "odd"
                trv.insert("", tk.END, values=row, tags=(tag,))
                
            status_msg = f"Status: {result_dto.rowcount} rows returned in {result_dto.execution_time_ms:.2f} ms"
        else:
            # 更新系クエリの場合
            status_msg = f"Status: Query successful ({result_dto.rowcount} rows affected) in {result_dto.execution_time_ms:.2f} ms"
            
        self._set_status(status_msg, is_error=False)

    def _set_status(self, msg: str, is_error: bool = False) -> None:
        """
        Summary:
            ステータスラベルのメッセージを更新します。
        Args:
            msg: str - メッセージ文字列。
            is_error: bool - エラーの場合はTrue。
        Returns:
            None - 戻り値なし。
        """
        self.fws_sqlite_viewer_view_obj.lbl_status.config(text=msg)
        if is_error:
            self.fws_sqlite_viewer_view_obj.lbl_status.config(foreground="red")
        else:
            self.fws_sqlite_viewer_view_obj.lbl_status.config(foreground="black")

    def _load_db(self, db_path: str) -> None:
        """
        Summary:
            DBに接続し、テーブル一覧を更新します。
        Args:
            db_path: str - DBファイルパス。
        Returns:
            None - 戻り値なし。
        """
        try:
            tables = self.fws_sqlite_viewer_logic_obj.load_db(db_path)
            self._set_db_path(db_path)
            self._set_status("Connected to DB.")
            
            self._update_tables_list(tables)
            self._clear_results()
            self._update_schema_list([])
            
        except Exception as e:
            self._set_status(f"Error connecting to DB: {e}", is_error=True)
            self._update_tables_list([])
            self._clear_results()
            self.fws_sqlite_viewer_logic_obj.close_db()

    def _copy_treeview_selection(self, trv: tk.ttk.Treeview) -> None:
        """
        Summary:
            Treeviewの選択行をクリップボードにコピーします。
        Args:
            trv: tk.ttk.Treeview - 対象のTreeview。
        Returns:
            None - 戻り値なし。
        """
        selected_items = trv.selection()
        if not selected_items:
            return
            
        copied_data = []
        for item in selected_items:
            values = trv.item(item, 'values')
            copied_data.append("\t".join(str(v) for v in values))
            
        clipboard_text = "\n".join(copied_data)
        self.fws_sqlite_viewer_view_obj.clipboard_clear()
        self.fws_sqlite_viewer_view_obj.clipboard_append(clipboard_text)
        self._set_status(f"Copied {len(selected_items)} rows to clipboard.")

    def _copy_cell_value(self, trv: tk.ttk.Treeview, event: tk.Event) -> None:
        """
        Summary:
            ダブルクリックされたセルの値をクリップボードにコピーします。
        Args:
            trv: tk.ttk.Treeview - 対象のTreeview。
            event: tk.Event - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        region = trv.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        col = trv.identify_column(event.x)
        item = trv.identify_row(event.y)
        
        if col and item:
            col_index = int(col.replace('#', '')) - 1
            values = trv.item(item, 'values')
            if col_index < len(values):
                cell_value = values[col_index]
                self.fws_sqlite_viewer_view_obj.clipboard_clear()
                self.fws_sqlite_viewer_view_obj.clipboard_append(str(cell_value))
                
                # 文字列が長い場合は省略してStatusに表示
                display_val = str(cell_value)
                if len(display_val) > 30:
                    display_val = display_val[:27] + "..."
                self._set_status(f"Copied cell value: '{display_val}'")
    #endregion
