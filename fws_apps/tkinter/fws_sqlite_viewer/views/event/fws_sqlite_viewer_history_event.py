"""
Summary:
    fws_sqlite_viewer アプリの実行履歴ダイアログのイベントモジュール。
Description:
    UIイベントのバインドおよびダイアログの表示制御を行います。
Attachment:
    なし
"""
import tkinter as tk
from typing import List

from fws_apps.tkinter.fws_sqlite_viewer.views.view import fws_sqlite_viewer_history_view
from fws_apps.tkinter.fws_sqlite_viewer.views.logic import fws_sqlite_viewer_history_logic

class FwsSqliteViewerHistoryEvent:
    """
    Summary:
        実行履歴ダイアログのイベントクラス。
    Description:
        Viewからのイベントを受け取り、Logicまたは自身の表示処理を実行します。
    """

    #region Constructor
    def __init__(self, parent_view: tk.Tk | tk.Toplevel | tk.Widget) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            ViewとLogicのインスタンスを生成し、イベントをバインドします。
        Args:
            parent_view: tk.Tk | tk.Toplevel | tk.Widget - 親ウィンドウまたはウィジェット。
        Returns:
            None - 戻り値なし。
        """
        self.parent_view = parent_view
        
        # ViewとLogicの初期化
        self.view: fws_sqlite_viewer_history_view.FwsSqliteViewerHistoryView = fws_sqlite_viewer_history_view.FwsSqliteViewerHistoryView(self.parent_view)
        self.logic: fws_sqlite_viewer_history_logic.FwsSqliteViewerHistoryLogic = fws_sqlite_viewer_history_logic.FwsSqliteViewerHistoryLogic()
        
        self._bind_events()
    #endregion

    #region Private Methods
    def _bind_events(self) -> None:
        """
        Summary:
            Viewのイベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.view.btn_close.config(command=self.view.destroy)
    #endregion

    #region Public Methods
    def show_dialog(self, history: List[tuple]) -> None:
        """
        Summary:
            履歴ダイアログを中央に配置して表示し、データを流し込みます。
        Args:
            history: List[tuple] - クエリ文字列と処理件数のタプルリスト。
        Returns:
            None - 戻り値なし。
        """
        # メインウィンドウの中央に配置
        width, height = 600, 400
        parent_x = self.parent_view.winfo_rootx()
        parent_y = self.parent_view.winfo_rooty()
        parent_width = self.parent_view.winfo_width()
        parent_height = self.parent_view.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.view.geometry(f"{width}x{height}+{x}+{y}")
        
        # データの取得と流し込み
        formatted_history = self.logic.format_history_for_display(history)
        for query_single_line, rows, tag in formatted_history:
            self.view.trv_history.insert("", tk.END, values=(query_single_line, rows), tags=(tag,))
    
    def destroy(self) -> None:
        """
        Summary:
            ダイアログを破棄します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.view.winfo_exists():
            self.view.destroy()
    
    def winfo_exists(self) -> bool:
        """
        Summary:
            ダイアログが存在するかどうかを返します。
        Args:
            なし
        Returns:
            bool - 存在する場合はTrue、そうでない場合はFalse。
        """
        return self.view.winfo_exists()
    #endregion
