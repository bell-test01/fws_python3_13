"""
Summary:
    fws_notepad アプリのロジックモジュール。
Description:
    ViewとBusinessを繋ぎ、データの受け渡しやUIへの反映を制御します。
Attachment:
    なし
"""
from typing import Tuple
from fws_apps.tkinter.fws_notepad.businesses.business import fws_notepad_business
from fws_apps.tkinter.fws_notepad.businesses.dto import fws_notepad_dto

class FwsNotepadLogic:
    """
    Summary:
        メモ帳アプリのロジッククラス。
    Description:
        Business層から取得したデータをView層に反映させます。
    """
    
    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            Businessインスタンスを保持します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_business_obj: fws_notepad_business.FwsNotepadBusiness = fws_notepad_business.FwsNotepadBusiness()
        """fws_notepad_business.FwsNotepadBusiness - ビジネスオブジェクト"""
    #endregion

    #region Public Methods
    def load_initial_data(self) -> fws_notepad_dto.FwsNotepadDto:
        """
        Summary:
            初期データの読み込みを行います。
        Description:
            起動時に設定やメモ内容を読み込み、DTOとして返却します。
        Args:
            なし
        Returns:
            fws_notepad_dto.FwsNotepadDto - 設定情報とメモ内容を格納したDTO。
        """
        dto_obj: fws_notepad_dto.FwsNotepadDto = self.fws_notepad_business_obj.load_settings()
        memo_content: str = self.fws_notepad_business_obj.load_memo()
        dto_obj.text_content = memo_content
        return dto_obj
        
    def save_memo_data(self, dto_obj: fws_notepad_dto.FwsNotepadDto) -> None:
        """
        Summary:
            入力されたメモデータを保存します。
        Description:
            Eventから受け取ったDTOをBusinessへ渡します。
        Args:
            dto_obj: fws_notepad_dto.FwsNotepadDto - 保存するメモデータ
        Returns:
            None - 戻り値なし。
        """
        self.fws_notepad_business_obj.save_memo(dto_obj)
        print("Memo saved.")
        
    def save_window_settings(self, dto_obj: fws_notepad_dto.FwsNotepadDto) -> None:
        """
        Summary:
            現在のウィンドウ設定を保存します。
        Description:
            Eventから受け取ったDTOをBusinessへ渡します。
        Args:
            dto_obj: fws_notepad_dto.FwsNotepadDto - 保存するウィンドウ設定データ
        Returns:
            None - 戻り値なし。
        """
        try:
            self.fws_notepad_business_obj.save_settings(dto_obj)
            print("Settings saved.")
        except Exception as e:
            print(f"Failed to save settings in logic: {e}")
    #endregion
