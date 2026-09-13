"""
Summary:
    fws_notepad アプリのロジックモジュール。
Description:
    ViewとBusinessを繋ぎ、データの受け渡しやUIへの反映を制御します。
Attachment:
    なし
"""
from fws_apps.tkinter.fws_notepad.views.view import fws_notepad_view
from fws_apps.tkinter.fws_notepad.businesses.business import fws_notepad_business
from fws_apps.tkinter.fws_notepad.businesses.dto import fws_notepad_dto

class FwsNotepadLogic:
    """
    Summary:
        メモ帳アプリのロジッククラス。
    Description:
        Business層から取得したデータをView層に反映させます。
    """
    
    def __init__(self, view_obj: fws_notepad_view.FwsNotepadView, business_obj: fws_notepad_business.FwsNotepadBusiness) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            ViewとBusinessのインスタンスを保持します。
        Args:
            view_obj: fws_notepad_view.FwsNotepadView - ビュークラスのインスタンス。
            business_obj: fws_notepad_business.FwsNotepadBusiness - ビジネスロジッククラスのインスタンス。
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_view_obj: fws_notepad_view.FwsNotepadView = view_obj
        """fws_notepad_view.FwsNotepadView - ビューオブジェクト"""
        
        self.fws_notepad_business_obj: fws_notepad_business.FwsNotepadBusiness = business_obj
        """fws_notepad_business.FwsNotepadBusiness - ビジネスオブジェクト"""
        
    def load_initial_data(self) -> None:
        """
        Summary:
            初期データの読み込みと画面への反映を行います。
        Description:
            起動時に設定やメモ内容を読み込みます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        dto_obj: fws_notepad_dto.FwsNotepadDto = self.fws_notepad_business_obj.load_settings()
        self.fws_notepad_view_obj.geometry(f"{dto_obj.window_width}x{dto_obj.window_height}+{dto_obj.window_x}+{dto_obj.window_y}")
        
        memo_content: str = self.fws_notepad_business_obj.load_memo()
        self.fws_notepad_view_obj.txt_memo.insert("1.0", memo_content)
        
    def save_memo_data(self) -> None:
        """
        Summary:
            入力されたメモデータを保存します。
        Description:
            Viewのテキストエリアから値を取得し、Businessへ渡します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        content: str = self.fws_notepad_view_obj.txt_memo.get("1.0", "end-1c")
        dto_obj: fws_notepad_dto.FwsNotepadDto = fws_notepad_dto.FwsNotepadDto(text_content=content)
        self.fws_notepad_business_obj.save_memo(dto_obj)
        print("Memo saved.")
        
    def save_window_settings(self) -> None:
        """
        Summary:
            現在のウィンドウ設定を保存します。
        Description:
            ウィンドウの位置・サイズを取得し、Businessへ渡します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        geom: str = self.fws_notepad_view_obj.geometry()
        try:
            width_height, x, y = geom.split('+')
            width, height = width_height.split('x')
            
            dto_obj: fws_notepad_dto.FwsNotepadDto = fws_notepad_dto.FwsNotepadDto(
                window_width=int(width),
                window_height=int(height),
                window_x=int(x),
                window_y=int(y)
            )
            self.fws_notepad_business_obj.save_settings(dto_obj)
            print("Settings saved.")
        except Exception as e:
            print(f"Failed to parse and save geometry: {e}")
