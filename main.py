"""
Page Replacement Simulator
--------------------------
Uygulamanın başlangıç noktası (Entry Point).
Bu dosyayı çalıştırarak arayüzü başlatabilirsiniz:
    python3 main.py
"""

from ui import PageReplacementUI


def main():
    app = PageReplacementUI()
    app.mainloop()


if __name__ == "__main__":
    main()
