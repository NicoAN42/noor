from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'noreana_secret_key'

# Dummy user login data
users = {
    'karyawan1': {'password': '1234', 'role': 'karyawan'},
    'pic1': {'password': '1234', 'role': 'pic'},
    'admin1': {'password': '1234', 'role': 'admin'}
}


nasabah_list = [
    {
        'id': '1',
        'nama': 'Andi Wijaya',
        'tgl_lahir': '2025-06-13',
        'no_hp': '081234567890',
        'alamat': 'Jl. Merdeka No.1, Jakarta',
        'produk': ['KPR', 'Kartu Kredit'],
        'keterangan': 'Tertarik dengan produk investasi',
        'referral_histori': [
            {'product': 'Deposito', 'description': 'Rekomendasi untuk deposito jangka panjang', 'date': '2024-10-01'},
            {'product': 'Asuransi', 'description': 'Direkomendasikan untuk perlindungan keluarga', 'date': '2025-03-15'}
        ]
    },
    {
        'id': '2',
        'nama': 'Budi Santoso',
        'tgl_lahir': '1985-08-30',
        'no_hp': '082134567891',
        'alamat': 'Jl. Sudirman No.55, Bandung',
        'produk': ['Kartu Kredit'],
        'keterangan': 'Sering bepergian ke luar negeri',
        'referral_histori': [
            {'product': 'Travel Insurance', 'description': 'Sesuai kebutuhan perjalanan luar negeri', 'date': '2025-01-20'}
        ]
    },
    {
        'id': '3',
        'nama': 'Citra Lestari',
        'tgl_lahir': '1993-11-22',
        'no_hp': '083134567892',
        'alamat': 'Jl. Asia Afrika No.3, Surabaya',
        'produk': ['Tabungan Tahapan', 'KPR'],
        'keterangan': 'Sedang membangun rumah',
        'referral_histori': [
            {'product': 'Renovation Loan', 'description': 'Cocok untuk biaya tambahan pembangunan', 'date': '2025-05-02'}
        ]
    },
    {
        'id': '4',
        'nama': 'Dedi Gunawan',
        'tgl_lahir': '1979-03-09',
        'no_hp': '085134567893',
        'alamat': 'Jl. Gajah Mada No.77, Medan',
        'produk': ['Kredit Motor'],
        'keterangan': 'Baru pindah ke kota ini',
        'referral_histori': [
            {'product': 'Tabungan Rencana', 'description': 'Membantu mengatur keuangan ke depan', 'date': '2025-06-10'}
        ]
    },
    {
        'id': '5',
        'nama': 'Eka Prasetya',
        'tgl_lahir': '1995-07-01',
        'no_hp': '086134567894',
        'alamat': 'Jl. Diponegoro No.88, Semarang',
        'produk': ['Kartu Kredit', 'Deposito'],
        'keterangan': 'Ingin investasi yang aman',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Dikenalkan sebagai alternatif investasi', 'date': '2024-12-22'}
        ]
    },
    {
        'id': '6',
        'nama': 'Fitri Ayu',
        'tgl_lahir': '1988-02-14',
        'no_hp': '087134567895',
        'alamat': 'Jl. Malioboro No.5, Yogyakarta',
        'produk': ['Asuransi Jiwa'],
        'keterangan': 'Menikah dan memiliki anak',
        'referral_histori': [
            {'product': 'Pendidikan Anak', 'description': 'Sesuai rencana pendidikan anak', 'date': '2025-02-14'}
        ]
    },
    {
        'id': '7',
        'nama': 'Gilang Saputra',
        'tgl_lahir': '1991-09-17',
        'no_hp': '089134567896',
        'alamat': 'Jl. Kartini No.10, Makassar',
        'produk': ['Tabungan Tahapan'],
        'keterangan': 'Aktif menggunakan mobile banking',
        'referral_histori': [
            {'product': 'Investasi Online', 'description': 'Direkomendasikan untuk investasi digital', 'date': '2025-04-01'}
        ]
    }
]
produk_list = ["Kartu Kredit", "KPR", "KKB", "Tahapan BCA", "Deposito", "BCA Syariah", "BCA Life"]

