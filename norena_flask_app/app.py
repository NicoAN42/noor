from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from datetime import datetime
import uuid
import re
import pandas as pd
import secrets
import tempfile
import os
import xlsxwriter
from functools import wraps
from flask import session, redirect, url_for
from flask import redirect, url_for, session, flash
from functools import wraps
from flask import redirect, url_for, session, request, flash, render_template
from functools import wraps
from flask import session, redirect, url_for, request, g




app = Flask(__name__)
app.secret_key = 'noreana_secret_key'

# Dummy user login data
users = {
    'karyawan1': {'password': '1234', 'role': 'karyawan'},
    'pic1': {'password': '1234', 'role': 'pic'},
    'admin1': {'password': '1234', 'role': 'admin'},
    'superadmin1': {'password': '1234', 'role': 'superadmin'}
}

user_list = [
{
'id': 'u001',
'username': 'karyawan1',
'password': '1234',
'role': 'karyawan'
},
{
'id': 'u002',
'username': 'pic1',
'password': '1234',
'role': 'pic'
},
{
'id': 'u003',
'username': 'admin1',
'password': '1234',
'role': 'admin'
},
{
'id': 'u004',
'username': 'superadmin1',
'password': '1234',
'role': 'superadmin'
}
]


nasabah_list = [
    {
        'id': '1',
        'nama': 'Andi Wijaya',
        'nik': '3173123456780001',
        'tgl_lahir': '1989-06-13',
        'no_hp': '081234567890',
        'alamat': 'Jl. Merdeka No.1, Jakarta',
        'produk': ['KPR', 'BCA Card'],
        'keterangan': 'Tertarik dengan produk investasi dan persiapan pensiun',
        'referral_histori': [
            {'product': 'Deposito Berjangka', 'description': 'Rekomendasi simpanan jangka menengah', 'date': '2024-10-01'},
            {'product': 'Reksa Dana', 'description': 'Investasi untuk diversifikasi portofolio', 'date': '2025-01-15'},
            {'product': 'Pensiun Plus', 'description': 'Persiapan dana hari tua', 'date': '2025-03-01'}
        ]
    },
    {
        'id': '2',
        'nama': 'Budi Santoso',
        'nik': '3173123456780002',
        'tgl_lahir': '1985-08-30',
        'no_hp': '082134567891',
        'alamat': 'Jl. Sudirman No.55, Bandung',
        'produk': ['BCA Visa Black'],
        'keterangan': 'Sering bepergian ke luar negeri untuk bisnis',
        'referral_histori': [
            {'product': 'Asuransi Kesehatan', 'description': 'Perlindungan perjalanan luar negeri', 'date': '2025-01-20'},
            {'product': 'BCA Singapore Airlines KrisFlyer', 'description': 'Tukar transaksi menjadi miles', 'date': '2025-04-22'}
        ]
    },
    {
        'id': '3',
        'nama': 'Citra Lestari',
        'nik': '3173123456780003',
        'tgl_lahir': '1993-11-22',
        'no_hp': '083134567892',
        'alamat': 'Jl. Asia Afrika No.3, Surabaya',
        'produk': ['Tahapan BCA', 'KPR'],
        'keterangan': 'Sedang membangun rumah dan menabung untuk keluarga',
        'referral_histori': [
            {'product': 'Tabungan Rencana', 'description': 'Tabungan otomatis untuk renovasi rumah', 'date': '2025-05-02'},
            {'product': 'Asuransi Jiwa', 'description': 'Proteksi keluarga setelah menikah', 'date': '2025-06-01'}
        ]
    },
    {
        'id': '4',
        'nama': 'Dedi Gunawan',
        'nik': '3173123456780004',
        'tgl_lahir': '1979-03-09',
        'no_hp': '085134567893',
        'alamat': 'Jl. Gajah Mada No.77, Medan',
        'produk': ['KKB'],
        'keterangan': 'Baru pindah tugas ke kota ini, butuh kendaraan baru',
        'referral_histori': [
            {'product': 'Tahapan BCA', 'description': 'Tabungan utama berbasis prinsip konvensional', 'date': '2025-04-10'},
            {'product': 'Tabungan Rencana', 'description': 'Perencanaan keuangan keluarga baru', 'date': '2025-06-10'}
        ]
    },
    {
        'id': '5',
        'nama': 'Eka Prasetya',
        'nik': '3173123456780005',
        'tgl_lahir': '1995-07-01',
        'no_hp': '086134567894',
        'alamat': 'Jl. Diponegoro No.88, Semarang',
        'produk': ['Deposito Berjangka', 'Sakuku'],
        'keterangan': 'Ingin investasi aman dan aktif menggunakan dompet digital',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Diversifikasi investasi', 'date': '2024-12-22'},
            {'product': 'Asuransi Jiwa', 'description': 'Perlindungan jangka panjang dengan manfaat investasi', 'date': '2025-03-10'}
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
        'keterangan': 'Menikah dan memiliki anak, memikirkan pendidikan anak',
        'referral_histori': [
            {'product': 'Pendidikan Anak', 'description': 'Dana pendidikan anak', 'date': '2025-02-14'},
            {'product': 'Tabungan Rencana', 'description': 'Perencanaan menabung jangka panjang', 'date': '2025-04-01'}
        ]
    },
    {
        'id': '7',
        'nama': 'Gilang Saputra',
        'nik': '3173123456780007',
        'tgl_lahir': '1991-09-17',
        'no_hp': '089134567896',
        'alamat': 'Jl. Kartini No.10, Makassar',
        'produk': ['Tahapan Xpresi', 'Flazz'],
        'keterangan': 'Aktif menggunakan mobile banking dan cashless lifestyle',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Investasi digital mudah diakses via aplikasi', 'date': '2025-04-01'},
            {'product': 'KlikBCA', 'description': 'Akses perbankan dari rumah', 'date': '2025-06-12'}
        ]
    },
    {
        'id': '8',
        'nama': 'Hendra Saputra',
        'nik': '3173123456780008',
        'tgl_lahir': '1990-05-11',
        'no_hp': '081234567897',
        'alamat': 'Jl. Mangga Dua No.10, Jakarta',
        'produk': ['BCA Card', 'Flazz'],
        'keterangan': 'Aktif berbelanja online dan suka cashback',
        'referral_histori': [
            {'product': 'KlikBCA', 'description': 'Transaksi aman dari rumah', 'date': '2025-01-02'},
            {'product': 'Reksa Dana', 'description': 'Investasi dari cashback kartu kredit', 'date': '2025-04-01'}
        ]
    },
    {
        'id': '9',
        'nama': 'Intan Maharani',
        'nik': '3173123456780009',
        'tgl_lahir': '1997-03-08',
        'no_hp': '082234567898',
        'alamat': 'Jl. Dipatiukur No.12, Bandung',
        'produk': ['Tahapan Xpresi'],
        'keterangan': 'Mahasiswi aktif yang senang menabung dan investasi kecil',
        'referral_histori': [
            {'product': 'Sakuku', 'description': 'Dompet digital untuk anak muda', 'date': '2025-02-01'},
            {'product': 'Reksa Dana', 'description': 'Investasi dengan dana kecil', 'date': '2025-05-01'}
        ]
    },
    {
        'id': '10',
        'nama': 'Joko Prabowo',
        'nik': '3173123456780010',
        'tgl_lahir': '1983-12-05',
        'no_hp': '083234567899',
        'alamat': 'Jl. Guntur No.8, Bekasi',
        'produk': ['KPR', 'Asuransi Jiwa'],
        'keterangan': 'Memiliki rumah dan keluarga, ingin masa depan aman',
        'referral_histori': [
            {'product': 'Tabungan Rencana', 'description': 'Menabung untuk biaya pendidikan anak', 'date': '2025-02-20'},
            {'product': 'Pensiun Plus', 'description': 'Persiapan dana pensiun', 'date': '2025-04-10'}
        ]
    },
    {
        'id': '11',
        'nama': 'Alexander Tuku',
        'nik': '3173123456780011',
        'tgl_lahir': '1992-06-21',
        'no_hp': '084234567800',
        'alamat': 'Jl. Jendral Sudirman No.3, Yogyakarta',
        'produk': ['Tahapan BCA'],
        'keterangan': 'Guru sekolah yang rajin menabung',
        'referral_histori': [
            {'product': 'Tabungan Rencana', 'description': 'Tabungan bulanan untuk liburan', 'date': '2025-03-11'},
            {'product': 'Asuransi Kesehatan', 'description': 'Perlindungan untuk keluarga', 'date': '2025-05-01'}
        ]
    },
    {
        'id': '12',
        'nama': 'Leonardo Yusuf',
        'nik': '3173123456780012',
        'tgl_lahir': '1975-09-14',
        'no_hp': '085234567801',
        'alamat': 'Jl. Letjen Sutoyo No.22, Semarang',
        'produk': ['Deposito Berjangka'],
        'keterangan': 'Pengusaha ingin simpan dana besar dengan aman',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Alternatif dari deposito', 'date': '2025-04-15'},
            {'product': 'Asuransi Jiwa', 'description': 'Perlindungan tambahan dari risiko', 'date': '2025-06-10'}
        ]
    },
    {
        'id': '13',
        'nama': 'Maria Agnes',
        'nik': '3173123456780013',
        'tgl_lahir': '1986-10-18',
        'no_hp': '086234567802',
        'alamat': 'Jl. Gatot Subroto No.5, Denpasar',
        'produk': ['BCA Visa Black'],
        'keterangan': 'Travel blogger yang sering bepergian',
        'referral_histori': [
            {'product': 'Asuransi Kesehatan', 'description': 'Perlindungan saat bepergian', 'date': '2025-01-30'},
            {'product': 'BCA Singapore Airlines KrisFlyer', 'description': 'Bonus miles dari belanja luar negeri', 'date': '2025-03-22'}
        ]
    },
    {
        'id': '14',
        'nama': 'Nurul Aini',
        'nik': '3173123456780014',
        'tgl_lahir': '1999-01-01',
        'no_hp': '087234567803',
        'alamat': 'Jl. Panglima Polim No.9, Surabaya',
        'produk': ['Sakuku'],
        'keterangan': 'Suka transaksi digital dan pakai QRIS',
        'referral_histori': [
            {'product': 'KlikBCA', 'description': 'Pantau transaksi dan tabungan', 'date': '2025-02-20'},
            {'product': 'Tahapan Xpresi', 'description': 'Tabungan untuk anak muda', 'date': '2025-05-18'}
        ]
    },
    {
        'id': '15',
        'nama': 'Oscar Fernando',
        'nik': '3173123456780015',
        'tgl_lahir': '1994-04-04',
        'no_hp': '088234567804',
        'alamat': 'Jl. Merpati No.45, Pontianak',
        'produk': ['KKB'],
        'keterangan': 'Baru beli mobil untuk keluarga',
        'referral_histori': [
            {'product': 'Asuransi Jiwa', 'description': 'Proteksi saat kredit kendaraan', 'date': '2025-03-12'},
            {'product': 'Tabungan Rencana', 'description': 'Cicil asuransi dan dana darurat', 'date': '2025-06-01'}
        ]
    },
    {
        'id': '16',
        'nama': 'Putri Melati',
        'nik': '3173123456780016',
        'tgl_lahir': '1996-12-25',
        'no_hp': '089234567805',
        'alamat': 'Jl. Sisingamangaraja No.99, Medan',
        'produk': ['Flazz', 'Tahapan Xpresi'],
        'keterangan': 'Aktif dalam komunitas kreatif dan UMKM',
        'referral_histori': [
            {'product': 'KlikBCA', 'description': 'Pantau pemasukan usaha dari rumah', 'date': '2025-03-20'},
            {'product': 'Reksa Dana', 'description': 'Dana cadangan hasil usaha', 'date': '2025-05-29'}
        ]
    },
    {
        'id': '17',
        'nama': 'Rangga Nugroho',
        'nik': '3173123456780017',
        'tgl_lahir': '1980-07-07',
        'no_hp': '081934567806',
        'alamat': 'Jl. Kenanga No.123, Padang',
        'produk': ['Tahapan BCA', 'Deposito Berjangka'],
        'keterangan': 'Menyiapkan dana pendidikan anak dan investasi jangka menengah',
        'referral_histori': [
            {'product': 'Pendidikan Anak', 'description': 'Perencanaan biaya sekolah', 'date': '2025-04-17'},
            {'product': 'Asuransi Jiwa', 'description': 'Proteksi kepala keluarga', 'date': '2025-06-08'}
        ]
    },
    {
        'id': '18',
        'nama': 'Santi Dewi',
        'nik': '3173123456780018',
        'tgl_lahir': '1990-06-30',
        'no_hp': '081244567891',
        'alamat': 'Jl. Melati No.10, Jakarta',
        'produk': ['Tahapan BCA'],
        'keterangan': 'Baru memulai karier, ingin menabung',
        'referral_histori': []
    },
    {
        'id': '19',
        'nama': 'Agus Salim',
        'nik': '3173123456780019',
        'tgl_lahir': '1982-10-10',
        'no_hp': '082255567892',
        'alamat': 'Jl. Ahmad Yani No.12, Bogor',
        'produk': ['KPR', 'Asuransi Jiwa'],
        'keterangan': 'Mempersiapkan masa depan keluarga',
        'referral_histori': [
            {'product': 'Pensiun Plus', 'description': 'Dana pensiun dari sekarang', 'date': '2025-02-01'}
        ]
    },
    {
        'id': '20',
        'nama': 'Linda Oktaviani',
        'nik': '3173123456780020',
        'tgl_lahir': '1995-11-11',
        'no_hp': '083266567893',
        'alamat': 'Jl. Suryopranoto No.20, Surabaya',
        'produk': ['BCA Card', 'Sakuku'],
        'keterangan': 'Aktif di media sosial, sering belanja online',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Investasi kecil-kecilan dari cashback', 'date': '2025-01-20'},
            {'product': 'KlikBCA', 'description': 'Cek transaksi belanja harian', 'date': '2025-03-01'}
        ]
    },
    {
        'id': '21',
        'nama': 'Haris Wijaya',
        'nik': '3173123456780021',
        'tgl_lahir': '1979-05-20',
        'no_hp': '084277567894',
        'alamat': 'Jl. Letda Sujono No.3, Medan',
        'produk': ['Deposito Berjangka'],
        'keterangan': 'Pensiunan yang ingin simpanan aman',
        'referral_histori': [
            {'product': 'Reksa Dana', 'description': 'Tambahan investasi lebih fleksibel', 'date': '2025-02-10'},
            {'product': 'Pensiun Plus', 'description': 'Perlindungan saat usia senja', 'date': '2025-04-25'},
            {'product': 'Asuransi Kesehatan', 'description': 'Proteksi medis untuk lansia', 'date': '2025-05-17'}
        ]
    },
    {
        'id': '22',
        'nama': 'Vina Mulia',
        'nik': '3173123456780022',
        'tgl_lahir': '1998-08-08',
        'no_hp': '085288567895',
        'alamat': 'Jl. Tunjungan No.9, Surabaya',
        'produk': ['Tahapan Xpresi', 'Flazz'],
        'keterangan': 'Mahasiswi suka gaya hidup cashless',
        'referral_histori': [
            {'product': 'Sakuku', 'description': 'Top-up digital yang praktis', 'date': '2025-01-01'}
        ]
    },
    {
        'id': '23',
        'nama': 'Yudi Hartanto',
        'nik': '3173123456780023',
        'tgl_lahir': '1987-07-07',
        'no_hp': '086299567896',
        'alamat': 'Jl. Hasanuddin No.77, Makassar',
        'produk': ['KKB'],
        'keterangan': 'Sedang mencicil mobil pribadi',
        'referral_histori': []
    },
    {
        'id': '24',
        'nama': 'Selvi Paramitha',
        'nik': '3173123456780024',
        'tgl_lahir': '1993-02-02',
        'no_hp': '087300567897',
        'alamat': 'Jl. Cendrawasih No.4, Palembang',
        'produk': ['Tahapan BCA'],
        'keterangan': 'Karyawan swasta, ingin menabung otomatis',
        'referral_histori': [
            {'product': 'Tabungan Rencana', 'description': 'Auto-debit tabungan bulanan', 'date': '2025-03-10'},
            {'product': 'Asuransi Jiwa', 'description': 'Proteksi karyawan', 'date': '2025-04-10'}
        ]
    },
    {
        'id': '25',
        'nama': 'Bayu Nugroho',
        'nik': '3173123456780025',
        'tgl_lahir': '1984-04-04',
        'no_hp': '088311567898',
        'alamat': 'Jl. Jendral Gatot Subroto No.5, Balikpapan',
        'produk': ['KlikBCA', 'Reksa Dana'],
        'keterangan': 'Pekerja kantoran yang aktif investasi',
        'referral_histori': [
            {'product': 'Deposito Berjangka', 'description': 'Dana cadangan investasi', 'date': '2025-01-12'},
            {'product': 'Asuransi Jiwa', 'description': 'Perlindungan keuangan keluarga', 'date': '2025-03-11'},
            {'product': 'Pensiun Plus', 'description': 'Persiapan hari tua sejak dini', 'date': '2025-05-19'},
            {'product': 'Tabungan Rencana', 'description': 'Tujuan liburan tahunan', 'date': '2025-06-10'}
        ]
    },
    {
        'id': '26',
        'nama': 'Mega Lestari',
        'nik': '3173123456780026',
        'tgl_lahir': '1985-12-12',
        'no_hp': '089322567899',
        'alamat': 'Jl. Majapahit No.99, Semarang',
        'produk': ['BCA Singapore Airlines KrisFlyer'],
        'keterangan': 'Pegawai ekspatriat yang sering keluar negeri',
        'referral_histori': [
            {'product': 'Asuransi Kesehatan', 'description': 'Proteksi perjalanan luar negeri', 'date': '2025-03-05'}
        ]
    },
    {
        'id': '27',
        'nama': 'Taufik Hidayat',
        'nik': '3173123456780027',
        'tgl_lahir': '1977-11-11',
        'no_hp': '081333567800',
        'alamat': 'Jl. Siliwangi No.100, Cirebon',
        'produk': ['Asuransi Jiwa'],
        'keterangan': 'Baru saja pensiun, ingin proteksi keluarga',
        'referral_histori': [
            {'product': 'Deposito Berjangka', 'description': 'Simpan dana pensiun secara aman', 'date': '2025-01-25'}
        ]
    }


]


