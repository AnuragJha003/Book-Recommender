from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
#with open('popular.pkl', 'rb') as f:
#      popular_df = pd.read_pickle(f)
#with open('pt.pkl', 'rb') as f:
#      pt = pd.read_pickle(f)
#with open('books.pkl', 'rb') as f:
#      books = pd.read_pickle(f)
#with open('similarity_score.pkl', 'rb') as f:
#      similarity_score = pd.read_pickle(f) 
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg-ratings'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    #def recommend(book_name):
    #index fetch
    index=np.where(pt.index==user_input)[0][0] #fetching index
    #distances=similarity_score[index]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:11]
    data=[] #to store all of the related details 
    for i in similar_items:
        item=[]
        #print(pt.index[i[0]])#index get and the name in the pt pivot table  
        temp_df=books[books['Book-Title'] == pt.index[i[0]]]
        #we dont want duplicates so store it in temp df
        # #print(temp_df.drop_duplicates('Book-Title')['Book-Author'])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
        #print the entire row of details print it matching the conditon 
        # #return data
    print(data)
    return render_template('recommend.html',data=data)
        #user input is being received 


if __name__=='__main__':
    app.run(debug=False)
