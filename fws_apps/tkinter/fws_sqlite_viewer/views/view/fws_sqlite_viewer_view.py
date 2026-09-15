"""
Summary:
    fws_sqlite_viewer アプリのビューモジュール。
Description:
    メイン画面のUIレイアウトを構築します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
from fws_apps.tkinter.fws_sqlite_viewer.constant import fws_sqlite_viewer_const

class FwsSqliteViewerView(tk.Tk):
    """
    Summary:
        SQLiteビューアーアプリのビュークラス。
    Description:
        DBパス入力、テーブル一覧、スキーマ詳細、SQLエディタ、結果グリッドを配置します。
    """
    
    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            UI部品を初期化し配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        super().__init__()
        
        self.title(fws_sqlite_viewer_const.WINDOW_TITLE)
        self.geometry(f"{fws_sqlite_viewer_const.WINDOW_MIN_WIDTH}x{fws_sqlite_viewer_const.WINDOW_MIN_HEIGHT}")
        self.minsize(fws_sqlite_viewer_const.WINDOW_MIN_WIDTH, fws_sqlite_viewer_const.WINDOW_MIN_HEIGHT)
        
        self._create_widgets()
    #endregion

    #region Private Methods
    def _create_widgets(self) -> None:
        """
        Summary:
            ウィジェットの生成と配置を行います。
        Description:
            メインウィンドウ内の各ペインやコントロールを構築します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # メインコンテナ
        self.frm_main: ttk.Frame = ttk.Frame(self)
        self.frm_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 上部: DB選択エリア
        self.frm_top: ttk.Frame = ttk.Frame(self.frm_main)
        self.frm_top.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))
        
        lbl_db_path: ttk.Label = ttk.Label(self.frm_top, text="DB Path:")
        lbl_db_path.pack(side=tk.LEFT, padx=(0, 5))
        
        self.ent_db_path: ttk.Entry = ttk.Entry(self.frm_top)
        self.ent_db_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_open_db: ttk.Button = ttk.Button(self.frm_top, text="Open DB")
        self.btn_open_db.pack(side=tk.LEFT)
        
        self.btn_new_db: ttk.Button = ttk.Button(self.frm_top, text="New DB")
        self.btn_new_db.pack(side=tk.LEFT, padx=(5, 0))
        
        # 中央: 左右分割 PanedWindow
        self.pw_main: ttk.PanedWindow = ttk.PanedWindow(self.frm_main, orient=tk.HORIZONTAL)
        self.pw_main.pack(fill=tk.BOTH, expand=True)
        
        # 左ペイン
        self.pw_left: ttk.PanedWindow = ttk.PanedWindow(self.pw_main, orient=tk.VERTICAL)
        self.pw_main.add(self.pw_left, weight=1)
        
        # 左上: テーブル一覧
        self.frm_tables: ttk.Frame = ttk.LabelFrame(self.pw_left, text="Tables")
        self.pw_left.add(self.frm_tables, weight=1)
        
        self.trv_tables: ttk.Treeview = ttk.Treeview(self.frm_tables, show="tree", selectmode="browse")
        scr_tables: ttk.Scrollbar = ttk.Scrollbar(self.frm_tables, orient=tk.VERTICAL, command=self.trv_tables.yview)
        self.trv_tables.configure(yscrollcommand=scr_tables.set)
        self.trv_tables.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_tables.pack(side=tk.RIGHT, fill=tk.Y)
        
        # テーブル用右クリックメニュー
        self.menu_tables: tk.Menu = tk.Menu(self.trv_tables, tearoff=0)
        self.menu_tables.add_command(label="Refresh", command=lambda: None) # Event層で上書き
        self.menu_tables.add_command(label="Detach Database", command=lambda: None) # Event層で上書き
        
        # 左下: テーブルスキーマ詳細
        self.frm_schema: ttk.LabelFrame = ttk.LabelFrame(self.pw_left, text="Schema Details")
        self.pw_left.add(self.frm_schema, weight=1)
        
        self.trv_schema: ttk.Treeview = ttk.Treeview(self.frm_schema, columns=("Name", "Type", "PK", "Not Null"), show="headings", selectmode="extended")
        self.trv_schema.heading("Name", text="Column Name")
        self.trv_schema.heading("Type", text="Type")
        self.trv_schema.heading("PK", text="PK")
        self.trv_schema.heading("Not Null", text="Not Null")
        self.trv_schema.column("Name", width=100)
        self.trv_schema.column("Type", width=80)
        self.trv_schema.column("PK", width=30)
        self.trv_schema.column("Not Null", width=60)
        
        scr_schema: ttk.Scrollbar = ttk.Scrollbar(self.frm_schema, orient=tk.VERTICAL, command=self.trv_schema.yview)
        self.trv_schema.configure(yscrollcommand=scr_schema.set)
        self.trv_schema.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_schema.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右ペイン
        self.pw_right: ttk.PanedWindow = ttk.PanedWindow(self.pw_main, orient=tk.VERTICAL)
        self.pw_main.add(self.pw_right, weight=3)
        
        # 右上: SQLエディタ
        self.frm_sql: ttk.LabelFrame = ttk.LabelFrame(self.pw_right, text="SQL Query Editor")
        self.pw_right.add(self.frm_sql, weight=1)
        
        self.txt_sql: tk.Text = tk.Text(self.frm_sql, wrap=tk.NONE, height=10)
        scr_sql_y: ttk.Scrollbar = ttk.Scrollbar(self.frm_sql, orient=tk.VERTICAL, command=self.txt_sql.yview)
        scr_sql_x: ttk.Scrollbar = ttk.Scrollbar(self.frm_sql, orient=tk.HORIZONTAL, command=self.txt_sql.xview)
        self.txt_sql.configure(yscrollcommand=scr_sql_y.set, xscrollcommand=scr_sql_x.set)
        
        self.btn_run_query: ttk.Button = ttk.Button(self.frm_sql, text="Run Query")
        
        self.btn_run_query.pack(side=tk.BOTTOM, anchor=tk.E, pady=5, padx=5)
        scr_sql_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.txt_sql.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_sql_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右下: 結果データグリッド
        self.frm_results: ttk.LabelFrame = ttk.LabelFrame(self.pw_right, text="Query Results")
        self.pw_right.add(self.frm_results, weight=3)
        
        self.lbl_status: ttk.Label = ttk.Label(self.frm_results, text="Status: Ready")
        self.lbl_status.pack(side=tk.TOP, fill=tk.X, anchor=tk.W, pady=(0, 2))
        
        self.trv_results: ttk.Treeview = ttk.Treeview(self.frm_results, show="headings", selectmode="extended")
        scr_results_y: ttk.Scrollbar = ttk.Scrollbar(self.frm_results, orient=tk.VERTICAL, command=self.trv_results.yview)
        scr_results_x: ttk.Scrollbar = ttk.Scrollbar(self.frm_results, orient=tk.HORIZONTAL, command=self.trv_results.xview)
        self.trv_results.configure(yscrollcommand=scr_results_y.set, xscrollcommand=scr_results_x.set)
        
        scr_results_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.trv_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_results_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ストライプ行用のタグ設定
        self.trv_schema.tag_configure("even", background="#f0f0f0")
        self.trv_schema.tag_configure("odd", background="#ffffff")
        self.trv_results.tag_configure("even", background="#f0f0f0")
        self.trv_results.tag_configure("odd", background="#ffffff")
    #endregion
