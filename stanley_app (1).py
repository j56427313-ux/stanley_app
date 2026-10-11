"""
Stanley Lubricants - mini katalog va buyurtma ilovasi (Tkinter, yangi dizayn)

Faqat Python standart kutubxonasi: hech narsa o'rnatish shart emas.
Python 3.13 / 3.14 da ishlaydi.

Ishga tushirish:
    python stanley_app.py
"""
from __future__ import annotations

import csv
import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, messagebox, ttk

# ---------- Ma'lumotlar (PDF katalogdan) ----------
P_MOTO = ["1L", "2L", "208L"]
P_STD = ["1L", "4L", "5L", "20L", "208L"]
P_BRAKE = ["250G", "500GM"]
P_GREASE = ["500G", "1KG", "3KG", "15KG", "180KG"]


@dataclass(frozen=True, slots=True)
class Product:
    category: str
    name: str
    viscosity: str
    standard: str
    description: str
    packs: list[str]

    def search_text(self) -> str:
        return " ".join(
            (self.category, self.name, self.viscosity, self.standard, self.description)
        ).lower()


PRODUCTS: list[Product] = [Product(*row) for row in [
    # Mototsikl moylari
    ("Mototsikl moyi", "4T 5500 SAE 25W-60 API SN JASO MA2", "SAE 25W-60", "API SN / JASO MA2",
     "4 taktli mototsikllar uchun sintetik moy. Debriyaj va uzatma qutisini himoya qiladi.", P_MOTO),
    ("Mototsikl moyi", "4T 7000 SAE 15W-50 API SN JASO MA2", "SAE 15W-50", "API SN / JASO MA2",
     "Sintetik 4 taktli moy, yuqori termal va oksidlanish barqarorligi.", P_MOTO),
    ("Mototsikl moyi", "4T 7000 SAE 20W-50 API SN JASO MA2", "SAE 20W-50", "API SN / JASO MA2",
     "Yuqori aylanishli 4 taktli dvigatellar uchun, silindr va klapanlarni yeyilishdan himoya qiladi.", P_MOTO),
    ("Mototsikl moyi", "4T 7000 SAE 10W-40 API SN JASO MA2", "SAE 10W-40", "API SN / JASO MA2",
     "Dvigatel ish faoliyatining optimal balansi, halqa va podshipniklar yeyilishi minimal.", P_MOTO),
    # Dvigatel moylari (benzin)
    ("Dvigatel moyi (benzin)", "SAE 15W-40 API SN", "SAE 15W-40", "API SN",
     "Yengil avtomobillar uchun sintetik moy, uzoq almashtirish oralig'i.", P_STD),
    ("Dvigatel moyi (benzin)", "SAE 5W-30 API SN/CF", "SAE 5W-30", "API SN/CF",
     "Turbo va ko'p klapanli dvigatellar uchun to'liq sintetik moy.", P_STD),
    ("Dvigatel moyi (benzin)", "SAE 5W-40 API SN/CF", "SAE 5W-40", "API SN/CF",
     "To'liq sintetik, qiyin sharoitlar va uzoq almashtirish oralig'i uchun.", P_STD),
    ("Dvigatel moyi (benzin)", "SAE 10W-40 API SN/CF", "SAE 10W-40", "API SN/CF",
     "To'liq sintetik, to'g'ridan-to'g'ri purkashli dvigatellar uchun mos.", P_STD),
    # Dizel
    ("Dizel moyi", "SAE 15W-40 API CI-4/SL", "SAE 15W-40", "API CI-4/SL",
     "Og'ir yuk dizel dvigatellari va EGR tizimli zamonaviy dvigatellar uchun.", P_STD),
    ("Dizel moyi", "SAE 10W-40 API CH-4/SN", "SAE 10W-40", "API CH-4/SN",
     "Yuqori samarali dizel moyi, EGR tizimli dvigatellarga mos.", P_STD),
    ("Dizel moyi", "SAE 10W-30 API CK-4", "SAE 10W-30", "API CK-4",
     "Yangi CK-4 talabidan oshadigan yuqori texnologiyali dizel moyi.", P_STD),
    ("Dizel moyi", "SAE 10W-40 API CK-4", "SAE 10W-40", "API CK-4",
     "Yuqori samarali dizel moyi, sovuqda ham yaxshi oqadi.", P_STD),
    # Transmissiya
    ("Transmissiya", "Gear Oil SAE 80W-90 API GL-5", "SAE 80W-90", "API GL-5",
     "Uzatma qutisi uchun, yeyilish va zanglashdan himoya.", P_STD),
    ("Transmissiya", "Gear Oil SAE 75W-85 API GL-5", "SAE 75W-85", "API GL-5",
     "Premium uzatma moyi, ekstremal bosimga chidamli.", P_STD),
    ("Transmissiya", "ATF Dexron VI", "ATF", "Dexron VI",
     "Universal to'liq sintetik avtomat uzatma suyuqligi.", P_STD),
    ("Transmissiya", "ATF CVT", "CVT", "CVT",
     "Variatorli (CVT) uzatmalar uchun to'liq sintetik suyuqlik.", P_STD),
    # Maxsus
    ("Maxsus mahsulotlar", "Antifreeze Coolant 50%", "50/50", "Glikol asosli",
     "Tayyor aralashma. Nitrit, nitrat, borat va fosfatlarsiz.", P_STD),
    ("Maxsus mahsulotlar", "Antifreeze Coolant 100%", "Konsentrat", "Glikol asosli",
     "Konsentrlangan antifriz, suv bilan aralashtirib ishlatiladi.", P_STD),
    ("Maxsus mahsulotlar", "Brake Fluid DOT 4", "DOT 4", "Poliglikol",
     "Yuqori haroratda ham samarali tormoz suyuqligi.", P_BRAKE),
    ("Maxsus mahsulotlar", "Brake Fluid DOT 3", "DOT 3", "Glikol asosli",
     "Yengil va tijorat transporti uchun tormoz suyuqligi.", P_BRAKE),
    ("Maxsus mahsulotlar", "Lithium EP Grease", "NLGI 3", "Litiyli EP",
     "Sanoat uchun ko'p maqsadli ekstremal bosimli surkov.", P_GREASE),
    ("Maxsus mahsulotlar", "Calcium MP Grease", "NLGI 3", "Kalsiyli MP",
     "Suvga chidamli ko'p maqsadli kalsiyli surkov.", P_GREASE),
    ("Maxsus mahsulotlar", "Hydraulic Oil ISO 68", "ISO 68", "Gidravlik",
     "Mobil texnikaning gidravlik tizimi uchun premium moy.", P_STD),
    ("Maxsus mahsulotlar", "Transmission Oil SAE 10W", "SAE 10W", "Mineral",
     "Yuk ko'targichlar (payloader) dvigateli va gidravlikasi uchun.", ["208L"]),
]]

