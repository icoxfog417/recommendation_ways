import numpy as np
from data_loader import load


def calc_collaborative_users(user_id, user_reviews):
    user_index = user_reviews.users.index(user_id)

    # calculate corrcoef score
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.corrcoef.html
    scores = np.corrcoef(user_reviews.data)

    # extract user's score
    user_scores = scores[:, user_index]

    # make user/score list and sort it
    collaborators = []
    for i, c in enumerate(user_scores):
        # exclude self
        if i != user_index:
            collaborators.append((i, c))

    collaborators = sorted(collaborators, key=lambda x: x[1], reverse=True)
    return collaborators


def filter_by_collaborative_users(user_reviews, collaborators, to_rank=10):
    # extract top n collaborators
    # !you have to sort collaborators by score
    top_collaborators = collaborators[:to_rank]

    # calculate weighted score of rating and weighted average
    review_mx = user_reviews.data
    ratings = review_mx[[c[0] for c in top_collaborators], :]
    # have to consider the way to calculate weighted average
    weights = np.abs(np.array([c[1] for c in top_collaborators]))

    weighted_rating = np.transpose(ratings) * weights
    weighted_rating = np.sum(weighted_rating, axis=1) / np.sum(weights)  # calculate weighted average

    # make places list
    places = []
    for i, r in enumerate(weighted_rating):
        places.append((i, r))

    places = sorted(places, key=lambda x: x[1], reverse=True)
    return places


def main():
    user_reviews = load()
    target_user_id = user_reviews.users[0]

    collaborators = calc_collaborative_users(target_user_id, user_reviews)
    print("user {0}'s collaborators are below (top5)".format(target_user_id))
    for c in collaborators[:5]:
        user_id = user_reviews.users[c[0]]
        print("{0}: {1}".format(user_id, c[1]))

    places = filter_by_collaborative_users(user_reviews, collaborators)
    print("favorite places will be below")
    for p in places[:5]:
        place_id = user_reviews.places[p[0]]
        print("{0}: {1}".format(place_id, p[1]))


if __name__ == "__main__":
    main()
