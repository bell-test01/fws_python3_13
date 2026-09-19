"""
Summary:
    fws_dir_searcher アプリのイベントモジュール。
Description:
    UIイベントのバインドおよび処理呼び出しを行います。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from pathlib import Path
from typing import Dict, List

from fws_apps.tkinter.fws_dir_searcher.views.view import fws_dir_searcher_view
from fws_apps.tkinter.fws_dir_searcher.views.logic import fws_dir_searcher_logic
from fws_apps.tkinter.fws_dir_searcher.businesses.dto.fws_dir_searcher_dto_search_result import FwsDirSearcherDtoDirInfo

class FwsDirSearcherEvent:
    """
    Summary:
        イベントハンドラクラス。
    """

    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各クラスを生成し、イベントを紐付けます。
        """
        self.fws_dir_searcher_view_obj: fws_dir_searcher_view.FwsDirSearcherView = fws_dir_searcher_view.FwsDirSearcherView()
        """fws_dir_searcher_view.FwsDirSearcherView - ビューオブジェクト"""
        
        self.fws_dir_searcher_logic_obj: fws_dir_searcher_logic.FwsDirSearcherLogic = fws_dir_searcher_logic.FwsDirSearcherLogic()
        """fws_dir_searcher_logic.FwsDirSearcherLogic - ロジックオブジェクト"""

        self._cached_results: Dict[str, FwsDirSearcherDtoDirInfo] = {}
        """Dict[str, FwsDirSearcherDtoDirInfo] - 左ペインで選択した際に中身を表示するためのキャッシュ"""

        self._bind_events()

    def _bind_events(self) -> None:
        """
        Summary:
            UIイベントをバインドします。
        """
        self.fws_dir_searcher_view_obj.btn_browse.config(command=self.btn_browse_click)
        self.fws_dir_searcher_view_obj.btn_search.config(command=self.btn_search_click)
        self.fws_dir_searcher_view_obj.ent_keyword.bind("<Return>", lambda e: self.btn_search_click())
        
        # Treeview selection
        self.fws_dir_searcher_view_obj.trv_dirs.bind("<<TreeviewSelect>>", self.trv_dirs_select)
        
        # Double click to open
        self.fws_dir_searcher_view_obj.trv_dirs.bind("<Double-1>", self.trv_dirs_double_click)
        self.fws_dir_searcher_view_obj.trv_files.bind("<Double-1>", self.trv_files_double_click)

        # Context menu
        self.fws_dir_searcher_view_obj.trv_dirs.bind("<Button-3>", self.show_dirs_context_menu)
        self.fws_dir_searcher_view_obj.trv_files.bind("<Button-3>", self.show_files_context_menu)

        self.fws_dir_searcher_view_obj.protocol("WM_DELETE_WINDOW", self.win_main_close)

    def btn_browse_click(self) -> None:
        """
        Summary:
            Browseボタンクリック時の処理。
        """
        selected_dir = filedialog.askdirectory(title="Select Root Directory")
        if selected_dir:
            self.fws_dir_searcher_view_obj.ent_root_path.delete(0, tk.END)
            self.fws_dir_searcher_view_obj.ent_root_path.insert(0, selected_dir)

    def btn_search_click(self) -> None:
        """
        Summary:
            Searchボタンクリック時の処理。
        """
        root_path = self.fws_dir_searcher_view_obj.ent_root_path.get().strip()
        keyword = self.fws_dir_searcher_view_obj.ent_keyword.get().strip()

        self._set_status("Searching...")
        self.fws_dir_searcher_view_obj.update() # UI更新

        result = self.fws_dir_searcher_logic_obj.perform_search(root_path, keyword)

        if not result.is_success:
            self._set_status(f"Error: {result.error_message}", True)
            return

        self._update_dirs_list(result.directories)
        self._clear_files_list()
        self._set_status(f"Found {len(result.directories)} directories in {result.execution_time_ms:.2f} ms")

    def trv_dirs_select(self, event: tk.Event) -> None:
        """
        Summary:
            左ペインでディレクトリが選択された時の処理。
        """
        trv = self.fws_dir_searcher_view_obj.trv_dirs
        selection = trv.selection()
        if not selection:
            return

        item_id = selection[0]
        dir_info = self._cached_results.get(item_id)
        if dir_info:
            self._update_files_list(dir_info)

    def trv_dirs_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            左ペインのディレクトリをダブルクリックした時の処理。
        """
        self._open_selected_item(self.fws_dir_searcher_view_obj.trv_dirs, "Path")

    def trv_files_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            右ペインのファイルをダブルクリックした時の処理。
        """
        self._open_selected_item(self.fws_dir_searcher_view_obj.trv_files, "Path")

    def _open_selected_item(self, trv: tk.ttk.Treeview, path_col: str) -> None:
        """
        Summary:
            Treeviewで選択されているアイテムのパスをエクスプローラーで開きます。
        """
        selection = trv.selection()
        if not selection:
            return
            
        item_id = selection[0]
        values = trv.item(item_id, "values")
        if not values:
            return
            
        # path_col は表示上のカラム名なので、インデックスを取得
        columns = trv["columns"]
        try:
            path_idx = columns.index(path_col)
            target_path = values[path_idx]
            if os.path.exists(target_path):
                # Windows
                os.startfile(target_path)
        except ValueError:
            pass

    def show_dirs_context_menu(self, event: tk.Event) -> None:
        """
        Summary:
            左ペインのコンテキストメニュー表示。
        """
        item = self.fws_dir_searcher_view_obj.trv_dirs.identify_row(event.y)
        if item:
            self.fws_dir_searcher_view_obj.trv_dirs.selection_set(item)
            menu = self.fws_dir_searcher_view_obj.menu_dirs
            # Update menu command dynamically
            menu.entryconfigure("Open in Explorer", command=lambda: self._open_selected_item(self.fws_dir_searcher_view_obj.trv_dirs, "Path"))
            menu.post(event.x_root, event.y_root)

    def show_files_context_menu(self, event: tk.Event) -> None:
        """
        Summary:
            右ペインのコンテキストメニュー表示。
        """
        item = self.fws_dir_searcher_view_obj.trv_files.identify_row(event.y)
        if item:
            self.fws_dir_searcher_view_obj.trv_files.selection_set(item)
            menu = self.fws_dir_searcher_view_obj.menu_files
            menu.post(event.x_root, event.y_root)

    def _update_dirs_list(self, dirs: List[FwsDirSearcherDtoDirInfo]) -> None:
        """
        Summary:
            左ペインのTreeviewを更新します。
        """
        trv = self.fws_dir_searcher_view_obj.trv_dirs
        for item in trv.get_children():
            trv.delete(item)
            
        self._cached_results.clear()

        for idx, dir_info in enumerate(dirs):
            iid = f"dir_{idx}"
            self._cached_results[iid] = dir_info
            tag = "even" if idx % 2 == 0 else "odd"
            trv.insert("", tk.END, iid=iid, text=dir_info.dir_name, values=(dir_info.absolute_path,), tags=(tag,))

    def _update_files_list(self, dir_info: FwsDirSearcherDtoDirInfo) -> None:
        """
        Summary:
            右ペインのTreeviewを更新します。
        """
        trv = self.fws_dir_searcher_view_obj.trv_files
        self._clear_files_list()

        for idx, file_info in enumerate(dir_info.files):
            tag = "even" if idx % 2 == 0 else "odd"
            trv.insert("", tk.END, text=file_info.name, values=(
                file_info.size_bytes,
                file_info.modified_time,
                file_info.absolute_path
            ), tags=(tag,))

    def _clear_files_list(self) -> None:
        """
        Summary:
            右ペインをクリアします。
        """
        trv = self.fws_dir_searcher_view_obj.trv_files
        for item in trv.get_children():
            trv.delete(item)

    def _set_status(self, msg: str, is_error: bool = False) -> None:
        """
        Summary:
            ステータスラベルのメッセージを更新します。
        """
        lbl = self.fws_dir_searcher_view_obj.lbl_status
        lbl.config(text=msg)
        if is_error:
            lbl.config(foreground="red")
        else:
            lbl.config(foreground="black")

    def win_main_close(self) -> None:
        """
        Summary:
            ウィンドウ終了時の処理。
        """
        self.fws_dir_searcher_view_obj.destroy()
