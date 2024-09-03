from flask import Flask, render_template, request
import pickle as pkl
import pandas as pd

popular = pkl.load(open('popular_news.pkl','rb'))
subset_news = pd.read_csv('subset_news_article.csv')
unique_headlines_indices = list(subset_news[['headline']].values.ravel())
similarity_matrix = pkl.load(open('similarity_matrix.pkl','rb'))
app = Flask(__name__)
@app.route('/')

def hello_world():
    return render_template('index.html', category=popular['category'].values.tolist(),
                           link=popular['link'].values.tolist(), headline=popular['headline'].values.tolist(),
                           author=popular['authors'].values.tolist(), pub_Date=subset_news['date'].values.tolist())

@app.route('/recommend')

def recommend():
    return render_template('recommend.html')

@app.route('/recommend_article',methods=["POST"])

def give_recommend():
    sim_mat = similarity_matrix

    user_input = str(request.form.get('user_input'))

    # Get the index corresponding to original_title
    idx = unique_headlines_indices.index(user_input)

    # Get the pairwise similarity score
    similarity_score = list(enumerate(sim_mat[idx]))

    # Sort the article
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # Score of the 10 most similar Articles
    similarity_score = similarity_score[0:5]

    # Article indices
    article_indices = [i[0] for i in similarity_score]

    data = []

    for i in article_indices:
        item = []

        item.append(subset_news['category'].values[i])
        item.append(subset_news['link'].values[i])
        item.append(subset_news['headline'].values[i])
        item.append(subset_news['authors'].values[i])
        item.append(subset_news['date'].values[i])

        data.append(item)

    return render_template('recommend.html',data_list=data)

if __name__ == '__main__':
    app.run(debug=True)