ALL = "Hammasi"
CATEGORIES = sorted({p.category for p in PRODUCTS})
ALL_PACKS = sorted({pk for p in PRODUCTS for pk in p.packs})

ABOUT_INTRO = (
    "STANLEY Group — BAAda joylashgan neft mahsulotlari kompaniyalari guruhi. "
    "Avtomobil va sanoat moylari, surkovlar, izolyatsion moylar, tormoz suyuqliklari "
    "va maxsus moylarni ishlab chiqaradi. Zavod ISO 9001:2008 sertifikatiga ega, "
    "mahsulotlar ESMA tomonidan tasdiqlangan."
)

ABOUT_COMPANIES = [
    ("Prime Petroleum FZC", "Neftni qayta ishlash zavodi"),
    ("Henkel International Lubricant Industry LLC / FZE", "Moy va baza moy ishlab chiqarish"),
    ("Solar Gulf International FZC", "Moy ishlab chiqarish (ishga tushirilmoqda)"),
    ("Stanley Trading LLC", "Baza moy, qo'shimchalar va moylar savdosi"),
]


# ---------- Dizayn ----------
NAVY = "#12203B"
NAVY_LIGHT = "#1F3358"
ACCENT = "#FFB703"
ACCENT_HOVER = "#FFC933"
BG = "#F2F5FA"
CARD = "#FFFFFF"
BORDER = "#DCE3EE"
TEXT = "#1B2437"
MUTED = "#6B778C"
ZEBRA = "#F7F9FC"