@app.route('/')
def home():
    return redirect(url_for('login'))

def generate_product_recommendation(nasabah):
    import datetime
    today = datetime.date.today()
    tgl_lahir = datetime.datetime.strptime(nasabah['tgl_lahir'], '%Y-%m-%d').date()
    age = (today - tgl_lahir).days // 365

    if age < 30:
        return ['Tabungan Rencana', 'Investasi Online', 'Reksa Dana']
    elif age < 50:
        return ['Deposito', 'Kartu Kredit', 'Asuransi Jiwa']
    else:
        return ['Pensiun Plus', 'Asuransi Kesehatan', 'Deposito']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard_karyawan'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard/karyawan', methods=['GET', 'POST'])
def dashboard_karyawan():
    if session.get('role') != 'karyawan':
        return redirect(url_for('login'))

    hasil_pencarian = []
    rekomendasi_ai = []
    selected_nasabah = None
    show_modal = False

    if request.method == 'POST':
        nama = request.form.get('nama_nasabah', '').strip().lower()
        tgl_lahir = request.form.get('tgl_lahir', '').strip()

        hasil_pencarian = [n for n in nasabah_list if nama in n['nama'].lower()]
        if tgl_lahir:
            hasil_pencarian = [n for n in hasil_pencarian if n['tgl_lahir'] == tgl_lahir]

        if not hasil_pencarian:
            show_modal = True
        elif len(hasil_pencarian) == 1:
            selected_nasabah = hasil_pencarian[0]
            rekomendasi_ai = generate_product_recommendation(selected_nasabah)

    return render_template(
        'dashboard_karyawan.html',
        username=session.get('username'),
        hasil_pencarian=hasil_pencarian,
        rekomendasi_ai=rekomendasi_ai,
        selected_nasabah=selected_nasabah,
        show_modal=show_modal
    )

@app.route('/tambah_nasabah', methods=['POST'])
def tambah_nasabah():
    nama = request.form['nama'].strip()
    tgl_lahir = request.form['tgl_lahir'].strip()
    produk = request.form.getlist('produk')
    keterangan = request.form['keterangan']

    nasabah_id = str(uuid.uuid4())[:8]
    new_nasabah = {
        'id': nasabah_id,
        'nama': nama,
        'tgl_lahir': tgl_lahir,
        'produk': produk,
        'keterangan': keterangan,
        'referral_histori': []
    }

    nasabah_list.append(new_nasabah)

    if 'referral_produk' in request.form and request.form['referral_produk']:
        produk = request.form['referral_produk']
        ref_ket = request.form['referral_keterangan']
        new_nasabah['referral_histori'].append({
            'produk': produk,
            'keterangan': ref_ket,
            'tanggal': datetime.now().strftime('%Y-%m-%d')
        })

    return redirect(url_for('dashboard_karyawan'))

@app.route('/tambah_referral', methods=['POST'])
def tambah_referral():
    nasabah_id = request.form['nasabah_id']
    produk = request.form['produk']
    keterangan = request.form['keterangan']

    for nasabah in nasabah_list:
        if nasabah['id'] == nasabah_id:
            nasabah['referral_histori'].append({
                'produk': produk,
                'keterangan': keterangan,
                'tanggal': datetime.now().strftime('%Y-%m-%d')
            })
            break

    return redirect(url_for('dashboard_karyawan'))

@app.route('/nasabah/<nasabah_id>')
def profil_nasabah(nasabah_id):
    if session.get('role') != 'karyawan':
        return redirect(url_for('login'))
    nasabah = next((n for n in nasabah_list if n['id'] == nasabah_id), None)
    return render_template('profil_nasabah.html', nasabah=nasabah)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
