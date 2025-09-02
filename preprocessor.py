import pandas as pd 



def preprocess(df,region_df):
    # Filtering only Summer Games
    df = df[df['Season'] == 'Summer'].reset_index(drop=True)
    # Merging the region data with original data
    df = df.merge(region_df , on='NOC' , how='left')
    # Dropping the overall duplicate values
    df.drop_duplicates(inplace=True)
    # Concate the output of the one hot encoder with the dataframe
    df = pd.concat([df, pd.get_dummies(df['Medal'] , dtype=int)] , axis=1)
    return df  