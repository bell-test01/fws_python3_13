"""
Summary:
    fws_notepad アプリのビューモジュール。
Description:
    メイン画面のUIレイアウトを構築します。
Attachment:
    なし
"""
import tkinter as tk

class FwsNotepadView(tk.Tk):
    """
    Summary:
        メモ帳アプリのビュークラス。
    Description:
        テキストエリアや保存ボタンなどのウィジェットを配置します。
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
        self.title("Fws Notepad (Git Check)")
        
        self.frm_main: tk.Frame = tk.Frame(self)
        """tk.Frame - メインフレーム"""
        self.frm_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.txt_memo: tk.Text = tk.Text(self.frm_main, wrap=tk.WORD)
        """tk.Text - メモ入力用テキストエリア"""
        self.txt_memo.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.btn_save: tk.Button = tk.Button(self.frm_main, text="保存 (Save)", width=20)
        """tk.Button - 保存ボタン"""
        self.btn_save.pack(side=tk.RIGHT)
    #endregion
