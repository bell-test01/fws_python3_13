"""
Summary:
    fws_dir_searcher アプリのロジックモジュール。
Description:
    UIイベントとビジネスロジックの仲介を行います。
Attachment:
    なし
"""
from fws_apps.tkinter.fws_dir_searcher.businesses import fws_dir_searcher_business
from fws_apps.tkinter.fws_dir_searcher.businesses.dto import fws_dir_searcher_dto_search_result

class FwsDirSearcherLogic:
    """
    Summary:
        UIからの要求を受け、ビジネスロジックを呼び出すクラス。
    """

    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        """
        self.fws_dir_searcher_business_obj: fws_dir_searcher_business.FwsDirSearcherBusiness = fws_dir_searcher_business.FwsDirSearcherBusiness()
        """fws_dir_searcher_business.FwsDirSearcherBusiness - ビジネスオブジェクト"""

    def perform_search(self, root_path: str, keyword: str) -> fws_dir_searcher_dto_search_result.FwsDirSearcherDtoSearchResult:
        """
        Summary:
            ディレクトリ検索を実行します。
        Args:
            root_path: str - ルートディレクトリ。
            keyword: str - 検索キーワード。
        Returns:
            FwsDirSearcherDtoSearchResult - 検索結果DTO。
        """
        if not root_path:
            return fws_dir_searcher_dto_search_result.FwsDirSearcherDtoSearchResult(
                is_success=False, 
                error_message="Root path is empty.",
                directories=[]
            )

        if not keyword:
            return fws_dir_searcher_dto_search_result.FwsDirSearcherDtoSearchResult(
                is_success=False, 
                error_message="Keyword is empty.",
                directories=[]
            )

        return self.fws_dir_searcher_business_obj.search_directories(root_path, keyword)
