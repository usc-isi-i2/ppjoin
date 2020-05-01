import unittest
import collections
import ppjoin


class TestPPJoin(unittest.TestCase):

    @staticmethod
    def run_jaccard(ds, t):
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
    def run_ppjoin(ds, t):
        result = set()
        ppjoin_result = ppjoin.ppjoin(ds, t=t)
        for r in ppjoin_result:
            ds1_id, r1id = r[0]
            ds2_id, r2id = r[1]
            result.add(str(r1id) + '-' + str(r2id))
        return result

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
            datasets.append([set(ppjoin.whitespace_tokenizer(r)) for r in ds])

        for ds in datasets:
            for t in range(0, 11):
                t = float(t) / 10

                merged_result = collections.defaultdict(lambda: [None, None])
                for r in self.run_jaccard(ds, t):
                    merged_result[r][0] = True
                for r in self.run_ppjoin([ds], t):
                    merged_result[r][1] = True

                for k, r in merged_result.items():
                    assert r[0] == r[1]

    def test_multi_party(self):
        pass


if __name__ == '__main__':
    unittest.main()
