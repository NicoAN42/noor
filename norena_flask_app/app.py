from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import uuid
import re
from flask import flash, redirect
from flask import send_file, flash
from flask import jsonify, request
import pandas as pd, io, secrets, zipfile
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from datetime import datetime
import uuid
import pandas as pd
import io, secrets, zipfile, tempfile, os, re
import xlsxwriter


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
produk_list = ["Kartu Kredit", "KPR", "KKB", "Tahapan BCA", "BCA Syariah", "BCA Life","Reksa Dana","Investasi Online","Deposito","Pendidikan Anak","Asuransi Jiwa","Tabungan Rencana","Renovation Loan","Travel insurance","Pensiun Plus","Asuransi Kesehatan"]
    


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
        uname = request.form['username']
        pwd = request.form['password']
        user = users.get(uname)

        if user and user['password'] == pwd:
            session['username'] = uname
            session['role'] = user['role']

            if user['role'] == 'karyawan':
                return redirect(url_for('dashboard_karyawan'))
            elif user['role'] == 'pic':
                return redirect(url_for('dashboard_pic'))
            elif user['role'] == 'admin':
                return redirect(url_for('dashboard_admin'))
        else:
            flash('Username atau password salah', 'login_error')

    return render_template('login.html')

@app.route('/dashboard/pic', methods=['GET'])
def dashboard_pic():
    if session.get('role') != 'pic':
        return redirect(url_for('login'))

    role = session.get('role')

    # Untuk PIC, tampilkan data tanpa masking
    # (jika ingin masking, logika bisa disesuaikan di bawah)
    masked_nasabah_list = []
    for n in nasabah_list:
        masked_nasabah_list.append({
            'id': n['id'],
            'nama': n['nama'],
            'nik': n['nik'],
            'tgl_lahir': n['tgl_lahir'],
            'no_hp': n['no_hp'],  # Unmasked
            'alamat': n['alamat'],  # Unmasked
            'produk': n.get('produk', []),
            'keterangan': n.get('keterangan', ''),
            'referral_histori': n.get('referral_histori', [])
        })

    return render_template(
        'dashboard_pic.html',
        username=session.get('username'),
        nasabah_list=masked_nasabah_list,
        produk_list=produk_list,
        show_add_modal=request.args.get('show_add_modal') == '1'
    )

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
                        'nik': n['nik'],
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
    role = session.get('role')
    nama = request.form.get('nama', '').strip()
    nik = request.form.get('nik', '').strip()
    tgl_lahir = request.form.get('tgl_lahir', '').strip()
    produk_direferensikan = request.form.get('produk_direferensikan', '').strip()
    keterangan = request.form.get('keterangan', '').strip()

    if role == 'karyawan':
        no_hp = "-"
        alamat = "-"
    else:
        no_hp = request.form.get('no_hp', '').strip()
        alamat = request.form.get('alamat', '').strip()
        

    def return_with_error(msg):
        flash(msg, "nasabah_error")
        if role == 'pic':
            return render_template(
                'dashboard_pic.html',
                username=session.get('username'),
                nasabah_list=nasabah_list,
                produk_list=produk_list,
                show_add_modal=True,
                form_data={
                    'nama': nama,
                    'nik': nik,
                    'no_hp': no_hp,
                    'alamat': alamat,
                    'tgl_lahir': tgl_lahir,
                    'produk_direferensikan': produk_direferensikan,
                    'keterangan': keterangan
                }
            )
        else:
            return redirect(url_for('dashboard_karyawan', show_add_modal=1))  # fallback aman

    # === Validasi ===
    if not nama:
        return return_with_error("Nama wajib diisi.")
    if not nik or not nik.isdigit() or len(nik) != 16:
        return return_with_error("NIK harus terdiri dari 16 digit angka.")
    if any(n['nik'] == nik for n in nasabah_list):
        return return_with_error("NIK sudah terdaftar, silakan gunakan NIK lain.")
    try:
        datetime.strptime(tgl_lahir, '%Y-%m-%d')
    except ValueError:
        return return_with_error("Format tanggal lahir tidak valid. Gunakan format YYYY-MM-DD.")

    if role != 'karyawan':
        if not no_hp.startswith('08') or not no_hp.isdigit() or not (10 <= len(no_hp) <= 13):
            return return_with_error("Nomor HP harus dimulai dengan 08 dan memiliki 10-13 digit angka.")
        if not alamat:
            return return_with_error("Alamat wajib diisi.")

    if not produk_direferensikan:
        return return_with_error("Produk yang direferensikan wajib dipilih.")

    # === Simpan Data Nasabah Baru ===
    nasabah_id = str(uuid.uuid4())[:8]
    new_nasabah = {
        'id': nasabah_id,
        'nama': nama,
        'nik': nik,
        'no_hp': no_hp,
        'alamat': alamat,
        'tgl_lahir': tgl_lahir,
        'produk': [],
        'keterangan': keterangan,
        'referral_histori': [{
            'product': produk_direferensikan,
            'description': keterangan,
            'date': datetime.now().strftime('%Y-%m-%d')
        }],
        'created_by': session.get('username')
    }

    nasabah_list.append(new_nasabah)
    flash("Nasabah baru berhasil ditambahkan.", "success")

    if role == 'pic':
        return redirect(url_for('dashboard_pic'))
    elif role == 'karyawan':
        return redirect(url_for('dashboard_karyawan'))
    else:
        return redirect(url_for('login'))

