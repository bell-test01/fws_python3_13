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
from fws_apps.tkinter.fws_notepad.businesses.dto import fws_notepad_dto

class FwsNotepadEvent:
    """
    Summary:
        メモ帳アプリのイベントクラス。
    Description:
        各UIのイベントバインドおよび処理の呼び出しを行います。
    """
    
    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            View, Logicの各インスタンスを生成し、イベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_view_obj: fws_notepad_view.FwsNotepadView = fws_notepad_view.FwsNotepadView()
        """fws_notepad_view.FwsNotepadView - ビューオブジェクト"""
        
        self.fws_notepad_logic_obj: fws_notepad_logic.FwsNotepadLogic = fws_notepad_logic.FwsNotepadLogic()
        """fws_notepad_logic.FwsNotepadLogic - ロジックオブジェクト"""
        
        self.bind_events()
        
        try:
            dto_obj = self.fws_notepad_logic_obj.load_initial_data()
            self.fws_notepad_view_obj.geometry(f"{dto_obj.window_width}x{dto_obj.window_height}+{dto_obj.window_x}+{dto_obj.window_y}")
            self.fws_notepad_view_obj.txt_memo.insert("1.0", dto_obj.text_content)
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
    #endregion

    #region Public Methods
    def btn_save_click(self) -> None:
        """
        Summary:
            保存ボタンクリック時のイベント。
        Description:
            Viewから入力内容を取得し、ロジックに保存処理を委譲します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            保存ボタンクリック - メモテキストが保存されます。
        """
        try:
            content: str = self.fws_notepad_view_obj.txt_memo.get("1.0", "end-1c")
            dto_obj: fws_notepad_dto.FwsNotepadDto = fws_notepad_dto.FwsNotepadDto(text_content=content)
            self.fws_notepad_logic_obj.save_memo_data(dto_obj)
        except Exception as e:
            print(f"Error in btn_save_click: {e}")
            
    def win_main_close(self) -> None:
        """
        Summary:
            ウィンドウ終了時のイベント。
        Description:
            Viewからウィンドウ情報を取得し、ロジックに設定保存処理を委譲して画面を破棄します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            閉じる(X)ボタンクリック - 設定情報が保存され、アプリが終了します。
        """
        try:
            geom: str = self.fws_notepad_view_obj.geometry()
            width_height, x, y = geom.split('+')
            width, height = width_height.split('x')
            
            dto_obj: fws_notepad_dto.FwsNotepadDto = fws_notepad_dto.FwsNotepadDto(
                window_width=int(width),
                window_height=int(height),
                window_x=int(x),
                window_y=int(y)
            )
            self.fws_notepad_logic_obj.save_window_settings(dto_obj)
        except Exception as e:
            print(f"Error in win_main_close: {e}")
        finally:
            self.fws_notepad_view_obj.destroy()
    #endregion
