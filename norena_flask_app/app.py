from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'noreana_secret_key'

# Dummy users
users = {
    'karyawan1': {'password': '1234', 'role': 'karyawan'},
    'pic1': {'password': '1234', 'role': 'pic'},
    'admin1': {'password': '1234', 'role': 'admin'}
}

# Dummy nasabah data
nasabah_data = [
    {'id': 1, 'nama': 'Andi Wijaya', 'telepon': '081234567890', 'produk': ['Kartu Kredit'], 'keterangan': 'Nasabah loyal', 'referral': []},
    {'id': 2, 'nama': 'Rina Marlina', 'telepon': '082112345678', 'produk': ['KPR', 'Deposito'], 'keterangan': 'Tertarik produk asuransi', 'referral': []},
    {'id': 3, 'nama': 'Budi Santoso', 'telepon': '085312341234', 'produk': [], 'keterangan': '', 'referral': []},
    {'id': 4, 'nama': 'Dewi Lestari', 'telepon': '081223344556', 'produk': ['Asuransi Jiwa'], 'keterangan': '', 'referral': []},
    {'id': 5, 'nama': 'Joko Susilo', 'telepon': '089912345678', 'produk': ['Kartu Debit'], 'keterangan': 'Butuh bantuan layanan online', 'referral': []}
]

produk_list = ["Kartu Kredit", "Kartu Debit", "KPR", "Deposito", "Asuransi Jiwa", "Asuransi Umum"]

def generate_rekomendasi(nasabah):
    if 'Kartu Kredit' not in nasabah['produk']:
        return "Direkomendasikan produk Kartu Kredit karena belum dimiliki."
    if 'Asuransi Jiwa' not in nasabah['produk']:
        return "Pertimbangkan penawaran Asuransi Jiwa untuk perlindungan lebih."
    return "Nasabah sudah memiliki produk utama. Bisa ditawarkan layanan investasi."

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            if user['role'] == 'karyawan':
                return redirect(url_for('dashboard_karyawan'))
            elif user['role'] == 'pic':
                return redirect(url_for('dashboard_pic'))
            elif user['role'] == 'admin':
                return redirect(url_for('dashboard_admin'))
        else:
            return render_template('login.html', error='Username atau password salah.')

    return render_template('login.html')

@app.route('/dashboard/karyawan', methods=['GET', 'POST'])
def dashboard_karyawan():
    if session.get('role') != 'karyawan':
        return redirect(url_for('login'))

    search_result = None
    rekomendasi = None
    referral_history = []
    show_add_form = False

    if request.method == 'POST':
        nama = request.form.get('nama', '').strip().lower()
        for nasabah in nasabah_data:
            if nama in nasabah['nama'].lower():
                search_result = nasabah
                rekomendasi = generate_rekomendasi(nasabah)
                referral_history = [
                    {
                        'produk': r['produk'],
                        'keterangan': r.get('keterangan', ''),
                        'tanggal': r.get('tanggal', datetime.now().strftime("%d %B %Y"))
                    }
                    for r in nasabah.get('referral', [])
                ]
                break
        if not search_result:
            show_add_form = True

    return render_template('dashboard_karyawan.html',
                           username=session.get('username'),
                           nasabah=search_result,
                           rekomendasi=rekomendasi,
                           referral_history=referral_history,
                           produk_list=produk_list,
                           show_add_form=show_add_form)

@app.route('/tambah_nasabah', methods=['POST'])
def tambah_nasabah():
    nama = request.form['nama']
    telepon = request.form['no_hp']
    alamat = request.form['alamat']
    keterangan = request.form.get('keterangan', '')

    new_id = max(n['id'] for n in nasabah_data) + 1
    nasabah_data.append({
        'id': new_id,
        'nama': nama,
        'telepon': telepon,
        'alamat': alamat,
        'keterangan': keterangan,
        'produk': [],
        'referral': []
    })
    return redirect(url_for('dashboard_karyawan'))

@app.route('/tambah_referral', methods=['POST'])
def tambah_referral():
    nasabah_id = int(request.form['nasabah_id'])
    produk = request.form['produk']
    keterangan = request.form.get('keterangan', '')

    for nasabah in nasabah_data:
        if nasabah['id'] == nasabah_id:
            if produk not in nasabah['produk']:
                nasabah['produk'].append(produk)
            nasabah['referral'].append({
                'produk': produk,
                'keterangan': keterangan,
                'tanggal': datetime.now().strftime("%d %B %Y")
            })
            break
    return redirect(url_for('dashboard_karyawan'))

@app.route('/nasabah/<int:nasabah_id>', methods=['GET'])
def view_nasabah(nasabah_id):
    if session.get('role') != 'karyawan':
        return redirect(url_for('login'))

    for nasabah in nasabah_data:
        if nasabah['id'] == nasabah_id:
            rekomendasi = generate_rekomendasi(nasabah)
            return render_template('nasabah_detail.html', nasabah=nasabah, rekomendasi=rekomendasi)
    return redirect(url_for('dashboard_karyawan'))

@app.route('/dashboard/pic')
def dashboard_pic():
    if session.get('role') != 'pic':
        return redirect(url_for('login'))
    return render_template('dashboard_pic.html', username=session.get('username'))

@app.route('/dashboard/admin')
def dashboard_admin():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('dashboard_admin.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/validate-username')
def validate_username():
    username = request.args.get('username')
    if username in users:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})


if __name__ == '__main__':
    app.run(debug=True)