@app.route('/tambah_referral', methods=['POST'])
def tambah_referral():
    nasabah_id = request.form['nasabah_id']
    produk = request.form['produk']
    keterangan = request.form['keterangan']

    for nasabah in nasabah_list:
        if nasabah['id'] == nasabah_id:
            nasabah['referral_histori'].append({
                'product': produk,
                'description': keterangan,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            break

    flash("Referral produk berhasil ditambahkan.", "success")
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
   
    return render_template('profil_nasabah.html', nasabah=nasabah,rekomendasi_ai=rekomendasi_ai,show_modal=show_modal,produk_list=produk_list)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    # flash("Anda telah logout.", "success")
    return redirect(url_for('login'))


@app.route('/validate-username')
def validate_username():
    username = request.args.get('username', '').strip()

    # Simulasi validasi: ganti logika ini sesuai kebutuhan database kamu
    valid_usernames = ['admin1', 'karyawan1', 'pic1']  # Contoh dummy data

    is_valid = username in valid_usernames

    return jsonify({'valid': is_valid})

@app.route('/pic/get_nasabah')
def pic_get_nasabah():
    nid = request.args.get('id')
    n = next((x for x in nasabah_list if x['id'] == nid), None)
    if n:
        n['rekomendasi_ai'] = generate_product_recommendation(n)
    return jsonify(n or {})

@app.route('/pic/edit_nasabah', methods=['POST'])
def pic_edit_nasabah():
    nid = request.form.get('id')
    if not nid:
        return jsonify({'error': 'ID nasabah tidak ditemukan'}), 400

    # Temukan nasabah dari list
    n = next((x for x in nasabah_list if x['id'] == nid), None)
    if not n:
        return jsonify({'error': 'Nasabah tidak ditemukan'}), 404

    # Update field umum
    for f in ('nama', 'nik', 'tgl_lahir', 'no_hp', 'alamat', 'keterangan'):
        if f in request.form:
            n[f] = request.form[f]

    # Ambil list produk yang dicentang (checkbox)
    produk_dimiliki = request.form.getlist('produk')  # <-- ini penting!
    n['produk'] = produk_dimiliki  # update ke field produk

    flash('Data nasabah berhasil diperbarui', 'success')
    return ('', 200)


@app.route('/pic/export_excel', methods=['POST'])
def pic_export_excel():
    import tempfile, os
    data = request.get_json()
    search = data.get('search', '').strip().lower()
    filter_produk = data.get('filterProduk', '').strip()
    filter_tanggal = data.get('filterTanggal', '').strip()

    # Nama file berdasarkan filter
    nama_filter = f"{filter_produk or 'semua'}_{filter_tanggal or 'semua'}"
    safe_nama = re.sub(r'[^\w\-]', '_', nama_filter.strip().lower())
    excel_filename = f'referral_{safe_nama}.xlsx'
    password_filename = f'password_{safe_nama}.txt'

    # Buat DataFrame dari nasabah_list
    df = pd.DataFrame([
        {
            'ID': n['id'],
            'Nama': n['nama'],
            'NIK': n['nik'],
            'Tanggal Lahir': n['tgl_lahir'],
            'No HP': n['no_hp'],
            'Alamat': n['alamat'],
            'Produk Dimiliki': ', '.join(n.get('produk', [])),
            'Keterangan': n.get('keterangan', ''),
            'Referral Terakhir': n['referral_histori'][-1]['date'] if n['referral_histori'] else '',
            'Produk Referral Terakhir': n['referral_histori'][-1]['product'] if n['referral_histori'] else ''
        }
        for n in nasabah_list
    ])

    # Filter pencarian (nama, nik, alamat)
    if search:
        df = df[df.apply(lambda row:
            search in str(row['Nama']).lower() or
            search in str(row['NIK']).lower() or
            search in str(row['Alamat']).lower(),
            axis=1
        )]

    # Filter produk/tanggal: logika OR (salah satu cocok)
    if filter_produk or filter_tanggal:
        df = df[df.apply(lambda row:
            (filter_produk and row['Produk Referral Terakhir'].lower() == filter_produk.lower()) or
            (filter_tanggal and row['Referral Terakhir'] == filter_tanggal),
            axis=1
        )]

    # ===== Buat Excel File dengan 2 Sheet dan Proteksi =====
    password = secrets.token_urlsafe(8)
    tmpdir = tempfile.mkdtemp()
    excel_path = os.path.join(tmpdir, excel_filename)
    password_path = os.path.join(tmpdir, password_filename)

    import xlsxwriter
    workbook = xlsxwriter.Workbook(excel_path)

    # Sheet 1: Informasi
    info_sheet = workbook.add_worksheet('Informasi')
    info_sheet.write('A1', 'Data ini bersifat rahasia dan dilindungi password.')
    info_sheet.protect(password)

    # Sheet 2: Data Nasabah (terproteksi dan disembunyikan)
    data_sheet = workbook.add_worksheet('Data Nasabah')
    for col_idx, col_name in enumerate(df.columns):
        data_sheet.write(0, col_idx, col_name)

    for row_idx, row in enumerate(df.itertuples(index=False), start=1):
        for col_idx, val in enumerate(row):
            data_sheet.write(row_idx, col_idx, val)

    data_sheet.protect(password)
    data_sheet.hide()  # disembunyikan

    workbook.close()

    # Simpan file password terpisah
    with open(password_path, 'w') as f:
        f.write(f'Password: {password}')

    # Simpan path ke session
    session['export_excel_path'] = excel_path
    session['export_password_path'] = password_path
    session['export_excel_name'] = excel_filename
    session['export_password_name'] = password_filename

    return jsonify({
        'success': True,
        'excel_url': url_for('download_export_excel'),
        'password_url': url_for('download_export_password')
    })

@app.route('/download/export_excel')
def download_export_excel():
    path = session.get('export_excel_path')
    name = session.get('export_excel_name')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404


@app.route('/download/export_password')
def download_export_password():
    path = session.get('export_password_path')
    name = session.get('export_password_name')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404

if __name__ == '__main__':
    app.run(debug=True)
