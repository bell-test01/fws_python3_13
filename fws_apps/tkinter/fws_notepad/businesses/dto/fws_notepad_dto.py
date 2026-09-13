"""
Summary:
    fws_notepad アプリのデータ転送用DTOモジュール。
Description:
    Event/Logic層とBusiness層の間で、設定情報やメモテキストを受け渡すためのDTOクラスを定義します。
Attachment:
    なし
"""
from dataclasses import dataclass

@dataclass
class FwsNotepadDto:
    """
    Summary:
        メモ帳アプリの設定およびテキスト情報を保持するDTOクラス。
    Description:
        Event/Logic層とBusiness層のデータ受け渡しに使用します。
    """
    window_width: int = 600
    """int - ウィンドウの幅"""
    
    window_height: int = 400
    """int - ウィンドウの高さ"""
    
    window_x: int = 100
    """int - ウィンドウのX座標"""
    
    window_y: int = 100
    """int - ウィンドウのY座標"""
    
    text_content: str = ""
    """str - メモのテキスト内容"""
