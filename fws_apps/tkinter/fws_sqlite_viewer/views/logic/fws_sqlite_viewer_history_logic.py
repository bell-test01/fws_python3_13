"""
Summary:
    fws_sqlite_viewer アプリの実行履歴ダイアログのロジックモジュール。
Description:
    履歴データの変換・整形処理を配置します。
Attachment:
    なし
"""
from typing import List, Tuple

class FwsSqliteViewerHistoryLogic:
    """
    Summary:
        実行履歴ダイアログのロジッククラス。
    Description:
        受け取った履歴データをView（Treeview）表示用に整形します。
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
        pass
    #endregion

    #region Public Methods
    def format_history_for_display(self, history: List[tuple]) -> List[Tuple[str, int, str]]:
        """
        Summary:
            履歴データをTreeview表示用に整形します。
        Description:
            改行をスペースに置換し、偶数/奇数行判定用のタグを付与します。
        Args:
            history: List[tuple] - クエリ文字列と処理件数のタプルリスト。
        Returns:
            List[Tuple[str, int, str]] - 整形済みクエリ, 処理件数, タグ名("even" or "odd") のタプルリスト。
        """
        formatted_list = []
        for index, (query, rows) in enumerate(history):
            # 改行をスペースに置換して1行で表示
            query_single_line = query.replace("\n", " ").replace("\r", "")
            tag = "even" if index % 2 == 0 else "odd"
            formatted_list.append((query_single_line, rows, tag))
            
        return formatted_list
    #endregion
