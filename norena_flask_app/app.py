from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import uuid
import re


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
        'nik': '3173123456780001',
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
        'nik': '3173123456780002',
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
        'nik': '3173123456780003',
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
        'nik': '3173123456780004',
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
        'nik': '3173123456780005',
        'tgl_lahir': '1995-07-01',
        'no_hp': '086134567894',
        'alamat': 'Diponegoro No.88, Semarang',
        'produk': ['Kartu Kredit', 'Deposito'],
        'keterangan': 'Ingin investasi yang aman',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Dikenalkan sebagai alternatif investasi', 'date': '2024-12-22'}
        ]
    },
    {
        'id': '6',
        'nama': 'Fitri Ayu',
        'nik': '3173123456780006',
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
        'nik': '3173123456780007',
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



def mask_no_hp(no_hp, role):
    if role in ['admin', 'pic']:
        return no_hp
    if no_hp and len(no_hp) >= 4:
        return 'xxxxxx' + no_hp[-4:]
    return 'xxxxxx0000'

def mask_alamat(alamat, role):
    if role in ['admin', 'pic']:
        return alamat

    if not alamat:
        return 'xxx'

    import re
    parts = re.split(r'[\s,]+', alamat.strip())

    masked_parts = []
    for i, word in enumerate(parts):
        if len(word) <= 4:
            masked = word[0] + 'x' * (len(word) - 1) if len(word) > 1 else word
        else:
            visible = word[:4]
            masked = visible + 'x' * (len(word) - 4)

        if i == 0 or i == len(parts) - 1:
            masked_parts.append(masked)
        else:
            masked_parts.append('x' * len(word))

    return ' '.join(masked_parts)

@app.route('/')
def home():
    return redirect(url_for('login'))

def generate_product_recommendation(nasabah):
    import datetime
    today = datetime.date.today()
    tgl_lahir = datetime.datetime.strptime(nasabah['tgl_lahir'], '%Y-%m-%d').date()
    usia = (today - tgl_lahir).days // 365

    produk_dimiliki = set([p.lower() for p in nasabah.get('produk', [])])
    keterangan = nasabah.get('keterangan', '').lower()

    keyword_map = {
        'investasi': ['Reksa Dana', 'Investasi Online', 'Deposito'],
        'anak': ['Pendidikan Anak', 'Asuransi Jiwa', 'Tabungan Rencana'],
        'menikah': ['Asuransi Jiwa', 'Tabungan Rencana'],
        'rumah': ['KPR', 'Renovation Loan'],
        'renovasi': ['Renovation Loan'],
        'pindah': ['Tabungan Rencana'],
        'perjalanan': ['Travel Insurance'],
        'luar negeri': ['Travel Insurance', 'Kartu Kredit'],
        'digital': ['Investasi Online'],
        'pensiun': ['Pensiun Plus', 'Asuransi Kesehatan'],
        'mobile banking': ['Investasi Online', 'Reksa Dana']
    }

    produk_script = {
        "Kartu Kredit": "Dengan Kartu Kredit ini, Bapak/Ibu bisa menikmati kemudahan bertransaksi harian, mendapatkan promo menarik, dan merasa lebih tenang saat bepergian. Semuanya dalam satu genggaman.",
        "KPR": "Kami tahu memiliki rumah sendiri adalah impian banyak orang. Dengan KPR ini, impian itu bisa terwujud lebih cepat dan mudah, tanpa harus menunggu terlalu lama.",
        "KKB": "Kami ingin Bapak/Ibu bisa memiliki kendaraan idaman tanpa harus memberatkan. Cicilan ringan dan proses cepat siap membantu mobilitas Anda sehari-hari.",
        "Tahapan BCA": "Tahapan BCA cocok untuk Bapak/Ibu yang ingin mengatur keuangan dengan nyaman. Semua transaksi mudah, aman, dan bisa diakses kapan saja.",
        "Deposito": "Jika Bapak/Ibu ingin dana aman namun tetap bertumbuh, Deposito bisa jadi solusi terbaik. Bunga menarik dan fleksibel, cocok untuk simpanan jangka menengah dan panjang.",
        "BCA Syariah": "Untuk Bapak/Ibu yang ingin produk keuangan berbasis nilai-nilai Islam, kami hadirkan BCA Syariah dengan prinsip bagi hasil yang adil dan transparan.",
        "BCA Life": "Melindungi orang tercinta adalah bentuk cinta yang nyata. BCA Life hadir untuk memberikan ketenangan bagi Anda dan keluarga, jika hal tak terduga terjadi.",
        "Reksa Dana": "Reksa Dana cocok bagi Bapak/Ibu yang ingin mulai berinvestasi tapi tak punya banyak waktu. Dana dikelola profesional agar bisa tumbuh dengan optimal.",
        "Investasi Online": "Ingin masa depan lebih terjamin tapi tetap fleksibel? Investasi Online bisa diakses di mana pun, kapan pun. Mudah, aman, dan menguntungkan.",
        "Pendidikan Anak": "Masa depan anak adalah prioritas setiap orang tua. Dengan produk ini, Bapak/Ibu bisa menyiapkan pendidikan terbaik sejak dini, tanpa beban di kemudian hari.",
        "Pensiun Plus": "Nikmati masa pensiun dengan tenang dan nyaman. Kami bantu Bapak/Ibu menyiapkan hari tua agar tetap aktif, bahagia, dan bebas kekhawatiran finansial.",
        "Asuransi Jiwa": "Melindungi keluarga saat kita sudah tak ada, adalah bentuk kasih sayang yang tak ternilai. Asuransi Jiwa memberikan perlindungan finansial untuk mereka yang Bapak/Ibu cintai.",
        "Asuransi Kesehatan": "Kesehatan adalah aset terpenting. Asuransi Kesehatan hadir untuk melindungi Bapak/Ibu dari risiko biaya medis yang tak terduga, sehingga bisa fokus pada pemulihan.",
        "Travel Insurance": "Saat bepergian jauh, hal tak terduga bisa saja terjadi. Travel Insurance memberi perlindungan agar perjalanan Bapak/Ibu tetap tenang dan menyenangkan.",
        "Tabungan Rencana": "Setiap impian finansial dimulai dari perencanaan. Dengan Tabungan Rencana, Bapak/Ibu bisa menabung otomatis menuju tujuan keuangan yang lebih pasti.",
        "Renovation Loan": "Rumah adalah tempat pulang yang nyaman. Renovation Loan ini membantu Bapak/Ibu memperbaiki atau memperindah rumah tanpa perlu menguras tabungan."
    }

    rekomendasi_dari_keterangan = set()
    for keyword, produk_list in keyword_map.items():
        if keyword in keterangan:
            rekomendasi_dari_keterangan.update(produk_list)

    rekomendasi_dari_usia = set()
    if usia < 30:
        rekomendasi_dari_usia.update(['Tabungan Rencana', 'Investasi Online', 'Reksa Dana'])
    elif usia < 50:
        rekomendasi_dari_usia.update(['Kartu Kredit', 'Asuransi Jiwa', 'Deposito'])
    else:
        rekomendasi_dari_usia.update(['Pensiun Plus', 'Asuransi Kesehatan', 'Deposito'])

    gabungan = (rekomendasi_dari_keterangan | rekomendasi_dari_usia)
    hasil_akhir = [p for p in gabungan if p.lower() not in produk_dimiliki]

    if not hasil_akhir:
        fallback = ['Deposito', 'Kartu Kredit', 'Asuransi Jiwa']
        hasil_akhir = [p for p in fallback if p.lower() not in produk_dimiliki]

    # Gabungkan dengan script
    hasil_dengan_script = []
    for p in hasil_akhir:
        hasil_dengan_script.append({
            'produk': p,
            'script': produk_script.get(p, 'Produk ini direkomendasikan untuk kebutuhan Anda.')
        })

    return hasil_dengan_script

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
    pencarian_dilakukan = False
    nasabah_not_found = False
    selected_nasabah = None
    show_modal = False
    role = session.get('role')  

    if request.method == 'POST':
        nama = request.form.get('nama', '').strip().lower()
        nik = request.form.get('nik', '').strip()

        if nama:
            filtered = [n for n in nasabah_list if nama in n['nama'].lower()]
            if nik:
                filtered = [n for n in filtered if n.get('nik') == nik]

            if not filtered:
                nasabah_not_found = True
            else:
                for n in filtered:
                    hasil_pencarian.append({
                        'id': n['id'],
                        'nama': n['nama'],
                        'tgl_lahir': n['tgl_lahir'],
                        'no_hp': mask_no_hp(n['no_hp'],role),
                        'alamat': mask_alamat(n['alamat'],role),
                        'produk': n['produk'],
                        'keterangan': n.get('keterangan', ''),
                        'referral_histori': n.get('referral_histori', []),
                        'rekomendasi_ai': generate_product_recommendation(n)
                    })

                if len(filtered) == 1:
                    selected_nasabah = filtered[0]
                    rekomendasi_ai = generate_product_recommendation(selected_nasabah)
        else:
            nasabah_not_found = True

        pencarian_dilakukan = True

    return render_template(
        'dashboard_karyawan.html',
        username=session.get('username'),
        hasil_pencarian=hasil_pencarian,
        rekomendasi_ai=rekomendasi_ai,
        selected_nasabah=selected_nasabah,
        show_modal=show_modal,
        pencarian_dilakukan=pencarian_dilakukan,
        nasabah_not_found=nasabah_not_found,
        produk_list=produk_list
    )

@app.route('/tambah_nasabah', methods=['POST'])
def tambah_nasabah():
    nama = request.form['nama'].strip()
    nik = request.form['nik'].strip()
    tgl_lahir = request.form['tgl_lahir'].strip()
    produk = request.form.getlist('produk')
    keterangan = request.form['keterangan']

    # 🔒 Validasi NIK hanya angka dan panjang 16 digit
        # VALIDASI NIK
    if not nik.isdigit() or len(nik) != 16:
        return render_template('dashboard_karyawan.html',
                               username=session.get('username'),
                               hasil_pencarian=[],
                               rekomendasi_ai=[],
                               selected_nasabah=None,
                               show_modal=False,
                               pencarian_dilakukan=False,
                               nasabah_not_found=False,
                               produk_list=produk_list,
                               error_message="NIK harus terdiri dari 16 digit angka.")

    # VALIDASI NOMOR HP
    if not no_hp.isdigit():
        return render_template('dashboard_karyawan.html',
                               username=session.get('username'),
                               hasil_pencarian=[],
                               rekomendasi_ai=[],
                               selected_nasabah=None,
                               show_modal=False,
                               pencarian_dilakukan=False,
                               nasabah_not_found=False,
                               produk_list=produk_list,
                               error_message="Nomor HP harus dimulai dengan 08 dan memiliki 10-13 digit angka.")
                            

    # CEK DUPLIKASI NIK
    if any(n['nik'] == nik for n in nasabah_list):
        return render_template('dashboard_karyawan.html',
                               username=session.get('username'),
                               hasil_pencarian=[],
                               rekomendasi_ai=[],
                               selected_nasabah=None,
                               show_modal=False,
                               pencarian_dilakukan=False,
                               nasabah_not_found=False,
                               produk_list=produk_list,
                               error_message="NIK sudah terdaftar, silakan gunakan NIK lain.")
        
    nasabah_id = str(uuid.uuid4())[:8]
    new_nasabah = {
        'id': nasabah_id,
        'nama': nama,
        'nik': nik,
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
    
    show_modal = True
    role = session.get('role')
    if role != 'karyawan':
        return redirect(url_for('login'))
    
    nasabah = next((n for n in nasabah_list if n['id'] == nasabah_id), None)
    if nasabah:
        # ⬇️ Optional masking jika role bukan admin/pic
        nasabah['no_hp'] = mask_no_hp(nasabah['no_hp'], role)
        nasabah['alamat'] = mask_alamat(nasabah['alamat'], role)
        rekomendasi_ai = generate_product_recommendation(nasabah) if nasabah else []
        
    else:
        rekomendasi_ai = []
    
    if not nasabah:
        return redirect(url_for('dashboard_karyawan'))
   
    return render_template('profil_nasabah.html', nasabah=nasabah,rekomendasi_ai=rekomendasi_ai,show_modal=show_modal)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
