def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_metal_tally(df,year,country):
    flag = 0 
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df 
    if year == 'Overall' and country != 'Overall':
        flag = 1 
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)] 
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)] 
    
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x 

def participation_nation_over_time(df):
    nation_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values(['Year'],ascending=True)
    return nation_over_time

def total_events_over_time(df):
    event_over_time = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values(['Year'],ascending=True)
    return event_over_time

def atheletes_over_time(df):
    player_over_time = df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values(['Year'],ascending=True)
    return player_over_time

def most_successfull(df,sport_val):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport_val != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport_val]
    
    x =  temp_df['Name'].value_counts().reset_index().head(15).merge(df , on="Name",how="left")[['Name','count','region','Sport']].drop_duplicates()
    
    x.rename(columns={'count':'Medals' , 'region' : 'Region'} , inplace=True)
    
    return x 

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'] , inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'] , inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return temp_df

def country_wise_top_athelete(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df , on='Name',how='left')[['Name','count','Sport']].drop_duplicates()
    x.rename(columns={'count':'Medals'} , inplace=True)
    x = x.reset_index(drop=True)
    x.index = x.index + 1
    return x

def weight_v_height(df,sport):
      athelete_df = df.drop_duplicates(subset=['Name','region'])
      athelete_df['Medal'].fillna('No Medal' , inplace= True)
      temp_df = athelete_df[athelete_df['Sport'] == sport]

      return temp_df

def men_women_participation(df):
    athelete_df = df.drop_duplicates(subset=['Name','region'])
    men_df = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women_df = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = men_df.merge(women_df , on='Year', how='left')
    final_df.rename(columns={'Name_x' : 'Male','Name_y':'Female'} , inplace= True)
    final_df = final_df.fillna(0).astype(int)
    return final_df