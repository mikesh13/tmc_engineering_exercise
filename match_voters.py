import pandas as pd
import numpy as np
import os


def transform_text(txt: str) -> str:
    if txt == '':
        return None
    
    return txt.title()


def extract_middle_name(txt: str) -> str:
    name = txt.split(" ")
    if len(name) > 2:
        return name[1]
    else:
        return ""


def add_name_col(df: pd.DataFrame) -> pd.DataFrame:
    df['FIRST_NAME'] = df['FIRST_NAME'].transform(lambda x: transform_text(x))
    # df['MIDDLE_NAME'] = df['MIDDLE_NAME'].transform(lambda x: transform_text(x))
    df['LAST_NAME'] = df['LAST_NAME'].transform(lambda x: transform_text(x))
    df['name'] = df[['FIRST_NAME', 'LAST_NAME']].agg(' '.join, axis=1)

    return df


def extract_year(birth_date: str) -> str:
    if birth_date == np.nan or birth_date == '':
        return birth_date
    else:
        year = birth_date.split('-')[0]
        return year


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
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
    county_df = merge_county_dfs()
    voter_df = pd.read_csv('matching_data/eng-matching-input-v3.csv').dropna()

    voter_df['birth_year'] = voter_df.birth_year.apply(lambda x: str(int(x)))
    voter_df['zip'] = voter_df.zip.apply(lambda x: str(x)[:-2])

    merged_df = pd.merge(county_df, voter_df, on=['name', 'birth_year', 'zip'],
                         how='inner')
    merged_df.to_csv('matched_data/matched_data.csv', index=False)
