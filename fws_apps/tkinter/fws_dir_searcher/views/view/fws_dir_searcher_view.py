"""
Summary:
    fws_dir_searcher アプリのViewモジュール。
Description:
    UIコンポーネントの配置および初期化を行います（2ペイン構成）。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk

class FwsDirSearcherView(tk.Tk):
    """
    Summary:
        検索アプリのメイン画面となるViewクラス。
    """

    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            ウィンドウの設定と各ウィジェットの配置を行います。
        """
        super().__init__()

        self.title("FWS Directory Searcher")
        self.geometry("1000x600")
        self.minsize(800, 400)

        self._init_ui()

    def _init_ui(self) -> None:
        """
        Summary:
            UIウィジェットを初期化し配置します。
        """
        # --- Top Frame (Input) ---
        frm_top = ttk.Frame(self, padding=10)
        frm_top.pack(side=tk.TOP, fill=tk.X)

        # Root Path
        ttk.Label(frm_top, text="Root Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ent_root_path = ttk.Entry(frm_top, width=60)
        self.ent_root_path.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        self.btn_browse = ttk.Button(frm_top, text="Browse...")
        self.btn_browse.grid(row=0, column=2, sticky=tk.E, pady=2)

        # Keyword
        ttk.Label(frm_top, text="Keyword:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ent_keyword = ttk.Entry(frm_top, width=60)
        self.ent_keyword.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        self.btn_search = ttk.Button(frm_top, text="Search")
        self.btn_search.grid(row=1, column=2, sticky=tk.E, pady=2)
        
        frm_top.columnconfigure(1, weight=1)

        # --- PanedWindow for 2-pane layout ---
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left Pane (Directories)
        frm_left = ttk.Frame(self.paned_window)
        self.paned_window.add(frm_left, weight=1)
        
        ttk.Label(frm_left, text="Matched Directories").pack(side=tk.TOP, anchor=tk.W)
        self.trv_dirs = ttk.Treeview(frm_left, columns=("Path",), selectmode="browse")
        self.trv_dirs.heading("#0", text="Directory Name")
        self.trv_dirs.heading("Path", text="Full Path")
        self.trv_dirs.column("#0", width=200, stretch=tk.NO)
        self.trv_dirs.column("Path", width=300, stretch=tk.YES)
        
        vsb_dirs = ttk.Scrollbar(frm_left, orient="vertical", command=self.trv_dirs.yview)
        hsb_dirs = ttk.Scrollbar(frm_left, orient="horizontal", command=self.trv_dirs.xview)
        self.trv_dirs.configure(yscrollcommand=vsb_dirs.set, xscrollcommand=hsb_dirs.set)
        
        vsb_dirs.pack(side=tk.RIGHT, fill=tk.Y)
        hsb_dirs.pack(side=tk.BOTTOM, fill=tk.X)
        self.trv_dirs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right Pane (Files)
        frm_right = ttk.Frame(self.paned_window)
        self.paned_window.add(frm_right, weight=2)
        
        ttk.Label(frm_right, text="Files in Selected Directory").pack(side=tk.TOP, anchor=tk.W)
        self.trv_files = ttk.Treeview(frm_right, columns=("Size", "Modified", "Path"), selectmode="browse")
        self.trv_files.heading("#0", text="File Name")
        self.trv_files.heading("Size", text="Size (Bytes)")
        self.trv_files.heading("Modified", text="Modified Time")
        self.trv_files.heading("Path", text="Full Path")
        
        self.trv_files.column("#0", width=250, stretch=tk.NO)
        self.trv_files.column("Size", width=100, stretch=tk.NO, anchor=tk.E)
        self.trv_files.column("Modified", width=150, stretch=tk.NO)
        self.trv_files.column("Path", width=200, stretch=tk.YES)
        
        vsb_files = ttk.Scrollbar(frm_right, orient="vertical", command=self.trv_files.yview)
        hsb_files = ttk.Scrollbar(frm_right, orient="horizontal", command=self.trv_files.xview)
        self.trv_files.configure(yscrollcommand=vsb_files.set, xscrollcommand=hsb_files.set)
        
        vsb_files.pack(side=tk.RIGHT, fill=tk.Y)
        hsb_files.pack(side=tk.BOTTOM, fill=tk.X)
        self.trv_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Context Menu Placeholder (for future copy/shortcut functionality)
        self.menu_dirs = tk.Menu(self, tearoff=0)
        self.menu_dirs.add_command(label="Open in Explorer")
        self.menu_dirs.add_separator()
        self.menu_dirs.add_command(label="Copy & Create Shortcut (Future)", state="disabled")

        self.menu_files = tk.Menu(self, tearoff=0)
        self.menu_files.add_command(label="Copy & Create Shortcut (Future)", state="disabled")

        # --- Status Bar ---
        frm_status = ttk.Frame(self, relief=tk.SUNKEN, padding=2)
        frm_status.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbl_status = ttk.Label(frm_status, text="Ready.")
        self.lbl_status.pack(side=tk.LEFT, padx=5)
