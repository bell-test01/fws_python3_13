"""
Summary:
    fws_notepad アプリのエントリーポイント。
Description:
    システムパスを追加し、アプリケーションのイベントクラスを起動します。
Attachment:
    なし
"""
import sys
from pathlib import Path
import tkinter as tk

current_dir: Path = Path(__file__).resolve().parent
"""Path - カレントディレクトリ"""
project_root: Path = current_dir.parent.parent.parent
"""Path - プロジェクトルートディレクトリ"""
sys.path.append(str(project_root))

from fws_apps.tkinter.fws_notepad.views.event import fws_notepad_event

def main() -> None:
    """
    Summary:
        アプリケーションのメイン処理。
    Description:
        ルートウィンドウを生成し、イベントクラスをインスタンス化してメインループを開始します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    try:
        fws_notepad_event_obj: fws_notepad_event.FwsNotepadEvent = fws_notepad_event.FwsNotepadEvent()
        fws_notepad_event_obj.fws_notepad_view_obj.mainloop()
    except Exception as e:
        print(f"Fatal error in application: {e}")

if __name__ == "__main__":
    main()
