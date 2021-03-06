import unittest
import collections
import csv
from ppjoin import ppjoin


class TestPPJoin(unittest.TestCase):

    @staticmethod
    def run_jaccard_single_ds(ds, t):
        result = set()
        for r1id, r1 in enumerate(ds):
            for r2id, r2 in enumerate(ds):
                if r1id >= r2id:
                    continue
                score = ppjoin.jaccard(r1, r2)
                if score < t:
                    continue
                result.add(str(r1id) + '-' + str(r2id))
        return result

    @staticmethod
    def run_jaccard_two_ds(ds, t):
        result = set()
        for r1id, r1 in enumerate(ds[0]):
            for r2id, r2 in enumerate(ds[1]):
                score = ppjoin.jaccard(r1, r2)
                if score < t:
                    continue
                result.add(str(r1id) + '-' + str(r2id))
        return result

    @staticmethod
    def run_ppjoin(ds, t):
        result = set()
        ppjoin_result = ppjoin.join(ds, t=t)
        for r in ppjoin_result:
            ds1_id, r1id = r[0]
            ds2_id, r2id = r[1]
            result.add(str(r1id) + '-' + str(r2id))
        return result

    @staticmethod
    def ws_tokenizer(r):
        return set(ppjoin.whitespace_tokenizer(r.lower()))

    @staticmethod
    def trigram_tokenizer(r):
        return set(ppjoin.qgram_tokenizer(3, r.lower(), padded=True))

    def test_correctness(self):
        raw_datasets = [
            ['a b d', 'a b c', 'h k', 'a b k', 'a b', 'h k', 'a c h', 'a c h'],
            ['h k', 'h k'],
            ['a b d', 'a b'],
            ['a b d', 'h k'],
            ['a c c', 'a b k', 'c d a']
        ]

        datasets = []
        for ds in raw_datasets:
            datasets.append([self.ws_tokenizer(r) for r in ds])

        for ds in datasets:
            for t in range(0, 11):
                t = float(t) / 10

                merged_result = collections.defaultdict(lambda: [None, None])
                for r in self.run_jaccard_single_ds(ds, t):
                    merged_result[r][0] = True
                for r in self.run_ppjoin([ds], t):
                    merged_result[r][1] = True

                for k, r in merged_result.items():
                    assert r[0] == r[1]

    def test_on_real_dataset(self):
        abt, buy = [], []
        with open('datasets/Abt.csv', encoding='latin-1') as f:
            for line in csv.DictReader(f):
                abt.append(self.ws_tokenizer(line['name']))
        with open('datasets/Buy.csv', encoding='latin-1') as f:
            for line in csv.DictReader(f):
                abt.append(self.ws_tokenizer(line['name']))
        ds = [abt, buy]

        for t in range(0, 11):
            t = float(t) / 10

            merged_result = collections.defaultdict(lambda: [None, None])
            for r in self.run_jaccard_two_ds(ds, t):
                merged_result[r][0] = True
            for r in self.run_ppjoin(ds, t):
                merged_result[r][1] = True

            for k, r in merged_result.items():
                assert r[0] == r[1]


if __name__ == '__main__':
    unittest.main()
