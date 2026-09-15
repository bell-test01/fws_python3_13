"""
Summary:
    fws_sqlite_viewer アプリの定数定義モジュール。
Description:
    アプリ内で使用する不変の値を定義します。
Attachment:
    なし
"""
from pathlib import Path

# アプリケーションのルートディレクトリ（このファイルから見て3階層上）
APP_DIR: Path = Path(__file__).resolve().parent.parent
"""Path - アプリケーションのルートディレクトリ"""

# デフォルトのデータ・出力ディレクトリ
DATA_DIR: Path = APP_DIR / "data"
"""Path - データファイル格納ディレクトリ"""
OUTPUT_DIR: Path = APP_DIR / "output"
"""Path - 出力ファイル格納ディレクトリ"""

# UI定数
WINDOW_TITLE: str = "DBBrowser SQLite - fws_sqlite_viewer"
"""str - メインウィンドウのタイトル"""
WINDOW_MIN_WIDTH: int = 600
"""int - ウィンドウの最小幅"""
WINDOW_MIN_HEIGHT: int = 400
"""int - ウィンドウの最小高さ"""
