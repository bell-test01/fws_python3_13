"""
Summary:
    fws_notepad アプリのビジネスロジックモジュール。
Description:
    設定情報のロード/セーブやメモのロード/セーブ等のファイルI/O処理を担当します。
Attachment:
    なし
"""
import json
from pathlib import Path
from fws_apps.tkinter.fws_notepad.businesses.entity import fws_notepad_entity
from fws_apps.tkinter.fws_notepad.businesses.dto import fws_notepad_dto
from fws_apps.tkinter.fws_notepad.constant import fws_notepad_const

class FwsNotepadBusiness:
    """
    Summary:
        メモ帳アプリのビジネスロジッククラス。
    Description:
        設定およびメモのファイルI/Oを行います。
    """
    
    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            保存用ディレクトリが存在しない場合は作成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        fws_notepad_const.DATA_DIR.mkdir(parents=True, exist_ok=True)
        fws_notepad_const.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    #endregion

    #region Public Methods
    def load_settings(self) -> fws_notepad_dto.FwsNotepadDto:
        """
        Summary:
            設定情報を読み込み、DTOとして返します。
        Description:
            JSONファイルから設定を読み込み、存在しない場合はデフォルト値を返します。
        Args:
            なし
        Returns:
            fws_notepad_dto.FwsNotepadDto - 設定情報を格納したDTO。
        """
        entity_obj: fws_notepad_entity.FwsNotepadEntity = fws_notepad_entity.FwsNotepadEntity()
        if fws_notepad_const.SETTINGS_FILE_PATH.exists():
            try:
                with fws_notepad_const.SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
                    data: dict = json.load(f)
                    entity_obj.window_width = data.get('window_width', entity_obj.window_width)
                    entity_obj.window_height = data.get('window_height', entity_obj.window_height)
                    entity_obj.window_x = data.get('window_x', entity_obj.window_x)
                    entity_obj.window_y = data.get('window_y', entity_obj.window_y)
            except Exception as e:
                print(f"Failed to load settings: {e}")
                
        dto_obj: fws_notepad_dto.FwsNotepadDto = fws_notepad_dto.FwsNotepadDto(
            window_width=entity_obj.window_width,
            window_height=entity_obj.window_height,
            window_x=entity_obj.window_x,
            window_y=entity_obj.window_y
        )
        return dto_obj

    def save_settings(self, dto_obj: fws_notepad_dto.FwsNotepadDto) -> None:
        """
        Summary:
            設定情報をJSONファイルに保存します。
        Description:
            DTOから情報を受け取り、JSON形式で保存します。
        Args:
            dto_obj: fws_notepad_dto.FwsNotepadDto - 保存する設定情報を持ったDTO。
        Returns:
            None - 戻り値なし。
        """
        entity_obj: fws_notepad_entity.FwsNotepadEntity = fws_notepad_entity.FwsNotepadEntity(
            window_width=dto_obj.window_width,
            window_height=dto_obj.window_height,
            window_x=dto_obj.window_x,
            window_y=dto_obj.window_y
        )
        data: dict = {
            'window_width': entity_obj.window_width,
            'window_height': entity_obj.window_height,
            'window_x': entity_obj.window_x,
            'window_y': entity_obj.window_y
        }
        try:
            with fws_notepad_const.SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def load_memo(self) -> str:
        """
        Summary:
            メモテキストを読み込みます。
        Description:
            テキストファイルからメモ内容を読み込み、文字列として返します。
        Args:
            なし
        Returns:
            str - 読み込んだメモ内容。
        """
        if fws_notepad_const.MEMO_FILE_PATH.exists():
            try:
                with fws_notepad_const.MEMO_FILE_PATH.open('r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Failed to load memo: {e}")
        return ""

    def save_memo(self, dto_obj: fws_notepad_dto.FwsNotepadDto) -> None:
        """
        Summary:
            メモテキストを保存します。
        Description:
            DTOのテキスト内容をファイルに保存します。
        Args:
            dto_obj: fws_notepad_dto.FwsNotepadDto - 保存するテキスト情報を持ったDTO。
        Returns:
            None - 戻り値なし。
        """
        try:
            with fws_notepad_const.MEMO_FILE_PATH.open('w', encoding='utf-8') as f:
                f.write(dto_obj.text_content)
        except Exception as e:
            print(f"Failed to save memo: {e}")
    #endregion