produk_list = [
    # Simpanan & Deposito
    "Tahapan BCA", "Tahapan Xpresi", "Tahapan Berjangka", 
    "Simpanan Pelajar", "Tapres", "TabunganKu", "BCA Dollar", 
    "Deposito Berjangka", "e‑Deposito",
    # Pinjaman
    "KPR", "KKB", "KSM", "Personal Loan", "Secured Personal Loan",
    # Kartu Kredit
    "BCA Card", "BCA Everyday Card", "BCA Card Platinum",
    "BCA Smartcash", "BCA Singapore Airlines KrisFlyer",
    "BCA Visa Batman", "BCA Visa Black",
    "BCA Mastercard World", "BCA Mastercard Globe",
    "BCA Mastercard Black", "BCA Mastercard Blibli",
    "BCA mastercard tiket.com", "BCA JCB Black",
    # Investasi & Asuransi
    "Reksa Dana", "Asuransi Jiwa", "Asuransi Kesehatan",
    "Pendidikan Anak", "Tabungan Rencana", "Pensiun Plus",
    # Uang Elektronik
    "Flazz", "Sakuku"
]



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
def root_redirect():
    return redirect(url_for('login'))

def login_required(roles=None, template=None):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_function(*args, **kwargs):
            if 'username' not in session or 'role' not in session:
                return redirect(url_for('login'))
            user_role = session.get('role')
            if roles and user_role not in roles:
                return render_template(
                    template or 'access_denied.html',
                    show_access_modal=True,
                    username=session.get('username')
                )
            return view_func(*args, **kwargs)
        return decorated_function
    return decorator

