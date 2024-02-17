from flask import Flask, render_template, request
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="db_dokter",
        port=8889
    )
    return conn

def get_doctor_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, pendidikan, nama, nama_title, spesialis FROM dokter")
    doctors_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    doctor_data = get_doctor_data()

    combined_data = [' '.join([d['pendidikan'].lower(), d['nama'].lower(), d['spesialis'].lower()]) for d in doctor_data]

    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(combined_data)
    feature_names = vectorizer.get_feature_names_out()

    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Dapatkan indeks fitur dengan similarity dan buat daftar term relevan
    relevant_indices = query_vector.toarray().flatten().nonzero()[0]
    relevant_features = [feature_names[i] for i in relevant_indices]

    # Siapkan data untuk DataFrame
    data = []
    for idx, doc_vector in enumerate(tfidf_matrix.toarray()):
        if cosine_similarities[idx] > 0:
            doc_terms = {feature_names[i]: doc_vector[i] for i in relevant_indices if doc_vector[i] > 0}
            if doc_terms:  # Hanya jika ada term relevan
                doc_data = {
                    'Doctor Name': doctor_data[idx]['nama_title'],
                    **doc_terms,
                    'Cosine Similarity': cosine_similarities[idx]
                }
                data.append(doc_data)

    # Jika tidak ada data yang cocok, kembalikan pesan atau DataFrame kosong
    if not data:
        return render_template('search.html', message="No matching results.", query=query)

    # Buat DataFrame dari data yang dikumpulkan
    tfidf_df = pd.DataFrame(data)

    # Urutkan DataFrame berdasarkan skor similarity
    tfidf_df_sorted = tfidf_df.sort_values(by='Cosine Similarity', ascending=False)

    # Konversi DataFrame ke HTML table
    tfidf_table_html = tfidf_df_sorted.to_html(classes='tfidf-table', float_format='%.3f', index=False)

    # Kirim HTML table ke template
    return render_template('search.html', tfidf_table=tfidf_table_html, query=query)

if __name__ == '__main__':
    app.run(debug=True)
