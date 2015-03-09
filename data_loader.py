import os
from collections import namedtuple
import numpy as np

DEFAULT_FILE_PATH = "./data/users_reviews.txt"
UserReview = namedtuple("UserReview", ["user_id", "place_id", "rating"])
UserReviews = namedtuple("UserReviews", ["users", "places", "data"])


def load(file_path="", separator="\t", skip_headers=1, encoding="utf-8"):
    # read file
    _file_path = file_path
    if not _file_path:
        _file_path = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_PATH)

    lines = []
    separate = lambda x: x.replace("\r", "").replace("\n", "").strip().split(separator)
    with open(_file_path, "r", encoding=encoding) as f:
        lines = f.readlines()
        lines = [separate(ln) for ln in lines[skip_headers:]]

    # get distinct user/place
    users = list(set([items[0] for items in lines]))
    places = list(set([items[1] for items in lines]))

    # make user review data
    urs = []
    for items in lines:
        ur = UserReview(items[0], items[1], float(items[2]))
        urs.append(ur)

    review_mx = __make_review_matrix(users, places, urs)
    return UserReviews(users, places, review_mx)


def __make_review_matrix(users, places, user_reviews):
    # make review data matrix
    review_mx = np.zeros([len(users), len(places)])
    for ur in user_reviews:
        u_index = users.index(ur.user_id)
        p_index = places.index(ur.place_id)
        review_mx[u_index][p_index] = ur.rating

    return review_mx
