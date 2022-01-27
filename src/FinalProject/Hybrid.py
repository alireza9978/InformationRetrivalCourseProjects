import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def calculate_similarity(temp_df: pd.DataFrame):
    normalized_pivot_table = temp_df.drop(columns=["user_type"]).T
    piv_sparse = sp.sparse.csr_matrix(normalized_pivot_table.values)
    item_similarity = cosine_similarity(piv_sparse)
    item_sim_df = pd.DataFrame(item_similarity, index=normalized_pivot_table.index,
                               columns=normalized_pivot_table.index)
    return item_sim_df


if __name__ == '__main__':
    anime_df = pd.read_csv("content_based_features.csv", index_col="name", low_memory=False)
    user_df = pd.read_csv("collaborative_filtering_features.csv", index_col="name", low_memory=False)

    user_anime_df = user_df.T

    # I test several cluster count and based on silhouette_score n_clusters=4 is the best
    clu = KMeans(n_clusters=4)
    user_type = clu.fit_predict(user_anime_df)
    user_anime_df['user_type'] = user_type

    user_anime_df_similarity = user_anime_df.groupby("user_type").apply(calculate_similarity)

    temp_anime_index = anime_df.index
    pca_model = PCA(n_components=20)
    anime_df = pca_model.fit_transform(anime_df.drop(columns=["anime_id"]).fillna(0))
    anime_df = pd.DataFrame(anime_df, index=temp_anime_index)
    model = NearestNeighbors(n_neighbors=10)
    model.fit(anime_df)

    target_name = 'Cowboy Bebop'
    target_df = pd.DataFrame()

    test_row = anime_df[anime_df.index == target_name]
    distance, result = model.kneighbors(test_row)
    target_df["content"] = pd.Series(1/distance[0][1:], index=anime_df.iloc[result[0][1:]].index)

    selected_rows = user_anime_df_similarity[user_anime_df_similarity.index.get_level_values(1) == target_name]
    selected_rows = selected_rows.reset_index(drop=True)
    for i in range(4):
        temp_result = selected_rows.T[i].sort_values(ascending=False).iloc[1:11]
        temp_result.name = None
        temp_result = pd.DataFrame(temp_result, columns=[f"collaborative_{i}"])
        target_df = target_df.join(temp_result, how="outer")

    result = target_df.fillna(0).sum(axis=1).sort_values(ascending=False)[:10]

    print(result)
