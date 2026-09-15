"""
Summary:
    fws_lib Tkinter アプリ用のダイアログユーティリティ。
Description:
    tkinter.messagebox や filedialog のよく使う処理をラップして提供します。
"""
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from typing import Optional

class DialogUtils:
    """
    Summary:
        メッセージダイアログ・ファイル選択ダイアログのユーティリティクラス。
    """

    @staticmethod
    def show_info(title: str, message: str) -> None:
        """
        Summary:
            情報ダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            message (str): 表示するメッセージ。
        """
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title: str, message: str) -> None:
        """
        Summary:
            エラーダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            message (str): 表示するメッセージ。
        """
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str) -> None:
        """
        Summary:
            警告ダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            message (str): 表示するメッセージ。
        """
        messagebox.showwarning(title, message)

    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        """
        Summary:
            「はい/いいえ」を確認するダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            message (str): 表示するメッセージ。
        Returns:
            bool: 「はい」を選択した場合は True、それ以外は False。
        """
        return messagebox.askyesno(title, message)

    @staticmethod
    def ask_open_file(title: str, filetypes: tuple, initialdir: Optional[str] = None) -> str:
        """
        Summary:
            ファイルを開くダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            filetypes (tuple): 選択可能なファイル形式のタプル。
            initialdir (Optional[str]): 初期ディレクトリ。
        Returns:
            str: 選択されたファイルのパス。キャンセルされた場合は空文字。
        """
        options = {"title": title, "filetypes": filetypes}
        if initialdir:
            options["initialdir"] = initialdir
        
        path = filedialog.askopenfilename(**options)
        return path if path else ""

    @staticmethod
    def ask_open_dir(title: str, initialdir: Optional[str] = None) -> str:
        """
        Summary:
            ディレクトリを選択するダイアログを表示します。
        Args:
            title (str): ダイアログのタイトル。
            initialdir (Optional[str]): 初期ディレクトリ。
        Returns:
            str: 選択されたディレクトリのパス。キャンセルされた場合は空文字。
        """
        options = {"title": title}
        if initialdir:
            options["initialdir"] = initialdir
            
        path = filedialog.askdirectory(**options)
        return path if path else ""
