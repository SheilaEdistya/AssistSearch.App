# AssistSearch.App

🔍 Assist Search – Aplikasi Pencarian Jasa ART & Babysitter

Assist Search adalah aplikasi desktop berbasis Python yang dirancang untuk memudahkan pengguna dalam mencari, memilih, dan memesan jasa Asisten Rumah Tangga (ART) dan Babysitter secara cepat dan efisien. Aplikasi ini dikembangkan sebagai proyek mata kuliah Struktur Data dan Algoritma, memanfaatkan kombinasi struktur data Queue dan algoritma sorting Timsort.

Tujuan Utama:

- Menyediakan platform pencarian jasa ART & babysitter berbasis kriteria.
- Mempermudah proses pemesanan dan pencatatan transaksi.
- Mengelola data pemesanan secara efisien dengan sistem antrian (Queue).
- Memberikan pengalaman digital dalam rekrutmen pekerja rumah tangga secara aman dan terpercaya.

🧩 Fitur-Fitur Utama
1. Autentikasi Pengguna
    - Registrasi dan login menggunakan username & password.
    - Validasi keamanan sederhana untuk akses sistem.

2. Pencarian Jasa ART & Babysitter

    - Pengguna dapat memfilter calon pekerja berdasarkan:
      - Asal Kota
      - Agama
      - Rating
    - Data ditampilkan dalam tabel interaktif dengan rating visual (bintang ⭐).

3. Detail Profil Pekerja
   
    Informasi mendalam seperti:
    - Nama, usia, asal, pengalaman, status kerja, keterampilan, gaji, dan foto.
    - Tombol "Pesan" dan "Exit" tersedia untuk lanjut atau kembali.

4. Formulir Pemesanan
   - Nama
   - Alamat
   - Nomor HP
   - Tanggal pemesanan (via kalender)
   - Data disimpan dalam file CSV.

5. Pembayaran & Antrian
    - Pilihan metode pembayaran: Transfer (BRI, BNI, BCA) atau QRIS.
    - Sistem antrian menggunakan Queue FIFO: pemesan lebih awal diproses terlebih dahulu.

6. Riwayat Pemesanan
    - Menampilkan daftar semua pemesanan yang telah dilakukan pengguna.
    - Tersimpan dalam file data_customer.csv.

Manfaat Aplikasi:
- Efisiensi waktu: pencarian dan pemesanan jasa dilakukan dalam hitungan menit.
- Transparansi: informasi pekerja ditampilkan dengan detail dan akurat.
- Aksesibilitas: aplikasi desktop dengan antarmuka grafis yang ramah pengguna.
- Keamanan data: pemesanan hanya dilakukan setelah pembayaran dikonfirmasi.
