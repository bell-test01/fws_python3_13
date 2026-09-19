"""
Summary:
    テンプレート構成からファイルやディレクトリを生成するコアロジックモジュール。
Description:
    GUI/CLI の標準テンプレートや、git_structure.txt などの構造定義ファイルから
    ディレクトリおよび空ファイル群を生成する役割を持ちます。
Attachment:
    docs_fws_apps_template_generator/final_specification.md
"""
import re
from pathlib import Path

from constant import fws_apps_template_generator_const as const


class FwsAppsTemplateGeneratorCore:
    """
    Summary:
        ファイルおよびディレクトリ構成の自動生成を行うコアクラス。
    Description:
        定数に定義されたテンプレート構成（GUI/CLI）、または
        git_structure.txt などのツリー構造ファイルからパスを読み取り、
        指定された出力先ディレクトリに実体（空ファイル/ディレクトリ）を作成します。
    """
    # region Constructor
    def __init__(self, output_path: str, app_name: str, template_type: str = "gui") -> None:
        """
        Summary:
            クラスの初期化を行います。
        Args:
            output_path: str - 出力先ディレクトリのパス。
            app_name: str - アプリケーション名。
            template_type: str - テンプレートの種類 ("gui" または "cli")。
        Returns:
            None - 戻り値なし。
        """
        self.output_path = Path(output_path).resolve()
        self.app_name = app_name
        self.template_type: str = template_type
    # endregion

    # region Public Methods
    def generate_from_template(self) -> None:
        """
        Summary:
            定数 (const) に定義されたテンプレートからファイル構成を生成します。
        Description:
            インスタンス生成時に指定された `template_type` (gui または cli) に応じて
            展開する構成を切り替え、プレースホルダー `{app_name}` を置換しながら出力します。
        Args:
            None
        Returns:
            None - 戻り値なし。
        """
        if self.template_type == "cli":
            template: list[str] = const.CLI_TEMPLATE_STRUCTURE
        else:
            template: list[str] = const.GUI_TEMPLATE_STRUCTURE

        print(f"Generating {self.template_type} template for {self.app_name} at {self.output_path}")

        for item in template:
            # プレースホルダーを置換
            rel_path: str = item.replace("{app_name}", self.app_name)
            
            if self._is_excluded(rel_path):
                continue

            full_path: Path = self.output_path / rel_path

            if rel_path.endswith("/"):
                # ディレクトリ
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {full_path}")
            else:
                # ファイル
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch(exist_ok=True)
                print(f"Created file: {full_path}")

    def generate_from_structure_file(self, file_path: str) -> None:
        """
        Summary:
            ツリー形式のテキストファイルからファイル構成を生成します。
        Description:
            git_structure.txt などの形式で書かれたファイルパス一覧を読み取り、
            ディレクトリ階層を計算しながら生成処理を行います。
        Args:
            file_path: str - 読み込む構造定義ファイルのパス。
        Returns:
            None - 戻り値なし。
        """
        structure_file: Path = Path(file_path).resolve()
        if not structure_file.exists():
            raise FileNotFoundError(f"Structure file not found: {structure_file}")
            
        print(f"Generating from structure file {structure_file} at {self.output_path}")

        with open(structure_file, 'r', encoding='utf-8') as f:
            lines: list[str] = f.readlines()

        # ツリー構造のパース用スタック
        # (レベル, Path) のタプルを保持
        stack: list[tuple[int, Path]] = []

        for line in lines:
            line = line.rstrip('\n')
            if not line.strip():
                continue

            # 行の先頭から、ツリーのインデント部分と要素名を分離
            # ├──, └──, │   などの文字とスペースをマッチさせる
            match: re.Match[str] | None = re.match(r'^([│├└─\s]*)(.*)$', line)
            if not match:
                continue

            indent: str
            name: str
            indent, name = match.groups()
            name = name.strip()
            if not name:
                continue
                
            # 文字幅からレベルを計算 (通常4文字単位)
            # ただし、最初のルート要素はインデントなし
            level: int = len(indent) // 4
            
            # ルートディレクトリ名自体も置換（もし {app_name}等が含まれていれば）
            # 基本的には git_structure.txt の内容はそのまま使う
            
            # ディレクトリかどうかの判定 (末尾が / )
            is_dir: bool = name.endswith('/')
            if is_dir:
                name = name[:-1]

            # スタックの調整
            while stack and stack[-1][0] >= level:
                stack.pop()

            current_path: Path
            if not stack:
                # ルート要素
                current_path = self.output_path / name
            else:
                # 親パスに連結
                parent_path: Path = stack[-1][1]
                current_path = parent_path / name

            # 除外判定
            # ルートパスからの相対パスで判定する
            try:
                rel_from_root = current_path.relative_to(self.output_path)
                if self._is_excluded(str(rel_from_root).replace('\\', '/')):
                    continue
            except ValueError:
                pass

            if is_dir:
                current_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {current_path}")
                stack.append((level, current_path))
            else:
                current_path.parent.mkdir(parents=True, exist_ok=True)
                current_path.touch(exist_ok=True)
                print(f"Created file: {current_path}")
                # ファイルは子を持たないのでスタックに積まない
    # endregion

    # region Private Methods
    def _is_excluded(self, path_str: str) -> bool:
        """
        Summary:
            除外リストに含まれるパスかどうかを判定します。
        Description:
            プレースホルダーを置換したパスが、設定された除外リストのいずれかに一致するか確認します。
        Args:
            path_str: str - 判定対象の相対パス。
        Returns:
            bool - 除外対象であれば True、そうでなければ False。
        """
        for exclude in const.EXCLUDE_LIST:
            # プレースホルダーを置換
            resolved_exclude: str = exclude.replace("{app_name}", self.app_name)
            # パスの一部に除外文字列が含まれていればTrue（簡易的な判定）
            # ただし厳密にはパスの各要素と比較する方が安全
            parts: tuple[str, ...] = Path(path_str).parts
            if resolved_exclude in parts:
                return True
        return False
    # endregion
