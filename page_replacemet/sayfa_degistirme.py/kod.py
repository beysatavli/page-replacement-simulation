class PageReplacementSimulator:
    def __init__(self, capacity: int, reference_string: list[int]):
        self.capacity = capacity
        self.reference_string = reference_string

    def fifo(self) -> dict:
        """First-In, First-Out (FIFO) Algoritması"""
        frames = []
        page_faults = 0
        history = []

        for page in self.reference_string:
            is_fault = False
            if page not in frames:
                is_fault = True
                page_faults += 1
                if len(frames) >= self.capacity:
                    frames.pop(0)
                frames.append(page)
            history.append({"page": page, "frames": list(frames), "is_fault": is_fault})

        return {
            "algorithm": "FIFO",
            "page_faults": page_faults,
            "hits": len(self.reference_string) - page_faults,
            "history": history
        }

    def lru(self) -> dict:
        """Least Recently Used (LRU) Algoritması"""
        frames = []
        page_faults = 0
        history = []

        for page in self.reference_string:
            is_fault = False
            if page in frames:
                frames.remove(page)
                frames.append(page)
            else:
                is_fault = True
                page_faults += 1
                if len(frames) >= self.capacity:
                    frames.pop(0)
                frames.append(page)
            history.append({"page": page, "frames": list(frames), "is_fault": is_fault})

        return {
            "algorithm": "LRU",
            "page_faults": page_faults,
            "hits": len(self.reference_string) - page_faults,
            "history": history
        }

    def opt(self) -> dict:
        """Optimal Page Replacement (OPT) Algoritması"""
        frames = []
        page_faults = 0
        history = []

        for i, page in enumerate(self.reference_string):
            is_fault = False
            if page not in frames:
                is_fault = True
                page_faults += 1
                if len(frames) < self.capacity:
                    frames.append(page)
                else:
                    future = self.reference_string[i + 1:]
                    victim_idx = -1
                    farthest_use = -1

                    for j, f in enumerate(frames):
                        if f not in future:
                            victim_idx = j
                            break
                        else:
                            first_use = future.index(f)
                            if first_use > farthest_use:
                                farthest_use = first_use
                                victim_idx = j

                    frames[victim_idx] = page
            history.append({"page": page, "frames": list(frames), "is_fault": is_fault})

        return {
            "algorithm": "OPTIMAL",
            "page_faults": page_faults,
            "hits": len(self.reference_string) - page_faults,
            "history": history
        }

    def second_chance(self) -> dict:
        """Clock / Second Chance Algoritması"""
        frames = []
        use_bits = []
        pointer = 0
        page_faults = 0
        history = []

        for page in self.reference_string:
            is_fault = False
            if page in frames:
                idx = frames.index(page)
                use_bits[idx] = 1
            else:
                is_fault = True
                page_faults += 1

                if len(frames) < self.capacity:
                    frames.append(page)
                    use_bits.append(1)
                else:
                    while True:
                        if use_bits[pointer] == 0:
                            frames[pointer] = page
                            use_bits[pointer] = 1
                            pointer = (pointer + 1) % self.capacity
                            break
                        else:
                            use_bits[pointer] = 0
                            pointer = (pointer + 1) % self.capacity

            history.append({"page": page, "frames": list(frames), "is_fault": is_fault})

        return {
            "algorithm": "SECOND CHANCE",
            "page_faults": page_faults,
            "hits": len(self.reference_string) - page_faults,
            "history": history
        }

    def run_all(self) -> dict:
        """Tüm algoritmaları çalıştırıp toplu sonuç döner"""
        return {
            "FIFO": self.fifo(),
            "LRU": self.lru(),
            "OPTIMAL": self.opt(),
            "SECOND_CHANCE": self.second_chance()
        }


# --- TEST İÇİN ---
if __name__ == "__main__":
    test_dizisi = [1, 2, 3, 1, 4, 5, 2, 1]
    frame_sayisi = 3

    sim = PageReplacementSimulator(capacity=frame_sayisi, reference_string=test_dizisi)
    
    print("=== TEST SONUÇLARI ===")
    sonuclar = sim.run_all()
    for algo, res in sonuclar.items():
        print(f"{algo:<15}: {res['page_faults']} Page Fault")



