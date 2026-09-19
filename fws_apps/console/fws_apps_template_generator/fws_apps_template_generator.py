"""
Summary:
    FWSアプリテンプレートジェネレータのエントリポイントモジュール。
Description:
    コマンドライン引数をパースし、FwsAppsTemplateGeneratorCoreを呼び出して、ファイル・フォルダ構成を自動生成します。
Attachment:
    docs_fws_apps_template_generator/final_specification.md
"""
import argparse
import sys
from pathlib import Path

from core.fws_apps_template_generator_core import FwsAppsTemplateGeneratorCore


def main():
    """
    Summary:
        fws_apps_template_generator のエントリポイントメソッド。
    Description:
        コマンドライン引数をパースし、指定された条件に基づいてfwsプロジェクトのファイル構成を生成します。
    Args:
        None
    Returns:
        None - 戻り値なし。
    """
    # ヘルプメッセージや使用例を見やすくするための設定
    description_text: str = (
        "=========================================\n"
        " FWS Apps Template Generator\n"
        "=========================================\n"
        "fwsプロジェクトのファイル・フォルダ構成を自動生成するツールです。\n"
        "GUI/CLIのテンプレート展開、または git_structure.txt からの生成をサポートします。"
    )
    epilog_text: str = (
        "【使用例】\n"
        "  # GUIテンプレートを使ってアプリを生成する場合\n"
        "  python fws_apps_template_generator.py -p ./my_new_app -n my_new_app\n\n"
        "  # CLIテンプレートを使ってアプリを生成する場合\n"
        "  python fws_apps_template_generator.py -p ./my_cli_app -n my_cli_app -t cli\n\n"
        "  # git_structure.txt から構成を生成する場合\n"
        "  python fws_apps_template_generator.py -p ./custom_app -n custom_app -f ./git_structure.txt"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=description_text,
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-p", "--path", required=True, help="出力先ディレクトリのルートパス (必須)")
    parser.add_argument("-n", "--app-name", required=True, help="アプリケーション名（例: fws_sample_app） (必須)")
    parser.add_argument("-f", "--file", help="読み込む構造定義ファイル (git_structure.txt等)")
    parser.add_argument("-t", "--type", choices=["gui", "cli"], default="gui", help="生成するテンプレートの種類 (デフォルト: gui)")

    # 引数なしで実行された場合はヘルプを表示して終了
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    # 出力先パスの検証と作成
    output_path: Path = Path(args.path).resolve()
    if not output_path.exists():
        print(f"Creating output root directory: {output_path}")
        output_path.mkdir(parents=True, exist_ok=True)

    fws_apps_template_generator_core_obj: FwsAppsTemplateGeneratorCore = FwsAppsTemplateGeneratorCore(
        output_path=str(output_path),
        app_name=args.app_name,
        template_type=args.type
    )

    try:
        if args.file:
            fws_apps_template_generator_core_obj.generate_from_structure_file(args.file)
        else:
            fws_apps_template_generator_core_obj.generate_from_template()
        print("Generation completed successfully.")
    except Exception as e:
        print(f"Error during generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
