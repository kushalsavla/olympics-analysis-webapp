import pandas as pd


def preprocess(df, region_df):
    # filtering to only summer olympics
    df = df[df['Season'] == 'Summer']

    # merging with region_df on region
    df = df.merge(region_df, on='NOC', how='left')

    # dropping duplicated rows
    df.drop_duplicates(inplace=True)

    # one hot encoding medals column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
