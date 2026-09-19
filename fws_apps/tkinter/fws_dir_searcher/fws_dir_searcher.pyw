"""
Summary:
    fws_dir_searcher アプリのエントリーポイント。
Description:
    システムパスを追加し、アプリケーションのイベントクラスを起動します。
Attachment:
    なし
"""
import sys
from pathlib import Path

app_dir: Path = Path(__file__).resolve().parent
"""Path - アプリケーションディレクトリ"""
project_root: Path = app_dir.parent.parent.parent
"""Path - プロジェクトルートディレクトリ"""
sys.path.append(str(project_root))

from fws_apps.tkinter.fws_dir_searcher.views.event import fws_dir_searcher_event

def main() -> None:
    """
    Summary:
        アプリケーションのメイン処理。
    Description:
        イベントクラスをインスタンス化してメインループを開始します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    try:
        event_obj: fws_dir_searcher_event.FwsDirSearcherEvent = fws_dir_searcher_event.FwsDirSearcherEvent()
        event_obj.fws_dir_searcher_view_obj.mainloop()
    except Exception as e:
        print(f"Fatal error in application: {e}")

if __name__ == "__main__":
    main()
