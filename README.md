**Dashboard Monitoring & Otomatisasi Hidroponik**
Sebuah prototipe aplikasi desktop untuk memantau dan mengontrol sistem pertanian hidroponik, dibangun dengan Python dan Tkinter. Proyek ini mengikuti arsitektur Model-View-Controller (MVC) untuk memisahkan logika data, antarmuka pengguna, dan kontrol sistem.

**Fitur Utama**
Dashboard Real-time: Memantau parameter kunci lingkungan seperti pH, Suhu, Kelembapan, Level Air, dan Intensitas Cahaya.
Visualisasi Data: Grafik riwayat untuk pH dan Suhu, serta indikator batang vertikal untuk Level Air, memberikan pemahaman visual yang cepat tentang kondisi sistem.
Kontrol Manual & Otomatis:
Kontrol Manual: Pengguna dapat secara manual menyesuaikan pH, level air, serta menyalakan/mematikan lampu dan kipas.
Otomatisasi Cerdas: Jika diaktifkan, sistem akan secara otomatis menjaga parameter lingkungan sesuai dengan profil tanaman yang dipilih.
Profil Tanaman: Pilih jenis tanaman (misalnya, Selada, Tomat, Cabai) dan sistem akan secara otomatis menggunakan setpoint ideal untuk pH, suhu, dan jadwal pencahayaan.
Sistem Notifikasi: Memberikan peringatan visual di dashboard jika ada parameter yang keluar dari rentang ideal atau jika level air terlalu rendah.
Simulasi Lingkungan Terpisah: Dilengkapi dengan environment.py yang mensimulasikan perubahan data sensor secara alami. Modul ini dapat dengan mudah diganti dengan sensor fisik (seperti Arduino atau Raspberry Pi) tanpa mengubah kode inti aplikasi.
Kustomisasi Tampilan: Antarmuka pengguna (UI) dapat dengan mudah diubah warnanya dengan memodifikasi file ui_config.py.

**Arsitektur**
Proyek ini menggunakan pola desain Model-View-Controller (MVC):

model.py: Bertanggung jawab untuk mengelola semua data dan status aplikasi. Ia tidak tahu apa-apa tentang tampilan.
view.py: Bertanggung jawab untuk semua elemen antarmuka pengguna (GUI) yang dibuat dengan Tkinter. Ia hanya menampilkan data dan meneruskan aksi pengguna ke Controller.
controller.py: Otak dari aplikasi. Ia menjadi jembatan antara Model dan View, mengambil data dari lingkungan, memperbarui Model, dan memerintahkan View untuk menampilkan perubahan.
environment.py: Mensimulasikan dunia nyata. Modul ini menghasilkan data sensor dan merespons perintah dari Controller.
main.py: Titik masuk utama aplikasi yang menginisialisasi dan menghubungkan semua komponen MVC.
ui_config.py: File konfigurasi terpusat untuk semua pengaturan visual seperti warna dan font.
