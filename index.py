from turtle import width
import streamlit as st
import helper
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# helper.add_bg_from_url()
image = Image.open("img.png")
st.sidebar.image(image.resize((150, 30)))
st.sidebar.header('Olympics history data')
df = pd.read_csv('olympicsData/athlete_events.csv')
region_df = pd.read_csv('olympicsData/noc_regions.csv')
def preprocess():
    global df, region_df
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])],axis=1)
    return df
df = preprocess()

user_menu = st.sidebar.radio(
    'Select option',
    ('Medal tally','Top performer','Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

#st.dataframe(df)
if user_menu == 'Medal tally':
    st.sidebar.header('Medal Tally')
    year = helper.year_list(df)
    country = helper.countries_list(df)
    selected_year = st.sidebar.selectbox('Select year', year)
    selected_country = st.sidebar.selectbox('Select country', country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in olympics ' + str(selected_year))
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall Medal tally of '+ selected_country)
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal tally of '+ selected_country + ' in olympics ' + str(selected_year))
    st.table(helper.medal_fetch(df,selected_year,selected_country))

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Olympics stats')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.participating_nations_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating nations over years')
    st.plotly_chart(fig)

    events_over_time = helper.participating_nations_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over years')
    st.plotly_chart(fig)

    athletes_over_time = helper.participating_nations_time(df,'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over years')
    st.plotly_chart(fig)

    st.title('No of events over years including every sport')
    x = df.drop_duplicates(['Year','Sport','Event'])
    fig, ax = plt.subplots(figsize=(15, 20))
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

if user_menu == 'Top performer':
    st.title('Most successful athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)
    st.table(helper.successful_athletes(df, selected_sport))

if user_menu == 'Country-wise Analysis':
    st.title('Country wise performance')
    nation_list = df['region'].dropna().unique().tolist()
    nation_list.sort()
    selected_nation = st.sidebar.selectbox('Select nation', nation_list)
    st.title('Medal tally of ' + selected_nation)
    nation_sport, nation_medal = helper.country_wise(df, selected_nation)
    fig = px.line(nation_medal, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(selected_nation + ' performance in every sport')
    fig, ax = plt.subplots(figsize=(15, 20))
    ax = sns.heatmap(nation_sport.pivot_table(index='Sport',columns='Year',values='Medal', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Top 10 players of ' + selected_nation)
    top10 = helper.successful_athletes_nationwise(df, selected_nation)
    st.table(top10)

if user_menu == 'Athlete wise Analysis':
    st.title('Distribution of Age wrt to Medals')
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    fig = helper.plot_athletes_age(df, 'Overview')
    fig.update_layout(autosize=False,width=800,height=400)
    st.plotly_chart(fig)

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overview')
    selected_sport = st.sidebar.selectbox('Select sport', sport_list)
    st.title('Distribution of Age wrt Sports('+selected_sport+')')
    fig = helper.plot_athletes_age(df, selected_sport)
    fig.update_layout(autosize=False,width=800,height=400)
    st.plotly_chart(fig)

    temp_df = helper.athletes_health(df, selected_sport)
    fig, ax = plt.subplots()
    st.title('Height v/s Weight')
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)

    temp_df = helper.gender(df)
    st.title('Men v/s Women participation over years')
    fig = px.line(temp_df, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Note:Some numbers may vary wrt wikipedia, Dataset have some historic issues</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

