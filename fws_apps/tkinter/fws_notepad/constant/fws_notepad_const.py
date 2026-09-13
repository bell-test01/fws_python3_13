"""
Summary:
    fws_notepad アプリの定数モジュール。
Description:
    アプリケーション全体で使用するファイルパスなどの定数を定義します。
Attachment:
    なし
"""
from pathlib import Path

APP_DIR: Path = Path(__file__).resolve().parent.parent
"""Path - アプリケーションのルートディレクトリパス"""

DATA_DIR: Path = APP_DIR / 'data'
"""Path - データ保存用ディレクトリパス"""

OUTPUT_DIR: Path = APP_DIR / 'output'
"""Path - 出力用ディレクトリパス"""

SETTINGS_FILE_PATH: Path = DATA_DIR / 'settings.json'
"""Path - 設定情報の保存先ファイルパス"""

MEMO_FILE_PATH: Path = OUTPUT_DIR / 'memo.txt'
"""Path - メモテキストの保存先ファイルパス"""
