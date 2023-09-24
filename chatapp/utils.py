import json
import math

from .models import User


class RecipientNotFound:
    pass


class RecipientOffline:
    pass


def get_interest_similarity_score(user1, user2):
    common_interests = {}
    for interest, score in user1.interests.items():
        if interest in user2.interests:
            common_interests[interest] = score * user2.interests[interest]
    sum_of_squares = sum([val ** 2 for val in common_interests.values()])
    user1_squares = sum([score ** 2 for score in user1.interests.values()])
    user2_squares = sum([score ** 2 for score in user2.interests.values()])
    return sum_of_squares / (math.sqrt(user1_squares) * math.sqrt(user2_squares))


def get_recommended_friends(user_id):
    with open('users.json') as f:
        users = json.load(f)
    target_user = User.objects.get(id=user_id)
    scores = {}
    for user in users:
        if user['id'] != target_user.id:
            score = get_interest_similarity_score(target_user, user)
            scores[user['id']] = score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    friends = [User.objects.get(id=id) for id, score in sorted_scores]
    return friends