FONT = "Segoe UI"

# kategoriya -> (belgi, chip foni, chip matni)
CAT_STYLE: dict[str, tuple[str, str, str]] = {
    "Mototsikl moyi": ("🏍️", "#FDE7D6", "#B54708"),
    "Dvigatel moyi (benzin)": ("🚗", "#DDEBFF", "#1D4ED8"),
    "Dizel moyi": ("🚛", "#E4E7EC", "#344054"),
    "Transmissiya": ("⚙️", "#EBE2FF", "#6D28D9"),
    "Maxsus mahsulotlar": ("🧪", "#D9F5E5", "#067647"),
}


def setup_style(root: tk.Tk) -> None:
    root.configure(bg=BG)
    root.option_add("*TCombobox*Listbox.font", (FONT, 10))
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", NAVY)

    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure(".", font=(FONT, 10), background=BG, foreground=TEXT)
    s.configure("TFrame", background=BG)
    s.configure("Card.TFrame", background=CARD)
    s.configure("TLabel", background=BG, foreground=TEXT)
    s.configure("Card.TLabel", background=CARD, foreground=TEXT)
    s.configure("Muted.TLabel", background=BG, foreground=MUTED)
    s.configure("CardMuted.TLabel", background=CARD, foreground=MUTED)
    s.configure("Title.TLabel", background=CARD, font=(FONT, 15, "bold"))
    s.configure("H2.TLabel", background=BG, font=(FONT, 14, "bold"))
    s.configure("Count.TLabel", background=BG, foreground=MUTED, font=(FONT, 10, "bold"))

    # Tablar
    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 0, 0, 0))
    s.configure("TNotebook.Tab", padding=(22, 10), font=(FONT, 10, "bold"),
                background="#E3E9F3", foreground=MUTED, borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", CARD), ("active", "#EEF2F9")],
          foreground=[("selected", NAVY)])

    # Maydonlar
    for name in ("TEntry", "TCombobox", "TSpinbox"):
        s.configure(name, fieldbackground=CARD, background=CARD, foreground=TEXT,
                    bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                    padding=(8, 6), arrowcolor=NAVY)
        s.map(name, bordercolor=[("focus", ACCENT)], lightcolor=[("focus", ACCENT)],
              darkcolor=[("focus", ACCENT)])
    s.map("TCombobox", fieldbackground=[("readonly", CARD), ("disabled", "#EEF1F6")],
          foreground=[("disabled", MUTED)])

    # Jadval
    s.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT,
                rowheight=36, borderwidth=0, font=(FONT, 10))
    s.configure("Treeview.Heading", background=NAVY, foreground="white",
                font=(FONT, 10, "bold"), relief="flat", padding=(10, 9))
    s.map("Treeview.Heading", background=[("active", NAVY_LIGHT)])
    s.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", NAVY)])

    s.configure("Vertical.TScrollbar", background="#C9D2E0", troughcolor=BG,
                bordercolor=BG, arrowcolor=NAVY, relief="flat")

    # Tugmalar
    base = dict(font=(FONT, 10, "bold"), padding=(16, 9), borderwidth=0, focuscolor=CARD)
    s.configure("Accent.TButton", background=ACCENT, foreground=NAVY, **base)
    s.map("Accent.TButton",
          background=[("disabled", "#E6E9EF"), ("active", ACCENT_HOVER)],
          foreground=[("disabled", "#9AA4B5")])
    s.configure("Secondary.TButton", background="#E3E9F3", foreground=NAVY, **base)
    s.map("Secondary.TButton", background=[("active", "#D3DCEB")])
    s.configure("Danger.TButton", background="#FDE8E8", foreground="#B42318", **base)
    s.map("Danger.TButton", background=[("active", "#FACACA")])


