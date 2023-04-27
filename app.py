import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np



def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7c2d48cf7426d82f447196e40fd601fb')
    data=response.json()
    url='https://image.tmdb.org/t/p/original/'+data['poster_path']
    return url

# get recommendations for content based algo
def content_recommendations(movie,index):
    # movie_index=original_data[original_data['title']==movie].index[0]
    distances=content_similarity[index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        idx=more_info.iloc[i[0]].id
        recommended_movies.append(more_info.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(idx))
    return recommended_movies,recommended_movies_posters

# get recommendations for collab based algo
def collab_recommendations(movie,id):
    tmdbId = more_info[more_info['title'] == movie].iloc[0]['id']
    movieId = links[links['tmdbId'] == tmdbId].iloc[0]['movieId']
    idx = np.where(pivot.index == movieId)[0][0]
    similar = sorted(list(enumerate(collab_similarity[idx])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    posters=[]
    for i in similar:
        item = []
        temp_df = links[links['movieId'] == pivot.index[i[0]]]
        id = temp_df.iloc[0]['tmdbId']
        title = more_info[more_info['id'] == id].iloc[0]['title']
        posters.append(fetch_poster(id))
        data.append(title)
    return data,posters


# start
# load list of movies from pkl file
# content_based_movies=pickle.load(open('final_data.pkl','rb'))
# content_based_movies_titles=content_based_movies['title'].values # extract only titles

st.set_page_config(layout="wide")
st.title('My Flix')

# load more info data
more_info=pickle.load(open('more_info.pkl','rb'))
movies_titles=more_info['title'].values

# load content similarity matrix
content_similarity=pickle.load(open('content_similarity.pkl','rb'))

# load ratings
ratings=pickle.load(open('ratings.pkl','rb'))

# load links
links=pickle.load(open('links.pkl','rb'))

# load collab similarity
collab_similarity=pickle.load(open('collab_similarity.pkl','rb'))

# load pivot table
pivot=pickle.load(open('collab_pivot.pkl','rb'))



if __name__=='__main__':
    str=['----------SELECT----------','Method 1','Method 2']
    options=st.selectbox('How may I recommed movie to you ?',str)
    #for movies search bar

    if options==str[1]:
        selected_movie = st.selectbox('Get Your Recommendations Here',movies_titles)

        # for button
        if st.button('Select'):
            index=more_info[more_info['title']==selected_movie].index[0]
            id=more_info.iloc[index]['id']

            st.subheader("Your Movie Of Choice Is")
            with st.container():
                col1,col2,col3,col4,col5=st.columns(5)
                with col1:
                    st.subheader('TITLE')
                with col2:
                    st.subheader('RATING')
                with col3:
                    st.subheader('DIRECTOR')
                with col4:
                    st.subheader('CAST')
                with col5:
                    st.subheader('OVERVIEW')

            with st.container():
                url=fetch_poster(id)
                title=more_info.iloc[index]['title']
                ratings = more_info.iloc[index]['vote_average']
                genres = more_info.iloc[index]['genres']
                cast = more_info.iloc[index]['cast']
                overview = more_info.iloc[index]['overview']
                director = more_info.iloc[index]['crew']
                with col1:
                    st.image(url, width=150, caption=title)
                with col2:
                    st.write(ratings)
                with col3:
                    st.write(director)
                with col4:
                    st.write(cast)
                with col5:
                    st.write(overview)

            st.write('____________________')

            st.subheader('Here are the Recommendations for you')

            titles,posters=content_recommendations(selected_movie,index)
            with st.container():
                col1, col2, col3, col4 ,col5= st.columns(5)
                with col1:
                    st.subheader('TITLE')
                with col2:
                    st.subheader('RATING')
                with col3:
                    st.subheader('DIRECTOR')
                with col4:
                    st.subheader('CAST')
                with col5:
                    st.subheader('OVERVIEW')

                gen=[]
                over=[]
                cast=[]
                director=[]
                ratings=[]
                for i in range(8):
                    tit=titles[i]
                    pos=posters[i]
                    idx=more_info[more_info['title'] == tit].index[0]
                        # pos.append(posters)
                        # tit.append(titles)
                    cast.append(more_info.iloc[idx]['cast'])
                    gen.append(more_info.iloc[idx]['genres'])
                    over.append(more_info.iloc[idx]['overview'])
                    ratings.append(more_info.iloc[idx]['vote_average'])
                    director.append(more_info.iloc[idx]['crew'])

                    st.write('____________________')

                    col1, col2, col3, col4 ,col5= st.columns(5)
                    with col1:
                        st.image(posters[i],width=150, caption=titles[i])
                    with col2:
                        st.write(ratings[i])
                    with col3:
                        st.write(director[i])
                    with col4:
                        st.write(cast[i])
                    with col5:
                        st.write(over[i])

    if options==str[2]:
        selected_movie = st.selectbox('Get Your Recommendations Here', movies_titles)

        # for button
        if st.button('Select'):
            index = more_info[more_info['title'] == selected_movie].index[0]
            id = more_info.iloc[index]['id']

            st.subheader("Your Movie Of Choice Is")
            with st.container():
                col1, col2, col3, col4,col5 = st.columns(5)
                with col1:
                    st.subheader('TITLE')
                with col2:
                    st.subheader('RATING')
                with col3:
                    st.subheader('DIRECTOR')
                with col4:
                    st.subheader('CAST')
                with col5:
                    st.subheader('OVERVIEW')

            with st.container():
                url = fetch_poster(id)
                title = more_info.iloc[index]['title']
                genres = more_info.iloc[index]['genres']
                cast = more_info.iloc[index]['cast']
                overview = more_info.iloc[index]['overview']
                director=more_info.iloc[index]['crew']
                ratings=more_info.iloc[index]['vote_average']
                with col1:
                    st.image(url, width=150, caption=title)
                with col2:
                    st.write(ratings)
                with col3:
                    st.write(director)
                with col4:
                    st.write(cast)
                with col5:
                    st.write(overview)

            st.write('____________________')

            st.subheader('Here are the Recommendations for you')

            titles, posters = collab_recommendations(selected_movie, index)
            with st.container():
                col1, col2, col3, col4,col5 = st.columns(5)
                with col1:
                    st.subheader('TITLE')
                with col2:
                    st.subheader('RATING')
                with col3:
                    st.subheader('DIRECTOR')
                with col4:
                    st.subheader('CAST')
                with col5:
                    st.subheader('OVERVIEW')

                gen = []
                over = []
                cast = []
                ratings=[]
                director=[]
                for i in range(10):
                    tit = titles[i]
                    pos = posters[i]
                    idx = more_info[more_info['title'] == tit].index[0]
                    # pos.append(posters)
                    # tit.append(titles)
                    cast.append(more_info.iloc[idx]['cast'])
                    gen.append(more_info.iloc[idx]['genres'])
                    over.append(more_info.iloc[idx]['overview'])
                    ratings.append(more_info.iloc[idx]['vote_average'])
                    director.append(more_info.iloc[idx]['crew'])

                    st.write('____________________')

                    col1, col2, col3, col4,col5 = st.columns(5)
                    with col1:
                        st.image(posters[i], width=150, caption=titles[i])
                    with col2:
                        st.write(ratings[i])

                    with col3:
                        st.write(director[i])

                    with col4:
                        st.write(cast[i])

                    with col5:
                        st.write(overview[i])
