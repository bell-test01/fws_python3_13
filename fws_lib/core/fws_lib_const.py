"""
Summary:
    fws_lib 全体で利用する共通の定数モジュール。
Description:
    ファイルエンコーディングなどの基本的な定数を定義します。
"""

class FwsLibConst:
    """
    Summary:
        共通定数クラス。
    """
    
    # デフォルトのファイルエンコーディング
    DEFAULT_ENCODING: str = "utf-8"
    
    # 共通エラーメッセージのプレフィックス
    ERROR_PREFIX: str = "[FWS_LIB_ERROR]"
