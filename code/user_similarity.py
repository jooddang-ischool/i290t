from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def aggregate_by_user_id(self, _, record):
        yield[record['user_id'], record['business_id']]

    def sum_of_biz_each_user(self, user_id, biz_ids):
        unique_biz_ids = list(set(biz_ids))
        yield[user_id, [unique_biz_ids, len(unique_biz_ids)]]

    def switch_to_biz_id(self, user_id, biz_ids_count_pair):
        biz_ids = biz_ids_count_pair[0]
        count_by_user = biz_ids_count_pair[1]
        for biz_id in biz_ids:
            yield[biz_id, [user_id, count_by_user]]

    def make_user_pair(self, biz_id, user_id_count_pair):
        user_id_count_pair = list(user_id_count_pair)
        for i in range(0, len(user_id_count_pair) - 1):
            for j in range(i + 1, len(user_id_count_pair)):
                yield[sorted([user_id_count_pair[i][0], user_id_count_pair[j][0]]), 
                    user_id_count_pair[i][1] + user_id_count_pair[j][1]]

    def calculate_jaccard(self, user_id_pair, sums):
        sums = list(sums)
        jaccard = float(len(sums)) / float(sums[0] - len(sums))
        if jaccard >= 0.5:
            print 'user', user_id_pair[0], 'and ', user_id_pair[1], ' have jaccard similarity of ', jaccard
            yield[user_id_pair, jaccard]

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <key, value>
        reducer1: <key, [values]>
        mapper2: ...
        """
        return [
            self.mr(mapper=self.aggregate_by_user_id, reducer=self.sum_of_biz_each_user),
            self.mr(mapper=self.switch_to_biz_id, reducer=self.make_user_pair),
            self.mr(reducer=self.calculate_jaccard),
        ]


if __name__ == '__main__':
    UserSimilarity.run()
