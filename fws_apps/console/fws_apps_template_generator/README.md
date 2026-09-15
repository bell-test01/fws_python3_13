# fws_apps_template_generator

## 概要
`fws_apps_template_generator` は、fwsプロジェクトの新規アプリケーション開発用ファイル・ディレクトリ構成を自動生成するコンソールアプリです。
事前に定義された GUI / CLI の標準構成を展開できるほか、テキストベースの構造定義ファイル (`git_structure.txt` 等) を読み込んで任意の構成を展開することができます。

## 使い方

```powershell
# ヘルプと使い方を表示
python fws_apps_template_generator.py -h

# 指定したパスにGUIアプリ用のテンプレートを展開する（デフォルト）
python fws_apps_template_generator.py -p ./my_gui_app -n my_gui_app

# 指定したパスにCLIアプリ用のテンプレートを展開する
python fws_apps_template_generator.py -p ./my_cli_app -n my_cli_app -t cli

# 既存の git_structure.txt などの構造定義ファイルを元に展開する
python fws_apps_template_generator.py -p ./custom_app -n custom_app -f ./path/to/git_structure.txt
```

詳細は `docs_fws_apps_template_generator/final_specification.md` を参照してください。
