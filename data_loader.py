import os
from collections import namedtuple

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

    return UserReviews(users, places, urs)
