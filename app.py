from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time


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


def search_without_training(query, combined_data, doctor_data):
   vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
   tfidf_matrix = vectorizer.fit_transform(combined_data)
   query_vector = vectorizer.transform([query])
   cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()


   results = []
   for idx, similarity in enumerate(cosine_similarities):
       if similarity > 0.1:
           results.append({
               'id': doctor_data[idx]['id'],
               'nama_title': doctor_data[idx]['nama_title'],
               'nama': doctor_data[idx]['nama'],
               'spesialis': doctor_data[idx]['spesialis'],
               'similarity': similarity
           })
   return results


def train_model(combined_data):
   vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
   tfidf_matrix = vectorizer.fit_transform(combined_data)
   return vectorizer, tfidf_matrix


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
   query = request.args.get('query', '').lower()
   doctor_data = get_doctor_data()


   combined_data = [' '.join([d['pendidikan'].lower(), d['nama'].lower(), d['nama_title'].lower(), d['spesialis'].lower()]) for d in doctor_data]


   # Langsung melakukan pencarian tanpa pelatihan model
   start_search_time_no_training = time.time()
   results_no_training = search_without_training(query, combined_data, doctor_data)
   end_search_time_no_training = time.time()
   search_time_no_training = end_search_time_no_training - start_search_time_no_training


   # Melakukan pelatihan model dan kemudian pencarian
   start_training_time = time.time()
   vectorizer, tfidf_matrix = train_model(combined_data)
   end_training_time = time.time()
   training_time = end_training_time - start_training_time


   query_vector = vectorizer.transform([query])
   cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()


   results = []
   for idx, similarity in enumerate(cosine_similarities):
       if similarity > 0.1:
           results.append({
               'id': doctor_data[idx]['id'],
               'nama_title': doctor_data[idx]['nama_title'],
               'nama': doctor_data[idx]['nama'],
               'spesialis': doctor_data[idx]['spesialis'],
               'similarity': similarity
           })
  
   # Urutkan hasil berdasarkan nilai similarity, dari yang tertinggi ke terendah
   sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)


   return render_template('search.html', dokter_list=sorted_results, query=query,
                      search_time_no_training=round(search_time_no_training, 5),
                      training_time=round(training_time, 5))




@app.route('/feedback', methods=['POST'])
def feedback():
   dokter_id = request.form['dokter_id']
   query = request.form['query']
   relevansi = request.form['relevansi']  # 'ya' jika relevan, 'tidak' jika tidak relevan


   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute(
       'INSERT INTO feedback (dokter_id, query, relevansi) VALUES (%s, %s, %s)',
       (dokter_id, query, relevansi)
   )
   conn.commit()
   cursor.close()
   conn.close()
  
   return redirect(url_for('search', query=query, feedback_sent='true'))


@app.route('/metrics', methods=['GET'])
def calculate_metrics():
   # Mengambil query dari parameter URL. Jika tidak ada, gunakan string kosong sebagai default.
   query = request.args.get('query', default="")


   # Jika query kosong, kirim pesan error ke template.
   if not query:
       return render_template('metrics.html', error="Query tidak boleh kosong.")


   # Buka koneksi database.
   conn = get_db_connection()
   cursor = conn.cursor(dictionary=True)


   # Dapatkan semua feedback relevan untuk query yang diberikan.
   cursor.execute('SELECT relevansi FROM feedback WHERE query = %s', (query,))
   feedback_data = cursor.fetchall()


   # Menghitung TP dan FP berdasarkan feedback.
   TP = sum(f['relevansi'] == 'ya' for f in feedback_data)
   FP = sum(f['relevansi'] == 'tidak' for f in feedback_data)
   FN = 0


   # Hitung metrik.
   precision = TP / (TP + FP) if TP + FP > 0 else 0
   recall = TP / (TP + FN) if TP + FN > 0 else 0
   F1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0


   # Tutup kursor dan koneksi database.
   cursor.close()
   conn.close()


   # Kirim hasil metrik ke template metrics.html bersama dengan query.
   metrics = {
       'precision': precision,
       'recall': recall,
       'F1': F1,
       'query': query  # Pastikan variabel ini dikirim ke template.
   }


   # Render dan kembalikan template metrics.html dengan data metrik dan query.
   return render_template('metrics.html', metrics=metrics, query=query)


if __name__ == '__main__':
   app.run(debug=True)
