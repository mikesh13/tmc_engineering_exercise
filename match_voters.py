import pandas as pd
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
    df['MIDDLE_NAME'] = df['MIDDLE_NAME'].transform(lambda x: transform_text(x))
    df['LAST_NAME'] = df['LAST_NAME'].transform(lambda x: transform_text(x))
    df['name'] = df[['FIRST_NAME', 'LAST_NAME']].agg(' '.join, axis=1)

    return df[['matched_voter_id', 'name', 'MIDDLE_NAME']]


def merge_county_dfs():
    data_list = os.listdir('county_voter_data')
    data_list = ['county_voter_data/' + ele for ele in data_list]

    df = pd.concat(map(pd.read_csv, data_list), ignore_index=True)
    df = (
        df[['SOS_VOTERID', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME']]
        .dropna()
        .copy()
        .rename(columns={'SOS_VOTERID': 'matched_voter_id'})
        )

    df = add_name_col(df)

    return df


def match_voters_with_voter_id():
    county_df = merge_county_dfs()
    voter_df = pd.read_csv('matching_data/eng-matching-input-v3.csv')
    voter_df['MIDDLE_NAME'] = voter_df.name.apply(
        lambda x: extract_middle_name(x))
    print(voter_df.head())

    #merged_df = pd.merge(county_df, voter_df, on=['name', 'MIDDLE_NAME'], how='inner')
    merged_df = pd.merge(county_df, voter_df, on='name', how='inner')
    #final_cols = merged_df.columns.remove('MIDDLE_NAME')
    #merged_df[final_cols].to_csv('matched_data/matched_data.csv', index=False)
    merged_df.to_csv('matched_data/matched_data.csv', index=False)


#print(match_voters_with_voter_id())
#print(merge_county_dfs().head())
match_voters_with_voter_id()
