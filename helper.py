import numpy as np
import plotly.figure_factory as ff
import streamlit as st

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/png;base64,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");
             background-attachment: fixed;
             background-size: auto;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def medal_total(medal_tally):
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')
    return medal_tally

def medal_tally_compute(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally = medal_total(medal_tally)
    return medal_tally

def year_list(df):
    years = df['Year'].unique().tolist()
    years.sort(reverse=True)
    years.insert(0, 'Overall')
    return years 

def countries_list(df):
    country = np.unique(df['region'].dropna().tolist()).tolist()
    country.sort()
    country.insert(0,'Overall')
    return country

def medal_fetch(df, year, country):
    flag = 0
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby(['Year']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    return x

def participating_nations_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time = nations_over_time.rename(columns={'index':'Edition', 'Year':col})
    return nations_over_time

def successful_athletes(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index',right_on='Name',how='left')[['index','Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index':'Name', 'Name_x':'Medals', 'region':'Country'},inplace=True)
    return x.reset_index().drop(['index'], axis=1)

def country_wise(df, nation):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df = temp_df[temp_df['region'] == nation]
    temp_ = temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df, temp_

def successful_athletes_nationwise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index',right_on='Name',how='left')[['index','Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name', 'Name_x':'Medals', 'region':'Sport'},inplace=True)
    return x.reset_index().drop(['index'], axis=1)

def plot_athletes_age(df, sport):
    if sport != 'Overview':
        df = df[df['Sport'] == sport]
    x1 = df['Age'].dropna()
    x2 = df[df['Medal'] == 'Gold']['Age'].dropna()
    x3 = df[df['Medal'] == 'Silver']['Age'].dropna()
    x4 = df[df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],show_hist=False,show_rug=False)
    return fig

def athletes_health(df, sport):
    df = df.drop_duplicates(subset=['Name','region'])
    df['Medal'].fillna('No Medal',inplace=True)
    if sport == 'Overview':
        return df
    temp_df = df[df['Sport'] == sport]
    return temp_df

def gender(df):
    df = df.drop_duplicates(subset=['Name','region'])
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final
