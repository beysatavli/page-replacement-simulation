"""
Simulator Bridge (Bağlantı Modülü)
----------------------------------
Bu modül, 'main' branch'inden gelen orijinal algoritma dosyasına 
klasör yapısını ve kodları değiştirmeden güvenli bir şekilde bağlanır.
"""

import sys
import importlib.util
from pathlib import Path


def _load_simulator_class():
    """
    Orijinal 'kod.py' dosyasını dosya yolundan dinamik olarak yükler.
    Böylece Türkçe karakter veya özel klasör isimleri import hatası oluşturmaz.
    """
    base_dir = Path(__file__).resolve().parent
    target_file = base_dir / "sayfa_degiştirme_projesi" / "sayfa_degistirme.py" / "kod.py"

    if not target_file.exists():
        raise FileNotFoundError(
            f"Algoritma dosyası bulunamadı: {target_file}\n"
            "Lütfen 'sayfa_degiştirme_projesi/sayfa_degistirme.py/kod.py' dosyasının mevcut olduğundan emin olun."
        )

    spec = importlib.util.spec_from_file_location("original_simulator", target_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "PageReplacementSimulator"):
        raise AttributeError("Modül içinde 'PageReplacementSimulator' sınıfı bulunamadı.")

    return module.PageReplacementSimulator


# Yüklenen sınıfı dışa aktarıyoruz
PageReplacementSimulator = _load_simulator_class()


def run_algorithm(capacity: int, reference_string: list, algorithm_name: str) -> dict:
    """
    Seçilen algoritmaya göre simülasyonu çalıştırır ve sonuç sözlüğünü döner.
    
    Parametreler:
        capacity (int): Frame (çerçeve) sayısı
        reference_string (list[int]): Sayfa istek dizisi
        algorithm_name (str): 'FIFO', 'LRU', 'Optimal' veya 'Second Chance'
    
    Dönüş:
        dict: {
            "algorithm": str,
            "page_faults": int,
            "hits": int,
            "history": list[dict]
        }
    """
    simulator = PageReplacementSimulator(capacity=capacity, reference_string=reference_string)

    algo = algorithm_name.strip()
    if algo == "FIFO":
        return simulator.fifo()
    elif algo == "LRU":
        return simulator.lru()
    elif algo in ("Optimal", "OPT", "OPTIMAL"):
        return simulator.opt()
    elif algo in ("Second Chance", "SECOND CHANCE", "Clock"):
        return simulator.second_chance()
    else:
        raise ValueError(f"Desteklenmeyen algoritma adı: {algorithm_name}")
