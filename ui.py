"""
Page Replacement Simulator - Kullanıcı Arayüzü (UI)
---------------------------------------------------
Bu modül, CustomTkinter kütüphanesi kullanarak modern ve sade
bir koyu temalı masaüstü arayüzü sunar.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from simulator_bridge import run_algorithm


class PageReplacementUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Temel Pencere Ayarları ---
        self.title("Page Replacement Simulator")
        self.geometry("980x760")
        self.minsize(850, 650)

        # Koyu tema ve modern mor/lila renk paleti
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#171321")

        # Arayüz bileşenlerini oluştur
        self._build_header()
        self._build_input_section()
        self._build_summary_section()
        self._build_table_section()

    # ARAYÜZ BÖLÜMLERİ (WIDGET BUILDERS)

    def _build_header(self):
        # Üst kısımdaki başlık ve açıklama alanını oluşturduk
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Sayfa Değiştirme Algoritması Simülasyonu",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#F5F3FF"
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="İşletim Sistemleri Dersi — FIFO, LRU, Optimal ve Second Chance Simülasyonu",
            font=ctk.CTkFont(size=13),
            text_color="#C4B5FD"
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

    def _build_input_section(self):
        # Kullanıcıdan girdileri alan kısım (Koyu mürdüm / mor kart)
        input_card = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="#251D35",
            border_width=1,
            border_color="#36294C"
        )
        input_card.pack(fill="x", padx=25, pady=10)

        # Sayfa Referans Dizisinin girileceği alan
        ref_label = ctk.CTkLabel(
            input_card,
            text="Sayfa Referans Dizisi (Virgül veya boşluk ile ayırın):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#DDD6FE"
        )
        ref_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 5))

        self.ref_entry = ctk.CTkEntry(
            input_card,
            placeholder_text="Örn: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3 veya 7 0 1 2 0 3",
            font=ctk.CTkFont(size=13),
            height=36,
            fg_color="#1B1427",
            border_color="#3E2E5B",
            text_color="#F5F3FF",
            placeholder_text_color="#7E7294"
        )
        self.ref_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(15, 10), pady=(0, 15))

        # Daha kolay test edebilmek için örnek doldurma butonu
        sample_btn = ctk.CTkButton(
            input_card,
            text="Örnek Değer Doldur",
            width=150,
            height=36,
            fg_color="#3B2D54",
            hover_color="#4C3A6D",
            text_color="#E9D5FF",
            command=self._fill_sample_data
        )
        sample_btn.grid(row=1, column=2, sticky="e", padx=(0, 15), pady=(0, 15))

        # 2. satırdaki algoritma seçme kısmı vs.
        params_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        params_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=(0, 15))

        # Frame yani pencere sayısının girileceği alan
        frame_box = ctk.CTkFrame(params_frame, fg_color="transparent")
        frame_box.pack(side="left", padx=(0, 20))

        frame_label = ctk.CTkLabel(
            frame_box,
            text="Çerçeve (Frame) Sayısı:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#DDD6FE"
        )
        frame_label.pack(anchor="w")

        self.frames_entry = ctk.CTkEntry(
            frame_box,
            width=120,
            height=36,
            placeholder_text="Örn: 3",
            fg_color="#1B1427",
            border_color="#3E2E5B",
            text_color="#F5F3FF",
            placeholder_text_color="#7E7294"
        )
        self.frames_entry.insert(0, "3")
        self.frames_entry.pack(anchor="w", pady=(3, 0))

        # Algoritma Seçimi
        algo_box = ctk.CTkFrame(params_frame, fg_color="transparent")
        algo_box.pack(side="left", padx=(0, 20))

        algo_label = ctk.CTkLabel(
            algo_box,
            text="Algoritma:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#DDD6FE"
        )
        algo_label.pack(anchor="w")

        self.algo_menu = ctk.CTkOptionMenu(
            algo_box,
            values=["FIFO", "LRU", "Optimal", "Second Chance"],
            width=170,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color="#302543",
            button_color="#8B5CF6",
            button_hover_color="#7C3AED",
            dropdown_fg_color="#251D35",
            dropdown_hover_color="#3B2D54",
            dropdown_text_color="#F5F3FF",
            text_color="#F5F3FF"
        )
        self.algo_menu.set("FIFO")
        self.algo_menu.pack(anchor="w", pady=(3, 0))

        # Çalıştır Butonu (Canlı ama göz yormayan mor)
        sim_btn = ctk.CTkButton(
            params_frame,
            text="Çalıştır",
            width=180,
            height=36,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            text_color="#FFFFFF",
            command=self._on_simulate_click
        )
        sim_btn.pack(side="right", pady=(20, 0))

        input_card.grid_columnconfigure(0, weight=1)

        # Hata Bildirim Çubuğu (Kırmızı uyarı rengi korunmuştur)
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F87171"
        )
        self.error_label.pack(fill="x", padx=25, pady=(0, 5))

    def _build_summary_section(self):
        # Toplam Page Fault, Hit ve istatistik kartlarını oluşturur
        self.summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_frame.pack(fill="x", padx=25, pady=(0, 10))

        # 4 Adet özet kartı: Toplam İstek (Lila), Page Faults (Kırmızı), Hits (Yeşil), Hit Oranı (Mor)
        self.card_total = self._create_metric_card(self.summary_frame, "Toplam İstek", "0", "#C4B5FD")
        self.card_total.pack(side="left", expand=True, fill="both", padx=(0, 8))

        self.card_faults = self._create_metric_card(self.summary_frame, "Sayfa Hataları", "0", "#EF4444")
        self.card_faults.pack(side="left", expand=True, fill="both", padx=8)

        self.card_hits = self._create_metric_card(self.summary_frame, "Sayfa İsabetleri", "0", "#10B981")
        self.card_hits.pack(side="left", expand=True, fill="both", padx=8)

        self.card_ratio = self._create_metric_card(self.summary_frame, "İsabet Oranı", "%0.0", "#A78BFA")
        self.card_ratio.pack(side="left", expand=True, fill="both", padx=(8, 0))

    def _create_metric_card(self, parent, title: str, initial_value: str, accent_color: str):
        # Şık bir metrik bilgi kartı üretir (Koyu mürdüm panel)
        card = ctk.CTkFrame(
            parent,
            corner_radius=8,
            fg_color="#251D35",
            border_width=1,
            border_color="#36294C"
        )

        title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11), text_color="#A79FB8")
        title_lbl.pack(pady=(10, 2))

        val_lbl = ctk.CTkLabel(card, text=initial_value, font=ctk.CTkFont(size=20, weight="bold"), text_color=accent_color)
        val_lbl.pack(pady=(0, 10))

        # Değeri sonradan güncelleyebilmek için etiketi card nesnesine bağlıyoruz
        card.value_label = val_lbl
        return card

    def _build_table_section(self):
        """Simülasyon adımlarını gösteren tablo alanını oluşturur."""
        table_container = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="#251D35",
            border_width=1,
            border_color="#36294C"
        )
        table_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Tablo Başlığı
        table_header_box = ctk.CTkFrame(table_container, fg_color="transparent")
        table_header_box.pack(fill="x", padx=15, pady=(12, 8))

        section_title = ctk.CTkLabel(
            table_header_box,
            text="Simülasyon Adımları ve Bellek Durumu",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#DDD6FE"
        )
        section_title.pack(side="left")

        self.status_info_label = ctk.CTkLabel(
            table_header_box,
            text="Simülasyonu başlatmak için yukarıdaki 'Çalıştır' butonuna tıklayın.",
            font=ctk.CTkFont(size=12),
            text_color="#A79FB8"
        )
        self.status_info_label.pack(side="right")

        # Kaydırılabilir Tablo Çerçevesi (Koyu mor zemin ve uyumlu scrollbar)
        self.scroll_table = ctk.CTkScrollableFrame(
            table_container,
            corner_radius=6,
            fg_color="#1D172A",
            scrollbar_button_color="#3B2D54",
            scrollbar_button_hover_color="#4C3A6D"
        )
        self.scroll_table.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # KULLANICI ETKİLEŞİMİ VE DOĞRULAMA

    def _fill_sample_data(self):
        #Test için örnek girdi değerlerini doldurur
        self.ref_entry.delete(0, tk.END)
        self.ref_entry.insert(0, "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1")
        self.frames_entry.delete(0, tk.END)
        self.frames_entry.insert(0, "3") #örnek çerçeve sayısı
        self.error_label.configure(text="")

    def _parse_inputs(self):
        #Kullanıcı girdilerini doğrular ve uygun Python türlerine dönüştürür.
        #Hata durumunda anlaşılır bir ValueError fırlatır.

        # Reference string doğrulaması
        raw_ref = self.ref_entry.get().strip()
        if not raw_ref:
            raise ValueError("Lütfen 'Sayfa Referans Dizisi' alanına sayfa numaraları giriniz.")

        # Virgül ve boşlukları ayır
        tokens = raw_ref.replace(",", " ").split()
        if not tokens:
            raise ValueError("Sayfa referans dizisi geçerli sayı içermiyor.")

        reference_string = []
        for token in tokens:
            if not token.isdigit():
                raise ValueError(
                    f"Geçersiz sayfa değeri: '{token}'!\n"
                    "Sayfa referansları yalnızca pozitif tam sayılardan (örn: 0, 1, 2, 7) oluşmalıdır."
                )
            reference_string.append(int(token))

        # 2. Number of Frames doğrulaması
        raw_frames = self.frames_entry.get().strip()
        if not raw_frames:
            raise ValueError("Lütfen 'Çerçeve Sayısı' alanını doldurunuz.")

        if not raw_frames.isdigit():
            raise ValueError(
                f"Geçersiz çerçeve sayısı: '{raw_frames}'!\n"
                "Çerçeve sayısı pozitif bir tam sayı olmalıdır (örn: 3 veya 4)."
            )

        capacity = int(raw_frames)
        if capacity <= 0:
            raise ValueError("Çerçeve sayısı en az 1 olmalıdır.")

        # 3. Algoritma seçimi
        algorithm_name = self.algo_menu.get().strip()

        return capacity, reference_string, algorithm_name

    def _on_simulate_click(self):
        """Çalıştır butonuna basıldığında çalışan ana işlev."""
        # Hata mesajını sıfırla
        self.error_label.configure(text="")

        try:
            capacity, ref_string, algo_name = self._parse_inputs()
        except ValueError as err:
            error_message = str(err)
            self.error_label.configure(text=f"⚠️ {error_message.splitlines()[0]}")
            messagebox.showwarning("Giriş Hatası", error_message)
            return

        # Algoritmayı çalıştır
        try:
            result = run_algorithm(capacity=capacity, reference_string=ref_string, algorithm_name=algo_name)
        except Exception as e:
            messagebox.showerror("Simülasyon Hatası", f"Algoritma çalıştırılırken bir hata oluştu:\n{e}")
            return

        # Sonuçları ekrana yansıt
        self._display_results(result, capacity)

    # SONUÇLARI GÖRSELLEŞTİRME (RESULTS & TABLE RENDERING)

    def _display_results(self, result: dict, capacity: int):
        """Simülasyon sonuçlarını özet kartlara ve tabloya aktarır."""
        page_faults = result["page_faults"]
        hits = result["hits"]
        history = result.get("history", [])
        total_requests = len(history)

        # 1. Özet Kartlarını Güncelle
        hit_ratio = (hits / total_requests * 100) if total_requests > 0 else 0.0
        self.card_total.value_label.configure(text=str(total_requests))
        self.card_faults.value_label.configure(text=str(page_faults))
        self.card_hits.value_label.configure(text=str(hits))
        self.card_ratio.value_label.configure(text=f"%{hit_ratio:.1f}")

        self.status_info_label.configure(
            text=f"Algoritma: {result.get('algorithm', '')} | Toplam İstek: {total_requests}",
            text_color="#C4B5FD"
        )

        # 2. Tabloyu Temizle
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        # 3. Tablo Başlık Satırı
        # Sütunlar: Adım | İstek Sayfa | Bellek Çerçeveleri (Frames) | Sonuç (Hit/Fault)
        headers = ["Adım", "Gelen Sayfa", "Bellek Durumu (Frames)", "Sonuç"]
        col_weights = [1, 2, 5, 2]

        header_row = ctk.CTkFrame(self.scroll_table, fg_color="#302543", corner_radius=6)
        header_row.pack(fill="x", pady=(0, 6), padx=4)

        for col_idx, (header_text, weight) in enumerate(zip(headers, col_weights)):
            lbl = ctk.CTkLabel(
                header_row,
                text=header_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#DDD6FE"
            )
            lbl.grid(row=0, column=col_idx, padx=10, pady=8, sticky="w" if col_idx < 3 else "e")
            header_row.grid_columnconfigure(col_idx, weight=weight)

        # 4. Adım Adım Satırları Ekle
        for index, step in enumerate(history, start=1):
            page = step["page"]
            frames = step["frames"]
            is_fault = step["is_fault"]

            # Alternatif satır arka plan rengi (koyu mor tonları)
            row_bg = "#2B213D" if index % 2 == 0 else "#231B32"
            row_frame = ctk.CTkFrame(self.scroll_table, fg_color=row_bg, corner_radius=4)
            row_frame.pack(fill="x", pady=2, padx=4)

            # Adım Numarası (#1, #2...)
            step_lbl = ctk.CTkLabel(
                row_frame,
                text=f"#{index}",
                font=ctk.CTkFont(size=12),
                text_color="#A79FB8"
            )
            step_lbl.grid(row=0, column=0, padx=12, pady=6, sticky="w")

            # İstenen Sayfa
            page_lbl = ctk.CTkLabel(
                row_frame,
                text=f"Sayfa {page}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#F5F3FF"
            )
            page_lbl.grid(row=0, column=1, padx=10, pady=6, sticky="w")

            # Bellek Çerçeveleri Gösterimi: [ 7 | 0 | 1 ]
            # Kapasiteye kadar boş slotları '-' ile doldurarak görselleştiriyoruz
            frame_slots = [str(f) for f in frames]
            empty_slots = capacity - len(frames)
            if empty_slots > 0:
                frame_slots.extend(["—"] * empty_slots)
            frames_display = "  [ " + " | ".join(frame_slots) + " ]"

            frames_lbl = ctk.CTkLabel(
                row_frame,
                text=frames_display,
                font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                text_color="#C4B5FD"
            )
            frames_lbl.grid(row=0, column=2, padx=10, pady=6, sticky="w")

            # Sonuç Rozeti (Badge): Hit (Yeşil) / Page Fault (Kırmızı)
            if is_fault:
                badge_text = "SAYFA HATASI"
                badge_fg = "#7F1D1D"   # Koyu kırmızı arka plan
                badge_text_color = "#FCA5A5"  # Parlak kırmızı yazı
            else:
                badge_text = "İSABET"
                badge_fg = "#064E3B"   # Koyu yeşil arka plan
                badge_text_color = "#6EE7B7"  # Parlak yeşil yazı

            status_badge = ctk.CTkLabel(
                row_frame,
                text=badge_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=badge_fg,
                text_color=badge_text_color,
                corner_radius=4,
                width=100,
                height=24
            )
            status_badge.grid(row=0, column=3, padx=12, pady=6, sticky="e")

            # Kolon oranlarını koru
            for col_idx, weight in enumerate(col_weights):
                row_frame.grid_columnconfigure(col_idx, weight=weight)
