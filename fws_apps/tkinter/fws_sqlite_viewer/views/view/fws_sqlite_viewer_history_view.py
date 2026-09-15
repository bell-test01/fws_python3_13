"""
Summary:
    fws_sqlite_viewer アプリの実行履歴ダイアログのビューモジュール。
Description:
    実行履歴一覧をポップアップ表示するダイアログのUIレイアウトを構築します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk

class FwsSqliteViewerHistoryView(tk.Toplevel):
    """
    Summary:
        複数クエリの実行履歴を表示するダイアログのビュークラス。
    Description:
        Treeviewと閉じるボタンを配置します。
    """
    
    #region Constructor
    def __init__(self, parent: tk.Tk) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            UI部品を初期化し配置します。
        Args:
            parent: tk.Tk - 親ウィンドウ
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent)
        self.title("Query Execution History")
        self._create_widgets()
    #endregion

    #region Private Methods
    def _create_widgets(self) -> None:
        """
        Summary:
            ウィジェットの生成と配置を行います。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.frm_main: ttk.Frame = ttk.Frame(self)
        self.frm_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 履歴一覧ツリービュー
        columns = ("query", "rows")
        self.trv_history: ttk.Treeview = ttk.Treeview(self.frm_main, columns=columns, show="headings")
        self.trv_history.heading("query", text="Query")
        self.trv_history.heading("rows", text="Rows")
        self.trv_history.column("query", width=450, anchor=tk.W)
        self.trv_history.column("rows", width=100, anchor=tk.E)
        
        self.scr_history: ttk.Scrollbar = ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.trv_history.yview)
        self.trv_history.configure(yscrollcommand=self.scr_history.set)
        
        self.trv_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scr_history.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.trv_history.tag_configure("even", background="#f9f9f9")
        self.trv_history.tag_configure("odd", background="#ffffff")
        
        # 閉じるボタン
        self.btn_close: ttk.Button = ttk.Button(self, text="OK")
        self.btn_close.pack(pady=(0, 10))
    #endregion
