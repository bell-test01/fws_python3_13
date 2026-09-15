"""
Summary:
    fws_apps_template_generator 用の定数定義モジュール。
Description:
    ディレクトリ除外リストや、GUI/CLI 用のデフォルトのファイル・フォルダ構成テンプレートを管理します。
Attachment:
    docs_fws_apps_template_generator/final_specification.md
"""
import os

"""list[str] - ユーザー指定の除外リスト"""
EXCLUDE_LIST = [
    "git_structure.txt",
    ".gitkeep",
    "docs_{app_name}",
    "tests"
]

"""list[str] - GUI用テンプレート構造 (プレースホルダー {app_name} を含む)"""
GUI_TEMPLATE_STRUCTURE = [
    "{app_name}.py",
    "README.md",
    "businesses/business/{app_name}_business.py",
    "businesses/dto/{app_name}_dto.py",
    "businesses/entity/{app_name}_entity.py",
    "constant/{app_name}_const.py",
    "data/",
    "output/",
    "views/event/{app_name}_event.py",
    "views/logic/{app_name}_logic.py",
    "views/view/{app_name}_view.py",
]

"""list[str] - CLI用テンプレート構造 (プレースホルダー {app_name} を含む)"""
CLI_TEMPLATE_STRUCTURE = [
    "{app_name}.py",
    "README.md",
    "core/{app_name}_core.py",
    "constant/{app_name}_const.py",
    "data/",
    "output/",
]
