import pandas as pd
import numpy as np
import os


def transform_text(txt: str) -> str:
    """
    Takes a word and make it into title form
    e.g. TAKE -> Take

    :param txt: a string that needed to be transformed
    :return: transformed string
    """
    if txt == '':
        return None

    return txt.title()


def add_name_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a new 'name' column with 'first_name' and 'last_name' columns

    :param df: a pandas dataframe with 'first_name' and 'last_name' columns
    :return: a pandas dataframe with a new 'name' column
    """
    df['FIRST_NAME'] = df['FIRST_NAME'].transform(lambda x: transform_text(x))
    df['LAST_NAME'] = df['LAST_NAME'].transform(lambda x: transform_text(x))
    df['name'] = df[['FIRST_NAME', 'LAST_NAME']].agg(' '.join, axis=1)

    return df


def extract_year(birth_date: str) -> str:
    """
    Takes a date string and extract and return the year part
    e.g. 2023-02-02 -> 2023

    :param birth_date: a date string that should look like '2023-02-02'
    :return: a year string 
    """
    if birth_date == np.nan or birth_date == '':
        return birth_date
    else:
        year = birth_date.split('-')[0]
        return year


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform a pandas dataframe and prepares it for merge later

    :param df: a pandas dataframe
    :return: a tranformed pandas dataframe
    """
    df = add_name_col(df)
    df['birth_year'] = (df.birth_year.apply(lambda x: extract_year(x)))

    df = (df[['matched_voter_id', 'name', 'birth_year', 'zip']]
          .copy()
          .astype({
            'name': object,
            'zip': str
            }))

    return df


def merge_county_dfs():
    """
    Reads the all the input data into a single pandas dataframe

    :return: a pandas dataframe with all the input data
    """
    data_list = os.listdir('county_voter_data')
    data_list = ['county_voter_data/' + ele for ele in data_list]

    df = pd.concat(map(pd.read_csv, data_list), ignore_index=True)
    df = (
        df[['SOS_VOTERID', 'FIRST_NAME', 'LAST_NAME',
            'DATE_OF_BIRTH', 'RESIDENTIAL_ZIP']]
        .dropna()
        .copy()
        .rename(columns={
            'SOS_VOTERID': 'matched_voter_id',
            'DATE_OF_BIRTH': 'birth_year',
            'RESIDENTIAL_ZIP': 'zip'
            })
        )

    df = transform_df(df)

    return df


def match_voters_with_voter_id():
    """
    Reads and transforms both input and target data then merge them
    """
    county_df = merge_county_dfs()
    voter_df = pd.read_csv('matching_data/eng-matching-input-v3.csv').dropna()

    voter_df['birth_year'] = voter_df.birth_year.apply(lambda x: str(int(x)))
    voter_df['zip'] = voter_df.zip.apply(lambda x: str(x)[:-2])

    merged_df = pd.merge(county_df, voter_df, on=['name', 'birth_year', 'zip'],
                         how='inner')
    merged_df.to_csv('matched_data/matched_data.csv', index=False)
