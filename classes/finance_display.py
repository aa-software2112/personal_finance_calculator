
class FinanceDisplay:

    def __init__(self, transaction_map):
        # Receives a map of category -> list of transactions
        self.tmap = transaction_map

    def display(self):
        # Sort by largest list of transactions
        disp = dict(sorted(self.tmap.items(), key=lambda e: len(e[1]), reverse=True))
        running_in = 0
        running_out = 0
        for category, transactions in disp.items():
            if len(transactions) == 0:
                continue
            cat_in = 0
            cat_out = 0
            print(f"{category}:")
            for t in transactions:
                cost = t.get_cost()
                if cost > 0:
                    cat_in += cost
                    running_in += cost
                else:
                    cat_out += cost
                    running_out += cost
                print("\t" + str(t))
            print(f"\t...CATEGORY_IN: ${cat_in}")
            print(f"\t...CATEGORY_OUT: ${cat_out}")
        print(f"--> TOTAL_IN: ${running_in}")
        print(f"--> TOTAL_OUT: ${running_out}")
        print(f"--> GAIN/LOSS: ${running_in + running_out}")