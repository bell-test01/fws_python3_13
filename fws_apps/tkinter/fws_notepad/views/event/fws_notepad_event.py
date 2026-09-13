"""
Summary:
    fws_notepad アプリのイベントモジュール。
Description:
    ボタン押下や画面終了などのユーザー操作イベントをハンドリングします。
ScreenName:
    メモ帳メイン画面
Attachment:
    なし
"""
import tkinter as tk
from fws_apps.tkinter.fws_notepad.views.view import fws_notepad_view
from fws_apps.tkinter.fws_notepad.views.logic import fws_notepad_logic
from fws_apps.tkinter.fws_notepad.businesses.business import fws_notepad_business

class FwsNotepadEvent:
    """
    Summary:
        メモ帳アプリのイベントクラス。
    Description:
        各UIのイベントバインドおよび処理の呼び出しを行います。
    """
    
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            View, Business, Logicの各インスタンスを生成し、イベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_view_obj: fws_notepad_view.FwsNotepadView = fws_notepad_view.FwsNotepadView()
        """fws_notepad_view.FwsNotepadView - ビューオブジェクト"""
        
        self.fws_notepad_business_obj: fws_notepad_business.FwsNotepadBusiness = fws_notepad_business.FwsNotepadBusiness()
        """fws_notepad_business.FwsNotepadBusiness - ビジネスオブジェクト"""
        
        self.fws_notepad_logic_obj: fws_notepad_logic.FwsNotepadLogic = fws_notepad_logic.FwsNotepadLogic(
            self.fws_notepad_view_obj, 
            self.fws_notepad_business_obj
        )
        """fws_notepad_logic.FwsNotepadLogic - ロジックオブジェクト"""
        
        self.bind_events()
        
        try:
            self.fws_notepad_logic_obj.load_initial_data()
        except Exception as e:
            print(f"Failed to load initial data: {e}")
        
    def bind_events(self) -> None:
        """
        Summary:
            イベントをバインドします。
        Description:
            ボタンやウィンドウへのイベントを登録します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_view_obj.btn_save.config(command=self.btn_save_click)
        self.fws_notepad_view_obj.protocol("WM_DELETE_WINDOW", self.win_main_close)
        
    def btn_save_click(self) -> None:
        """
        Summary:
            保存ボタンクリック時のイベント。
        Description:
            ロジックに保存処理を委譲します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            保存ボタンクリック - メモテキストが保存されます。
        """
        try:
            self.fws_notepad_logic_obj.save_memo_data()
        except Exception as e:
            print(f"Error in btn_save_click: {e}")
            
    def win_main_close(self) -> None:
        """
        Summary:
            ウィンドウ終了時のイベント。
        Description:
            ロジックに設定保存処理を委譲し、画面を破棄します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            閉じる(X)ボタンクリック - 設定情報が保存され、アプリが終了します。
        """
        try:
            self.fws_notepad_logic_obj.save_window_settings()
        except Exception as e:
            print(f"Error in win_main_close: {e}")
        finally:
            self.fws_notepad_view_obj.destroy()
