import ahocorasick

class CategorySearcher:

    def __init__(self, aho_dict):
        # aho_dict is a list of string supported for lookup 
        # in the AHO model. These will be the "substrings" to look for that
        # indicate the bottom-most level category of a transaction based on the full
        # transaction description
        self.aho = ahocorasick.Automaton()
        for category in aho_dict:
            self.aho.add_word(category, category)
        self.aho.make_automaton()

    def search_category(self, v):
        ret = [v[1] for v in list(self.aho.iter(v))]
        assert len(ret) <= 1, f"[AHO] The search for {v} returned multiple entries... {ret}. Only 0 or 1 should match. Fix Mapping"
        return ret

    def undefined_transactions(self, transactions):
        undef = []
        # Returns the transactions that could not be linked to a category
        for transaction in transactions:
            description = transaction['description']
            ret = self.search_category(description)
            if len(ret) == 0:
                undef.append(description)
        return set(undef)
