from page_replacemet.kod import PageReplacementSimulator

def run_algorithm(capacity: int, reference_string: list, algorithm_name: str) -> dict:
    simulator = PageReplacementSimulator(capacity=capacity, reference_string=reference_string)
    algo = algorithm_name.strip().upper()

    if algo == "FIFO":
        return simulator.fifo()
    elif algo == "LRU":
        return simulator.lru()
    elif algo in ("OPTIMAL", "OPT"):
        return simulator.opt()
    elif algo in ("SECOND CHANCE", "CLOCK"):
        return simulator.second_chance()
    else:
        raise ValueError(f"Desteklenmeyen veya geçersiz algoritma adı: {algorithm_name}")

def run_console_simulation(capacity: int, reference_string: list):
    print("\n" + "="*45)
    print(" PAGE REPLACEMENT SİSTEM TESTİ BAŞLADI")
    print("="*45)
    print(f"Çerçeve (Frame) Sayısı : {capacity}")
    print(f"Sayfa Referans Dizisi  : {reference_string}\n")
    
    simulator = PageReplacementSimulator(capacity=capacity, reference_string=reference_string)
    results = simulator.run_all()
    
    for algo_name, res in results.items():
        faults = res['page_faults']
        hits = res['hits']
        print(f"[{algo_name:<13}] -> Page Faults: {faults:<3} | Hits: {hits}")
    print("="*45 + "\n")

if __name__ == "__main__":
    test_capacity = 3
    test_ref_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3]
    run_console_simulation(capacity=test_capacity, reference_string=test_ref_string)