def chip(parent: tk.Misc, text: str, bg: str, fg: str) -> tk.Label:
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=(FONT, 9, "bold"),
                    padx=10, pady=3)


def card(parent: tk.Misc, **pack_opts: object) -> ttk.Frame:
    """Oq kartochka (yupqa ramka bilan)."""
    box = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    box.pack(**pack_opts)
    inner = ttk.Frame(box, style="Card.TFrame", padding=14)
    inner.pack(fill="both", expand=True)
    return inner


class StanleyApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Stanley Lubricants")
        self.geometry("1120x740")
        self.minsize(960, 620)
        setup_style(self)

        # Buyurtma: (mahsulot nomi, qadoq) -> soni
        self.cart: dict[tuple[str, str], int] = {}
        self.visible: list[Product] = []
        self._toast_job: str | None = None

        self.search_var = tk.StringVar()
        self.cat_var = tk.StringVar(value=ALL)
        self.pack_var = tk.StringVar(value=ALL)
        self.sel_pack_var = tk.StringVar()
        self.qty_var = tk.IntVar(value=1)
        self.count_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.stat_items = tk.StringVar(value="0")
        self.stat_qty = tk.StringVar(value="0")

        self._build_header()
        self._build_status_bar()
        self._build_tabs()
        self._apply_filters()
        self._refresh_cart()

    # ---------- Sarlavha ----------
    def _build_header(self) -> None:
        head = tk.Frame(self, bg=NAVY)
        head.pack(fill="x")
        row = tk.Frame(head, bg=NAVY)
        row.pack(fill="x", padx=22, pady=16)

        tk.Label(row, text="🛢️", bg=NAVY, fg="white", font=(FONT, 28)
                 ).pack(side="left", padx=(0, 14))
        titles = tk.Frame(row, bg=NAVY)
        titles.pack(side="left")
        tk.Label(titles, text="STANLEY OIL & LUBRICANTS", bg=NAVY, fg="white",
                 font=(FONT, 19, "bold")).pack(anchor="w")
        tk.Label(titles, bg=NAVY, fg="#AEB9D0", font=(FONT, 10),
                 text="Your Partner in Progress — Total Reliability With Stanley Lubricants"
                 ).pack(anchor="w")

        self.badge = tk.Label(row, text="", bg=ACCENT, fg=NAVY, cursor="hand2",
                              font=(FONT, 11, "bold"), padx=16, pady=8)
        self.badge.pack(side="right")
        self.badge.bind("<Button-1>", lambda _e: self.tabs.select(self.tab_cart))

        tk.Frame(self, bg=ACCENT, height=4).pack(fill="x")

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self, bg=NAVY)
        bar.pack(side="bottom", fill="x")
        tk.Label(bar, textvariable=self.status_var, bg=NAVY, fg=ACCENT,
                 font=(FONT, 10, "bold"), anchor="w", padx=22, pady=7).pack(side="left")
        tk.Label(bar, text="www.stanleylubricants.com", bg=NAVY, fg="#8C99B3",
                 font=(FONT, 9), padx=22).pack(side="right")

    def _build_tabs(self) -> None:
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=(14, 10))

        self.tab_catalog = ttk.Frame(self.tabs, padding=14)
        self.tab_cart = ttk.Frame(self.tabs, padding=14)
        self.tab_about = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(self.tab_catalog, text="📚  Katalog")
        self.tabs.add(self.tab_cart, text="🛒  Buyurtma")
        self.tabs.add(self.tab_about, text="ℹ️  Kompaniya haqida")

        self._build_catalog()
        self._build_cart()
        self._build_about()

    def _toast(self, text: str) -> None:
        self.status_var.set(text)
        if self._toast_job:
            self.after_cancel(self._toast_job)
        self._toast_job = self.after(3000, lambda: self.status_var.set(""))

    # ---------- Katalog ----------
    def _build_catalog(self) -> None:
        f = self.tab_catalog

        # Filtrlar
        bar = ttk.Frame(f)
        bar.pack(fill="x", pady=(0, 10))

        def labeled(title: str) -> ttk.Frame:
            col = ttk.Frame(bar)
            col.pack(side="left", padx=(0, 14))
            ttk.Label(col, text=title, style="Muted.TLabel").pack(anchor="w")
            return col

        c = labeled("🔍  Qidiruv (5W-30, CK-4, DOT)")
        ttk.Entry(c, textvariable=self.search_var, width=28).pack()
        c = labeled("Kategoriya")
        cat = ttk.Combobox(c, textvariable=self.cat_var, state="readonly", width=22,
                           values=[ALL, *CATEGORIES])
        cat.pack()
        c = labeled("Qadoq hajmi")
        pack = ttk.Combobox(c, textvariable=self.pack_var, state="readonly", width=9,
                            values=[ALL, *ALL_PACKS])
        pack.pack()
        ttk.Button(bar, text="Tozalash", style="Secondary.TButton",
                   command=self._reset_filters).pack(side="left", anchor="s")
        ttk.Label(bar, textvariable=self.count_var, style="Count.TLabel"
                  ).pack(side="right", anchor="s", pady=(0, 8))

        self.search_var.trace_add("write", lambda *_: self._apply_filters())
        cat.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())
        pack.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        # Tanlangan mahsulot kartochkasi (pastda)
        det = card(f, side="bottom", fill="x", pady=(10, 0))
        self.det_top = ttk.Frame(det, style="Card.TFrame")
        self.det_top.pack(side="left", fill="both", expand=True)
        self.d_chips = ttk.Frame(self.det_top, style="Card.TFrame")
        self.d_chips.pack(anchor="w")
        self.d_name = ttk.Label(self.det_top, text="", style="Title.TLabel")
        self.d_name.pack(anchor="w", pady=(6, 2))
        self.d_desc = ttk.Label(self.det_top, text="", style="CardMuted.TLabel",
                                wraplength=640, justify="left")
        self.d_desc.pack(anchor="w")

        right = ttk.Frame(det, style="Card.TFrame")
        right.pack(side="right", padx=(16, 0))
        ttk.Label(right, text="Qadoq", style="CardMuted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(right, text="Soni", style="CardMuted.TLabel").grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.pack_box = ttk.Combobox(right, textvariable=self.sel_pack_var,
                                     state="disabled", width=9)
        self.pack_box.grid(row=1, column=0)
        ttk.Spinbox(right, from_=1, to=9999, textvariable=self.qty_var, width=7
                    ).grid(row=1, column=1, padx=(10, 0))
        self.add_btn = ttk.Button(right, text="＋  Buyurtmaga qo'shish", style="Accent.TButton",
                                  command=self._add_to_cart, state="disabled")
        self.add_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Mahsulotlar jadvali
        mid = tk.Frame(f, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        mid.pack(fill="both", expand=True)
        cols = ("name", "category", "viscosity", "standard")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", selectmode="browse")
        for col, title, w in (("name", "Nomi", 340), ("category", "Kategoriya", 210),
                              ("viscosity", "Yopishqoqlik", 120), ("standard", "Standart", 170)):
            self.tree.heading(col, text=title, anchor="w")
            self.tree.column(col, width=w, anchor="w")
        self.tree.tag_configure("odd", background=ZEBRA)
        self.tree.tag_configure("even", background=CARD)
        sb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda _e: self._add_to_cart())

    def _reset_filters(self) -> None:
        self.search_var.set("")
        self.cat_var.set(ALL)
        self.pack_var.set(ALL)

    def _apply_filters(self) -> None:
        q = self.search_var.get().strip().lower()
        cat, pk = self.cat_var.get(), self.pack_var.get()
        self.visible = [
            p for p in PRODUCTS
            if (cat == ALL or p.category == cat)
            and (pk == ALL or pk in p.packs)
            and (not q or q in p.search_text())
        ]
        self.tree.delete(*self.tree.get_children())
        for i, p in enumerate(self.visible):
            icon = CAT_STYLE.get(p.category, ("", "", ""))[0]
            self.tree.insert("", "end", iid=str(i),
                             tags=("odd" if i % 2 else "even",),
                             values=(p.name, f"{icon}  {p.category}", p.viscosity, p.standard))
        self.count_var.set(f"{len(self.visible)} ta mahsulot topildi")
        self._clear_details()

    def _set_chips(self, items: list[tuple[str, str, str]]) -> None:
        for w in self.d_chips.winfo_children():
            w.destroy()
        for text, bg, fg in items:
            chip(self.d_chips, text, bg, fg).pack(side="left", padx=(0, 6))

    def _clear_details(self) -> None:
        self._set_chips([])
        self.d_name.config(text="Ro'yxatdan mahsulot tanlang")
        self.d_desc.config(text="Mahsulotni bosing, qadoq va sonini tanlab buyurtmaga qo'shing "
                                "(ikki marta bosish ham qo'shadi).")
        self.sel_pack_var.set("")
        self.pack_box.config(values=[], state="disabled")
        self.add_btn.config(state="disabled")

    def _selected(self) -> Product | None:
        sel = self.tree.selection()
        return self.visible[int(sel[0])] if sel else None

    def _on_select(self, _event: object = None) -> None:
        p = self._selected()
        if p is None:
            return
        icon, bg, fg = CAT_STYLE.get(p.category, ("", "#E4E7EC", "#344054"))
        self._set_chips([
            (f"{icon} {p.category}", bg, fg),
            (p.viscosity, "#E3E9F3", NAVY),
            (p.standard, "#E3E9F3", NAVY),
        ])
        self.d_name.config(text=p.name)
        self.d_desc.config(text=p.description)
        self.pack_box.config(values=p.packs, state="readonly")
        self.sel_pack_var.set(p.packs[0])
        self.qty_var.set(1)
        self.add_btn.config(state="normal")

    def _add_to_cart(self) -> None:
        p = self._selected()
        if p is None:
            return
        try:
            qty = int(self.qty_var.get())
        except (tk.TclError, ValueError):
            qty = 0
        if qty < 1:
            messagebox.showwarning("Soni noto'g'ri", "Soni kamida 1 bo'lishi kerak.")
            return
        pack = self.sel_pack_var.get()
        key = (p.name, pack)
        self.cart[key] = self.cart.get(key, 0) + qty
        self._refresh_cart()
        self._toast(f"✔  Qo'shildi: {p.name}  ({pack} × {qty})")

    # ---------- Buyurtma ----------
    def _build_cart(self) -> None:
        f = self.tab_cart
        ttk.Label(f, text="Buyurtma ro'yxati", style="H2.TLabel").pack(anchor="w", pady=(0, 10))

        stats = ttk.Frame(f)
        stats.pack(fill="x", pady=(0, 12))
        for title, var in (("Pozitsiyalar", self.stat_items), ("Jami dona", self.stat_qty)):
            box = tk.Frame(stats, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", padx=(0, 12))
            inner = ttk.Frame(box, style="Card.TFrame", padding=(18, 10))
            inner.pack()
            ttk.Label(inner, text=title, style="CardMuted.TLabel").pack(anchor="w")
            tk.Label(inner, textvariable=var, bg=CARD, fg=NAVY,
                     font=(FONT, 22, "bold")).pack(anchor="w")

        btns = ttk.Frame(f)
        btns.pack(side="bottom", fill="x", pady=(12, 0))
        ttk.Button(btns, text="⬇  CSV saqlash", style="Accent.TButton",
                   command=self._export_csv).pack(side="left")
        ttk.Button(btns, text="Tanlanganni o'chirish", style="Secondary.TButton",
                   command=self._remove_selected).pack(side="left", padx=10)
        ttk.Button(btns, text="🗑  Tozalash", style="Danger.TButton",
                   command=self._clear_cart).pack(side="left")

        mid = tk.Frame(f, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        mid.pack(fill="both", expand=True)
        self.cart_tree = ttk.Treeview(mid, columns=("name", "pack", "qty"),
                                      show="headings", selectmode="extended")
        for col, title, w in (("name", "Mahsulot", 520), ("pack", "Qadoq", 110),
                              ("qty", "Soni", 90)):
            self.cart_tree.heading(col, text=title, anchor="w" if col == "name" else "center")
            self.cart_tree.column(col, width=w, anchor="w" if col == "name" else "center")
        self.cart_tree.tag_configure("odd", background=ZEBRA)
        self.cart_tree.tag_configure("even", background=CARD)
        sb = ttk.Scrollbar(mid, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=sb.set)
        self.cart_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.empty_lbl = tk.Label(mid, text="🛒\n\nHozircha bo'sh.\nKatalogdan mahsulot qo'shing.",
                                  bg=CARD, fg=MUTED, font=(FONT, 12), justify="center")

    def _refresh_cart(self) -> None:
        self.cart_tree.delete(*self.cart_tree.get_children())
        for i, ((name, pack), qty) in enumerate(self.cart.items()):
            self.cart_tree.insert("", "end", iid=str(i), tags=("odd" if i % 2 else "even",),
                                  values=(name, pack, qty))
        n, total = len(self.cart), sum(self.cart.values())
        self.stat_items.set(str(n))
        self.stat_qty.set(str(total))
        self.tabs.tab(self.tab_cart, text=f"🛒  Buyurtma ({n})" if n else "🛒  Buyurtma")
        self.badge.config(text=f"🛒  {n} pozitsiya · {total} dona" if n else "🛒  Buyurtma bo'sh")
        if n:
            self.empty_lbl.place_forget()
        else:
            self.empty_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def _remove_selected(self) -> None:
        keys = list(self.cart)
        for iid in self.cart_tree.selection():
            self.cart.pop(keys[int(iid)], None)
        self._refresh_cart()

    def _clear_cart(self) -> None:
        if self.cart and messagebox.askyesno("Tozalash", "Butun buyurtma o'chirilsinmi?"):
            self.cart.clear()
            self._refresh_cart()

    def _export_csv(self) -> None:
        if not self.cart:
            messagebox.showinfo("Bo'sh", "Buyurtma bo'sh.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", initialfile="stanley_buyurtma.csv",
            filetypes=[("CSV fayl", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:  # Excel uchun BOM
            w = csv.writer(fh)
            w.writerow(["Mahsulot", "Qadoq", "Soni"])
            for (name, pack), qty in self.cart.items():
                w.writerow([name, pack, qty])
        self._toast(f"✔  Saqlandi: {path}")

    # ---------- Kompaniya ----------
    def _build_about(self) -> None:
        c = card(self.tab_about, fill="x", anchor="n")
        ttk.Label(c, text="Stanley Group", style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(c, text=ABOUT_INTRO, style="Card.TLabel", wraplength=980, justify="left"
                  ).pack(anchor="w")

        ttk.Label(self.tab_about, text="Guruh kompaniyalari", style="H2.TLabel"
                  ).pack(anchor="w", pady=(16, 8))
        for title, desc in ABOUT_COMPANIES:
            row = card(self.tab_about, fill="x", pady=(0, 8))
            ttk.Label(row, text=title, style="Card.TLabel", font=(FONT, 10, "bold")).pack(anchor="w")
            ttk.Label(row, text=desc, style="CardMuted.TLabel").pack(anchor="w")

        contact = tk.Frame(self.tab_about, bg=NAVY)
        contact.pack(fill="x", pady=(8, 0))
        tk.Label(contact, bg=NAVY, fg="white", font=(FONT, 10), justify="left", padx=18, pady=12,
                 text="📞  Dubai ofisi: +971-4-2272425    ·    Faks: +971-4-2233189\n"
                      "🌐  www.stanleylubricants.com").pack(anchor="w")


if __name__ == "__main__":
    try:  # Windows'da aniq (blur emas) matn uchun
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    StanleyApp().mainloop()
