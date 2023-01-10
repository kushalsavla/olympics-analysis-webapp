
import streamlit as st
import pandas as pd
import preprocessing,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

#
#
df1 = pd.read_csv('athlete_events.csv')
df2 = pd.read_csv('noc_regions.csv')
#
olympics_df = preprocessing.preprocess(df1, df2)

st.sidebar.header("Olympics Tally")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise analysis', 'Athlete-wise Analysis')
)

# st.dataframe(olympics_df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(olympics_df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(olympics_df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = olympics_df['Year'].unique().shape[0] - 1
    cities = olympics_df['City'].unique().shape[0]
    sports = olympics_df['Sport'].unique().shape[0]
    events = olympics_df['Event'].unique().shape[0]
    athletes = olympics_df['Name'].unique().shape[0]
    nations = olympics_df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(olympics_df, 'region')
    fig = px.plot(nations_over_time, kind='line', x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(olympics_df, 'Event')
    fig = px.plot(events_over_time, kind='line', x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(olympics_df, 'Name')
    fig = px.plot(athlete_over_time, kind='line', x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("Number of events(every sport) over time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = olympics_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0),
                     annot=True)
    st.pyplot(fig)

    st.title('Most successful athletes')
    sport_list = olympics_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_successful(olympics_df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise analysis':
    st.title('Country-wise medal analysis')
    country_list = olympics_df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_list)
    country_df = helper.yearwise_medal_tally(olympics_df, selected_country)
    fig = px.plot(country_df, kind='line', x='Year', y='Medal')
    st.title("Medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in following events")
    pt = helper.country_event_heatmap(olympics_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)
    top10 = helper.most_successful_countrywise(olympics_df, selected_country)
    st.table(top10)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = olympics_df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = olympics_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(olympics_df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x= temp_df['Weight'],y= temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(olympics_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)