@app.after_request
def add_cache_control(response):
    # Prevent browser from caching pages after logout
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


def generate_product_recommendation(nasabah):
    import datetime
    today = datetime.date.today()
    tgl_lahir = datetime.datetime.strptime(nasabah['tgl_lahir'], '%Y-%m-%d').date()
    usia = (today - tgl_lahir).days // 365

    produk_dimiliki = set([p.lower() for p in nasabah.get('produk', [])])
    keterangan = nasabah.get('keterangan', '').lower()

    keyword_map = {
    'investasi': ['Reksa Dana', 'Deposito Berjangka', 'e‑Deposito'],
    'anak': ['Pendidikan Anak', 'Tabungan Rencana'],
    'menikah': ['Tabungan Rencana', 'Asuransi Jiwa'],
    'rumah': ['KPR'],
    'renovasi': ['KPR'],
    'pindah': ['Tabungan Rencana'],
    'perjalanan': ['BCA Singapore Airlines KrisFlyer', 'BCA Mastercard tiket.com'],
    'luar negeri': ['BCA Dollar', 'BCA Singapore Airlines KrisFlyer', 'BCA Mastercard World'],
    'digital': ['Sakuku', 'Flazz', 'Tahapan Xpresi'],
    'pensiun': ['Pensiun Plus', 'Asuransi Jiwa'],
    'pelajar': ['Simpanan Pelajar', 'Tahapan Xpresi'],
    'mobil': ['KKB'],
    'kesehatan': ['Asuransi Kesehatan'],
    'usaha': ['BCA Smartcash', 'Personal Loan'],
    'harian': ['Tahapan BCA', 'Tapres', 'TabunganKu']
    }


    produk_script = {
    "Tahapan BCA": "Solusi tabungan lengkap untuk kebutuhan transaksi harian Anda. Dilengkapi kartu ATM, internet banking, dan mobile banking untuk akses kapan saja.",
    "Tahapan Xpresi": "Tabungan stylish untuk generasi muda. Tanpa buku tabungan, kartu desain unik, dan akses mobile banking untuk gaya hidup digital.",
    "Tahapan Berjangka": "Tabungan rutin dengan jangka waktu tetap untuk membantu Anda meraih tujuan finansial, seperti liburan, pendidikan, atau dana darurat.",
    "Simpanan Pelajar": "Tabungan khusus pelajar yang ringan dan aman, cocok untuk mulai belajar menabung sejak dini.",
    "Tapres": "Tabungan Prestasi BCA dengan suku bunga menarik dan layanan e-banking untuk nasabah aktif dan profesional.",
    "TabunganKu": "Tabungan tanpa biaya administrasi bulanan, cocok untuk Anda yang menginginkan solusi hemat dan praktis.",
    "BCA Dollar": "Rekening khusus valuta asing (USD/SGD) untuk keperluan bisnis, investasi, atau perjalanan ke luar negeri.",
    "Deposito Berjangka": "Produk simpanan berjangka dengan bunga kompetitif dan pilihan tenor fleksibel untuk meningkatkan nilai dana Anda.",
    "e‑Deposito": "Deposito online yang bisa dibuka langsung melalui KlikBCA. Praktis, aman, dan tetap menguntungkan.",
    "KPR": "Solusi pembiayaan untuk rumah impian Anda. Bunga kompetitif, proses mudah, dan cicilan ringan sesuai kemampuan.",
    "KKB": "Kredit kendaraan dengan pilihan tenor fleksibel dan bunga kompetitif. Dapatkan mobil impian Anda dengan lebih mudah.",
    "KSM": "Kredit Sepeda Motor BCA yang memberikan kemudahan memiliki kendaraan roda dua dengan cicilan terjangkau.",
    "Personal Loan": "Pinjaman tanpa agunan untuk kebutuhan pribadi Anda seperti renovasi, pendidikan, atau liburan.",
    "Secured Personal Loan": "Pinjaman dengan agunan yang memberikan plafon lebih besar dan bunga lebih ringan.",
    "BCA Card": "Kartu kredit utama dari BCA dengan berbagai promo menarik dan kemudahan transaksi.",
    "BCA Everyday Card": "Kartu kredit yang cocok untuk belanja sehari-hari dengan cashback dan cicilan ringan.",
    "BCA Card Platinum": "Kartu premium dengan limit besar dan fasilitas eksklusif untuk gaya hidup Anda.",
    "BCA Smartcash": "Fasilitas kredit fleksibel untuk keperluan bisnis maupun pribadi, tarik tunai mudah melalui ATM.",
    "BCA Singapore Airlines KrisFlyer": "Kartu kredit spesial untuk traveler. Tukarkan transaksi Anda menjadi KrisFlyer miles.",
    "BCA Visa Batman": "Kartu kredit edisi khusus dengan desain eksklusif dan manfaat transaksi layaknya superhero.",
    "BCA Visa Black": "Kartu premium untuk perjalanan dan transaksi global. Dilengkapi berbagai fasilitas eksklusif.",
    "BCA Mastercard World": "Kartu untuk gaya hidup kelas dunia. Nikmati benefit internasional dan layanan concierge.",
    "BCA Mastercard Globe": "Kartu kredit praktis dengan jangkauan global dan promo menarik di merchant luar negeri.",
    "BCA Mastercard Black": "Kartu prestisius dengan limit tinggi dan akses layanan eksklusif.",
    "BCA Mastercard Blibli": "Kartu kredit khusus untuk pengguna Blibli. Dapatkan cashback dan promo belanja online.",
    "BCA mastercard tiket.com": "Kartu kredit co-branding untuk traveling dan booking tiket dengan lebih hemat.",
    "BCA JCB Black": "Kartu dengan kenyamanan maksimal, cocok untuk nasabah yang sering bepergian ke Jepang dan Asia.",
    "Reksa Dana": "Investasi yang dikelola profesional, cocok untuk Anda yang ingin mengembangkan dana dengan risiko terukur.",
    "Asuransi Jiwa": "Lindungi keluarga Anda dari risiko finansial dengan asuransi jiwa BCA Life.",
    "Asuransi Kesehatan": "Proteksi kesehatan menyeluruh dari biaya medis tidak terduga. Tersedia berbagai pilihan plan.",
    "Pendidikan Anak": "Perencanaan dana pendidikan sejak dini untuk masa depan cerah buah hati Anda.",
    "Tabungan Rencana": "Tabungan berjangka otomatis dengan bunga menarik, cocok untuk target keuangan seperti menikah atau traveling.",
    "Pensiun Plus": "Solusi perencanaan pensiun dengan manfaat investasi untuk masa tua yang tenang dan mandiri.",
    "Flazz": "Kartu prabayar multifungsi untuk pembayaran tol, parkir, transportasi, dan belanja. Cukup tap dan bayar.",
    "Sakuku": "Aplikasi dompet digital dari BCA. Bisa digunakan untuk belanja online, bayar tagihan, hingga transfer sesama pengguna."
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
            elif user['role'] == 'superadmin':
                return redirect(url_for('dashboard_superadmin'))
        else:
            flash('Username atau password salah', 'login_error')

    return render_template('login.html')


@app.route('/dashboard/superadmin',methods=['GET'])
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def dashboard_superadmin():
    if session.get('role') != 'superadmin':
        return redirect(url_for('login'))
    search = request.args.get('search', '').lower()
    role_filter = request.args.get('filter_role', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    filtered_users = []
    for uname, u in users.items():
        if search and search not in uname.lower():
            continue
        if role_filter and u['role'] != role_filter:
            continue
        filtered_users.append({
            'username': uname,
            'role': u['role'],
            'password': u['password']
        })

    total_data = len(filtered_users)
    total_pages = (total_data + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = filtered_users[start:end]

    return render_template(
        'dashboard_superadmin.html',
        username=session.get('username'),
        user_list=paginated_users,
        page=page,
        pages=total_pages,
        search=search,
        role_filter=role_filter,
        access_denied=getattr(g, 'access_denied', False),
        required_role=getattr(g, 'required_role', None)
    )


@app.route('/superadmin/tambah_user', methods=['POST'])
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def tambah_user():
    if session.get('role') != 'superadmin':
        return redirect(url_for('login'))
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', '').strip()

    if not username or not password or not role:
        flash('Semua field wajib diisi.', 'danger')
        return redirect(url_for('dashboard_superadmin'))

    # Cek apakah username sudah dipakai
    if any(u['username'] == username for u in user_list):
        flash('Username sudah terdaftar.', 'danger')
        return redirect(url_for('dashboard_superadmin'))

    new_user = {
        'id': str(uuid.uuid4())[:8],
        'username': username,
        'password': password,
        'role': role
    }
    user_list.append(new_user)
    users[username] = {'password': password, 'role': role}

    flash('User berhasil ditambahkan.', 'success')
    return redirect(url_for('dashboard_superadmin'))    


@app.route('/superadmin/get_user')
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def superadmin_get_user():
    if session.get('role') != 'superadmin':
        return jsonify({'error': 'Unauthorized'}), 403
    username = request.args.get('username')
    user = users.get(username)

    if not user:
        return jsonify({'error': 'User tidak ditemukan'}), 404

    return jsonify({
        'username': username,
        'password': user['password'],
        'role': user['role']
    })


@app.route('/superadmin/edit_user', methods=['POST'])
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def superadmin_edit_user():
    if session.get('role') != 'superadmin':
     return jsonify({'error': 'Unauthorized'}), 403
    username = request.form.get('username')
    role = request.form.get('role')
    password = request.form.get('password')

    if username not in users:
        return jsonify({'error': 'User tidak ditemukan'}), 404

    # Update role
    users[username]['role'] = role

    # Update password hanya jika tidak kosong dan bukan bintang2
    if password and password != '********':
        users[username]['password'] = password

    return jsonify({'success': True})

@app.route('/superadmin/export_users', methods=['POST'])
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def superadmin_export_users():
    if session.get('role') != 'superadmin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    search = data.get('search', '').strip().lower()
    role_filter = data.get('filter_role', '').strip().lower()

    export_data = []
    for username, info in users.items():
        match_search = not search or search in username.lower()
        match_role = not role_filter or info['role'].lower() == role_filter
        if match_search and match_role:
            export_data.append({
                'Username': username,
                'Role': info['role']
            })

    if not export_data:
        return jsonify({'error': 'Tidak ada data cocok'}), 404

    password = secrets.token_urlsafe(8)
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename_excel = f"data_users_{now}.xlsx"
    filename_password = f"password_export_{now}.txt"

    tmpdir = tempfile.mkdtemp()
    excel_path = os.path.join(tmpdir, filename_excel)
    password_path = os.path.join(tmpdir, filename_password)

    workbook = xlsxwriter.Workbook(excel_path)
    info_sheet = workbook.add_worksheet("Informasi")
    data_sheet = workbook.add_worksheet("Data Users")

    info_sheet.write('A1', 'Data ini diproteksi dengan password. Silakan hubungi admin jika tidak memiliki akses.')
    info_sheet.protect(password)

    headers = ['Username', 'Role']
    for col, h in enumerate(headers):
        data_sheet.write(0, col, h)

    for row_idx, row in enumerate(export_data, start=1):
        data_sheet.write(row_idx, 0, row['Username'])
        data_sheet.write(row_idx, 1, row['Role'])

    data_sheet.protect(password)
    data_sheet.hide()
    workbook.close()

    with open(password_path, 'w') as f:
        f.write(f"Password file Excel: {password}")

    session['export_excel_path'] = excel_path
    session['export_password_path'] = password_path
    session['export_excel_name'] = filename_excel
    session['export_password_name'] = filename_password

    return jsonify({
        'success': True,
        'excel_url': url_for('download_export_excel_superadmin'),
        'password_url': url_for('download_export_password_superadmin')
    })


@app.route('/superadmin/download_excel')
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def download_export_excel_superadmin():
    path = session.get('export_excel_path')
    name = session.get('export_excel_name')
    if path and os.path.exists(path):
     return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404

@app.route('/superadmin/download_password')
@login_required(roles=['superadmin'], template='dashboard_superadmin.html')
def download_export_password_superadmin():
    path = session.get('export_password_path')
    name = session.get('export_password_name')
    if path and os.path.exists(path):
     return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404

@app.route('/dashboard/pic', methods=['GET'])
@login_required(roles=['pic'], template='dashboard_pic.html')
def dashboard_pic():
    if session.get('role') != 'pic':
        return redirect(url_for('login'))
    
    role = session.get('role')
    search = request.args.get('search', '').strip().lower()
    filter_produk = request.args.get('produk', '').strip().lower()
    filter_tanggal = request.args.get('tanggal', '').strip()

    referral_data = []

    for nasabah in nasabah_list:
        for r in nasabah.get('referral_histori', []):
            row = {
                'id': nasabah['id'],
                'nama': nasabah['nama'],
                'nik': nasabah['nik'],
                'tgl_lahir': nasabah.get('tgl_lahir', ''),
                'no_hp': mask_no_hp(nasabah.get('no_hp', ''), role),
                'alamat': mask_alamat(nasabah.get('alamat', ''), role),
                'produk_dimiliki': ', '.join(nasabah.get('produk', [])),
                'keterangan': nasabah.get('keterangan', ''),
                'referral_tanggal': r.get('date', ''),
                'referral_produk': r.get('product', ''),
                'referral_deskripsi': r.get('description', '')
            }

            # Filter logika
            nama_match = search in row['nama'].lower() or search in row['nik'].lower() or search in row['alamat'].lower() if search else True
            produk_match = row['referral_produk'].lower() == filter_produk if filter_produk else True
            tanggal_match = row['referral_tanggal'] == filter_tanggal if filter_tanggal else True

            if nama_match and produk_match and tanggal_match:
                referral_data.append(row)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_data = len(referral_data)
    total_pages = (total_data + per_page - 1) // per_page

    # Sort by date descending
    referral_data.sort(key=lambda x: x['referral_tanggal'], reverse=True)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = referral_data[start:end]

    return render_template(
        'dashboard_pic.html',
        username=session.get('username'),
        referral_list=paginated_data,
        produk_list=produk_list,
        show_add_modal=request.args.get('show_add_modal') == '1',
        role='pic',
        page=page,
        pages=total_pages,
        access_denied=getattr(g, 'access_denied', False),
        required_role=getattr(g, 'required_role', None)
    )
    
@app.route('/dashboard/karyawan', methods=['GET', 'POST'])
@login_required(roles=['karyawan'], template='dashboard_karyawan.html')
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
                    no_hp_display = n['no_hp'] if role in ['admin', 'pic'] else mask_no_hp(n['no_hp'], role)
                    alamat_display = n['alamat'] if role in ['admin', 'pic'] else mask_alamat(n['alamat'], role)
                    hasil_pencarian.append({
                    'id': n['id'],
                    'nama': n['nama'],
                    'nik': n['nik'],
                    'tgl_lahir': n['tgl_lahir'],
                    'no_hp': no_hp_display,
                    'alamat': alamat_display,
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
        produk_list=produk_list,
        role='karyawan',
        access_denied=getattr(g, 'access_denied', False),
        required_role=getattr(g, 'required_role', None)
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
                },
                access_denied=getattr(g, 'access_denied', False),
                required_role=getattr(g, 'required_role', None)
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
@login_required(roles=['karyawan'], template='dashboard_karyawan.html')
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
   
    return render_template('profil_nasabah.html', nasabah=nasabah,rekomendasi_ai=rekomendasi_ai,show_modal=show_modal,produk_list=produk_list,access_denied=getattr(g, 'access_denied', False),
        required_role=getattr(g, 'required_role', None))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    # flash("Anda telah logout.", "success")
    return redirect(url_for('login'))


@app.route('/validate-username')
def validate_username():
    username = request.args.get('username', '').strip()

    # Simulasi validasi: ganti logika ini sesuai kebutuhan database kamu
    valid_usernames = ['admin1', 'karyawan1', 'pic1','superadmin1']  # Contoh dummy data

    is_valid = username in valid_usernames

    return jsonify({'valid': is_valid})

@app.route('/pic/get_nasabah')
@login_required(roles=['pic'], template='dashboard_pic.html')
def pic_get_nasabah():
    nid = request.args.get('id')
    n = next((x for x in nasabah_list if x['id'] == nid), None)
    if n:
        n['rekomendasi_ai'] = generate_product_recommendation(n)
    return jsonify(n or {})

@app.route('/pic/edit_nasabah', methods=['POST'])
@login_required(roles=['pic'], template='dashboard_pic.html')
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
@login_required(roles=['pic'], template='dashboard_pic.html')
def pic_export_excel():
    data = request.get_json()
    search = data.get('search', '').strip().lower()
    filter_produk = data.get('filterProduk', '').strip().lower()
    filter_tanggal = data.get('filterTanggal', '').strip()
    
   # Siapkan nama file berdasarkan filter
    nama_filter = f"{filter_produk or 'semua'}_{filter_tanggal or 'semua'}"
    safe_nama = re.sub(r'[^\w\-]', '_', nama_filter)
    excel_filename = f"referral_{safe_nama}.xlsx"
    password_filename = f"password_{safe_nama}.txt"

    # Ambil semua data referral
    referral_data = []
    for n in nasabah_list:
        for r in n.get('referral_histori', []):
            referral_data.append({
                'ID': n['id'],
                'Nama': n['nama'],
                'NIK': n['nik'],
                'Tanggal Lahir': n.get('tgl_lahir', ''),
                'No HP': n.get('no_hp', ''),
                'Alamat': n.get('alamat', ''),
                'Produk Dimiliki': ', '.join(n.get('produk', [])),
                'Keterangan': n.get('keterangan', ''),
                'Tanggal Referral': r.get('date', ''),
                'Produk Referral': r.get('product', ''),
                'Deskripsi Referral': r.get('description', '')
            })

    df = pd.DataFrame(referral_data)

    # Terapkan filter pencarian dan filter produk/tanggal
    def match_filter(row):
        nama = str(row.get('Nama', '')).lower()
        nik = str(row.get('NIK', '')).lower()
        alamat = str(row.get('Alamat', '')).lower()
        produk_ref = str(row.get('Produk Referral', '')).lower()
        tanggal_ref = str(row.get('Tanggal Referral', ''))
        
        match_search = (
            not search or
            search in nama or
            search in nik or
            search in alamat
        )

        match_produk = not filter_produk or produk_ref == filter_produk
        match_tanggal = not filter_tanggal or tanggal_ref == filter_tanggal

        # Aturan kombinasi filter:
        if filter_produk and filter_tanggal:
            return match_search and match_produk and match_tanggal
        elif filter_produk:
            return match_search and match_produk
        elif filter_tanggal:
            return match_search and match_tanggal
        else:
            return match_search

    df = df[df.apply(match_filter, axis=1)]
    

    # Buat file Excel sementara dengan proteksi
    password = secrets.token_urlsafe(8)
    tmpdir = tempfile.mkdtemp()
    excel_path = os.path.join(tmpdir, excel_filename)
    password_path = os.path.join(tmpdir, password_filename)

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
    data_sheet.hide()

    workbook.close()

    # Simpan file password terpisah
    with open(password_path, 'w') as f:
        f.write(f'Password: {password}')

    # Simpan path ke session untuk endpoint download
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
@login_required(roles=['pic'], template='dashboard_pic.html')
def download_export_excel():
    path = session.get('export_excel_path')
    name = session.get('export_excel_name')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404


@app.route('/download/export_password')
@login_required(roles=['pic'], template='dashboard_pic.html')
def download_export_password():
    path = session.get('export_password_path')
    name = session.get('export_password_name')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=name)
    return 'File tidak tersedia.', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
