import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors


def convert_genre(temp_df):
    def clean_genre(temp_row):
        temp_list = str(temp_row).split(",")
        temp_list = [temp_item.strip() for temp_item in temp_list]
        return temp_list

    temp_df.genre = temp_df.genre.apply(clean_genre)
    genre_dict = set()
    for index, row in temp_df.genre.iteritems():
        for item in row:
            genre_dict.add(item)
    genres_list = list(genre_dict)

    def convert_list_to_series(temp_row):
        temp_series = pd.Series(index=genres_list, name=index)
        for row_item in temp_row:
            temp_series[row_item] = True
        return temp_series

    genre_df = temp_df.genre.apply(convert_list_to_series)
    genre_df.columns = [f"genre_{temp}" for temp in genre_df.columns]
    temp_df = temp_df.drop(columns=["genre"]).join(genre_df)
    return temp_df


def convert_type(temp_df):
    anime_type_df = pd.get_dummies(temp_df["type"])
    anime_type_df.columns = [f"type_{temp}" for temp in anime_type_df.columns]
    temp_df = temp_df.drop(columns=["type"]).join(anime_type_df)
    return temp_df


def convert_input(temp_df, name, target_type=float):
    x = temp_df[name].astype(target_type).to_numpy().reshape(-1, 1)
    model = KMeans(n_clusters=5)
    cluster_label = model.fit_predict(x)
    cluster_label = pd.get_dummies(cluster_label)
    cluster_label.columns = [f"{name}_type_{i}" for i in range(5)]
    temp_df = temp_df.drop(columns=[name]).join(cluster_label)
    return temp_df


def train_model(temp_df):
    train_df = temp_df.drop(columns=["anime_id", "name"]).fillna(0).astype(int)
    model = NearestNeighbors(n_neighbors=10)
    model.fit(train_df)
    return model


def test_model(model, name):
    test_row = anime_df[anime_df.name == name].drop(columns=["anime_id", "name"]).fillna(0).astype(int)
    for index in model.kneighbors(test_row, return_distance=False)[0]:
        print(anime_df.loc[index, "name"])


if __name__ == '__main__':
    anime_df = pd.read_csv('../../data/FinalProject/anime.csv')
    anime_df = convert_genre(anime_df)
    anime_df = convert_type(anime_df)
    anime_df = anime_df[anime_df.episodes != "Unknown"]
    anime_df = convert_input(anime_df, "episodes", int)
    anime_df = anime_df[~anime_df.rating.isna()]
    anime_df = convert_input(anime_df, "rating")
    anime_df = convert_input(anime_df, "members", int)
    print(anime_df.shape)

    trained_model = train_model(anime_df)
    test_model(trained_model, 'Cowboy Bebop')
