"""
Summary:
    fws_notepad アプリのエンティティモジュール。
Description:
    設定情報を保持するエンティティクラスを定義します。
Attachment:
    なし
"""
from dataclasses import dataclass

@dataclass
class FwsNotepadEntity:
    """
    Summary:
        メモ帳アプリの設定情報を保持するエンティティクラス。
    Description:
        Business層内部やデータストアへの保存・読み込み時に使用します。
    """
    window_width: int = 600
    """int - ウィンドウの幅"""
    
    window_height: int = 400
    """int - ウィンドウの高さ"""
    
    window_x: int = 100
    """int - ウィンドウのX座標"""
    
    window_y: int = 100
    """int - ウィンドウのY座標"""
