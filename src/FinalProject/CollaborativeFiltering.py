import numpy as np
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

anime_df = pd.read_csv('../../data/FinalProject/anime.csv')
rating_df = pd.read_csv('../../data/FinalProject/rating.csv')

rating_df.loc[rating_df["rating"] == -1, "rating"] = np.nan

# Join the two dataframes on the anime_id columns
merged_df = rating_df.merge(anime_df, left_on='anime_id', right_on='anime_id', suffixes=['_user', ''])
merged_df.rename(columns={'rating_user': 'user_rating'}, inplace=True)

# For computing reasons I'm limiting the dataframe length to 10,000 users
merged_df = merged_df[['user_id', 'name', 'user_rating']]
unique_users_id = merged_df["user_id"].unique()
selected_users_id = np.random.choice(unique_users_id, 10000)
merged_sub = merged_df[merged_df.user_id.isin(selected_users_id)]

pivot_table = merged_sub.pivot_table(index=['user_id'], columns=['name'], values='user_rating')
# rows = users and columns = anime

# Note: As we are subtracting the mean from each rating to standardize
# all users with only one rating or who had rated everything the same will be dropped

# Normalize the values
normalized_pivot_table = pivot_table.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)), axis=1)

# # Drop all columns containing only zeros representing users who did not rate
normalized_pivot_table.fillna(0, inplace=True)
normalized_pivot_table = normalized_pivot_table.loc[(normalized_pivot_table != 0).any(axis=1)]
normalized_pivot_table = normalized_pivot_table.T

# Our data needs to be in a sparse matrix format to be read by the following functions
piv_sparse = sp.sparse.csr_matrix(normalized_pivot_table.values)

item_similarity = cosine_similarity(piv_sparse)
user_similarity = cosine_similarity(piv_sparse.T)

# Inserting the similarity matrices into dataframe objects
item_sim_df = pd.DataFrame(item_similarity, index=normalized_pivot_table.index, columns=normalized_pivot_table.index)
user_sim_df = pd.DataFrame(user_similarity, index=normalized_pivot_table.columns,
                           columns=normalized_pivot_table.columns)


# This function will return the top 10 shows with the highest cosine similarity value
def top_animes(anime_name):
    count = 1
    print('Similar shows to "{}" include:\n'.format(anime_name))
    for item in item_sim_df.sort_values(by=anime_name, ascending=False).index[1:11]:
        print('No. {}: {}'.format(count, item))
        count += 1


top_animes('Cowboy Bebop')
###
# No. 1: Cowboy Bebop: Tengoku no Tobira
# No. 2: Samurai Champloo
# No. 3: Tengen Toppa Gurren Lagann
# No. 4: Mononoke Hime
# No. 5: Trigun
# No. 6: Baccano!
# No. 7: Ghost in the Shell: Stand Alone Complex
# No. 8: Sen to Chihiro no Kamikakushi
# No. 9: Fullmetal Alchemist: Brotherhood
# No. 10: Black Lagoon: The Second Barrage
###

#
#
# # This function will return the top 5 users with the highest similarity value
# def top_users(user):
#     if user not in normalized_pivot_table.columns:
#         print('No data available on user {}'.format(user))
#
#     print('Most Similar Users:\n')
#     sim_values = user_sim_df.sort_values(by=user, ascending=False).loc[:, user].tolist()[1:11]
#     sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
#     zipped = zip(sim_users, sim_values, )
#     for user, sim in zipped:
#         print('User #{0}, Similarity value: {1:.2f}'.format(user, sim))
#
#     for user, sim in zipped:
#         print('User #{0}, Similarity value: {1:.2f}'.format(user, sim))
#
#
# # This function constructs a list of lists containing the highest rated shows per similar user
# # and returns the name of the show along with the frequency it appears in the list
# def similar_user_recs(user):
#     if user not in normalized_pivot_table.columns:
#         print('No data available on user {}'.format(user))
#
#     sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
#     best = []
#     most_common = {}
#
#     for i in sim_users:
#         max_score = normalized_pivot_table.loc[:, i].max()
#         best.append(normalized_pivot_table[normalized_pivot_table.loc[:, i] == max_score].index.tolist())
#     for i in range(len(best)):
#         for j in best[i]:
#             if j in most_common:
#                 most_common[j] += 1
#             else:
#                 most_common[j] = 1
#     sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
#     return sorted_list[:5]
#
#
# # This function calculates the weighted average of similar users
# # to determine a potential rating for an input user and show
# def predicted_rating(anime_name, user):
#     sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:1000]
#     user_values = user_sim_df.sort_values(by=user, ascending=False).loc[:, user].tolist()[1:1000]
#     rating_list = []
#     weight_list = []
#     for j, i in enumerate(sim_users):
#         rating = pivot_table.loc[i, anime_name]
#         similarity = user_values[j]
#         if np.isnan(rating):
#             continue
#         elif not np.isnan(rating):
#             rating_list.append(rating * similarity)
#             weight_list.append(similarity)
#     return sum(rating_list) / sum(weight_list)

# top_users(selected_users_id[0])
# similar_user_recs(selected_users_id[0])
# print(predicted_rating('Cowboy Bebop', 3))
# # Creates a list of every show watched by user 3
#
# watched = piv.T[piv.loc[3, :] > 0].index.tolist()
#
# # Make a list of the squared errors between actual and predicted value
#
# errors = []
# for i in watched:
#     actual = piv.loc[3, i]
#     predicted = predicted_rating(i, 3)
#     errors.append((actual - predicted) ** 2)
#
# # This is the average squared error for user 3
# np.mean(errors)
