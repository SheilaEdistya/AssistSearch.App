import tkinter as tk
from tkinter import*
from tkinter import FLAT, Entry, Label, messagebox, Frame, Toplevel
from tkinter import ttk,font, Radiobutton
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import csv
import pandas
from collections import deque

class AssistSearch:
    def __init__(self, master):
        self.master = master
        self.frame_dsk = None
        self.master.title("AssistSearch")

        # Set default style for the whole app
        self.set_default_style()

        self.load_registered_users()

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=10)

        self.master.state("zoomed")
        self.master.resizable(width=tk.TRUE, height=tk.TRUE)
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        self.frame_bawah = Frame(self.master, width=screen_width, height=screen_height)
        self.frame_bawah.place(x=0, y=0)

        self.foto = Image.open("AssistSearch/1.png")
        self.foto = self.foto.resize((screen_width, screen_height))
        self.photoo = ImageTk.PhotoImage(self.foto)

        label_background = tk.Label(self.frame_bawah, image=self.photoo)
        label_background.place(x=0, y=0)
        label_background.photo = self.photoo

        self.label_username = tk.Label(self.frame_bawah, text="Username:", bg='#4767A5')
        self.label_username.place(x=890, y=340)

        self.entry_username = tk.Entry(self.frame_bawah)
        self.entry_username.place(x=995, y=340)

        self.label_password = tk.Label(self.frame_bawah, text="Password:", bg='#4767A5')
        self.label_password.place(x=890, y=390)

        self.entry_password = tk.Entry(self.frame_bawah, show="*")
        self.entry_password.place(x=995, y=390)

        self.btn_login = tk.Button(self.frame_bawah, text="Login", command=self.cek_login, bg='#4767A5')
        self.btn_login.place(x=960, y=500)

        self.btn_registrasi = tk.Button(self.frame_bawah, text="Registrasi", command=self.tampil_registrasi, bg='#4767A5')
        self.btn_registrasi.place(x=1045, y=500)

        self.payload_customer = {}

    def set_default_style(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', foreground='black')
        style.configure('TButton', background='white', foreground='black')
        style.configure('Treeview', background='white', fieldbackground='white', foreground='black')
        style.map('Treeview', background=[('selected', 'gray')])
        style.configure('Treeview.Heading', background='white', foreground='black')
        
    def tampil_registrasi(self):
        self.master.withdraw()
        self.window_reg = Toplevel()
        self.window_reg.title("Registrasi")
        self.window_reg.state("zoomed")
        self.window_reg.resizable(width=tk.TRUE, height=tk.TRUE)
        screen_width = self.window_reg.winfo_screenwidth()
        screen_height = self.window_reg.winfo_screenheight()

        self.frame_reg = Frame(self.window_reg, width=screen_width, height=screen_height)
        self.frame_reg.place(x=0, y=0)

        self.foto = Image.open("AssistSearch/2.png")
        self.foto = self.foto.resize((screen_width, screen_height))
        self.photoo = ImageTk.PhotoImage(self.foto)

        label_background = tk.Label(self.frame_reg, image=self.photoo)
        label_background.place(x=0, y=0)
        label_background.photo = self.photoo

        self.label_reg_username = tk.Label(self.frame_reg, text="Username:", bg='#4767A5')
        self.label_reg_username.place(x=870, y=340)

        self.entry_reg_username = tk.Entry(self.frame_reg)
        self.entry_reg_username.place(x=975, y=340)

        self.label_reg_password = tk.Label(self.frame_reg, text="Password:", bg='#4767A5')
        self.label_reg_password.place(x=870, y=390)

        self.entry_reg_password = tk.Entry(self.frame_reg)
        self.entry_reg_password.place(x=975, y=390)

        self.btn_registrasi = tk.Button(self.frame_reg, text="Registrasi", command=self.daftar_akun, bg='#4767A5')
        self.btn_registrasi.place(x=960, y=500)
        
    def load_registered_users(self):
        try:
            with open('akun.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.registered_users = {row['Username']: row['Password'] for row in reader}
        except FileNotFoundError:
            self.registered_users = {}

    def save_registered_users(self):
        with open('akun.csv', 'w', newline='') as file:
            fieldnames = ['Username', 'Password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for username, password in self.registered_users.items():
                writer.writerow({'Username': username, 'Password': password})

    def daftar_akun(self):
        username = self.entry_reg_username.get()
        password = self.entry_reg_password.get()

        if username and password:
            if 6 <= len(username) <= 20 and 6 <= len(password) <= 20:
                if any(i.islower() for i in password) and any(i.isupper() for i in password) \
                        and any(i.isdigit() for i in password) and any(ip.islower() for ip in username) \
                        and any(ip.isupper() for ip in username):
                    if any(p1.islower() for p1 in username) and any(c1.isupper() for c1 in username) \
                            and not any(c1.isdigit() for c1 in username):
                        if username in self.registered_users:
                            messagebox.showerror("Registrasi", "Username sudah terdaftar")
                        else:
                            self.registered_users[username] = password
                            messagebox.showinfo("Registrasi", "Registrasi berhasil")
                            self.save_registered_users()
                            self.pop_up()
                    else:
                        messagebox.showerror("Error", "Username hanya boleh terdiri dari huruf besar dan huruf kecil")
                else:
                    messagebox.showerror("Error", "Password harus menggunakan huruf besar, huruf kecil, angka")
            else:
                messagebox.showerror("Error", "Username dan Password harus antara 6 dan 20 karakter")
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi!")

    def pop_up(self):
        self.window_reg.destroy()
        self.master.deiconify()
        self.master.state("zoomed")

    def cek_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "" or password == "":
            messagebox.showerror("Gagal", "Username atau password tidak boleh kosong")
            return

        if username not in self.registered_users:
            messagebox.showerror("Gagal", "Username tidak terdaftar")
            return

        if self.registered_users[username] != password:
            messagebox.showerror("Gagal", "Password salah")
            return

        messagebox.showinfo("Sukses", "Login berhasil")
        self.halaman_dekstop()

    
    def tampil_riwayat_pemesanan(self):
        # Membuat window baru untuk riwayat pemesanan
        self.window_riwayat = tk.Toplevel(self.master, background='white')  # Menambahkan background di sini
        self.window_riwayat.title("Riwayat Pemesanan")
        self.window_riwayat.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")

        # Tambahkan style baru untuk Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
        style.map('Treeview', background=[('selected', 'gray')])
        style.configure('Treeview.Heading', background='white', foreground='black')

        # Tampilkan riwayat pemesanan dalam window baru dengan frame ber-background putih
        self.frame_riwayat = tk.Frame(self.window_riwayat, background='white')
        self.frame_riwayat.pack(fill=tk.BOTH, expand=True)

        # Tambahkan judul di atas tabel
        self.label_title = tk.Label(self.frame_riwayat, text="Riwayat Pemesanan", font=("Helvetica", 16, "bold"), background='white', foreground='black')
        self.label_title.pack()

        self.tree = ttk.Treeview(self.frame_riwayat, columns=("Tanggal Pemesanan", "Peran", "Nama", "Rating"), show='headings')
        self.tree.heading("Tanggal Pemesanan", text="Tanggal Pemesanan")
        self.tree.heading("Peran", text="Peran")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Rating", text="Rating")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Contoh data riwayat pemesanan
        riwayat_pemesanan = [
            {"tanggal_pemesanan": "2024-05-01", "peran": "art", "nama": "joe", "rating": 4},
            {"tanggal_pemesanan": "2024-05-03", "peran": "art", "nama": "raa", "rating": 5},
            {"tanggal_pemesanan": "2024-05-02", "peran": "babysitter", "nama": "minja", "rating": 3},
            {"tanggal_pemesanan": "2024-05-01", "peran": "art", "nama": "joe", "rating": 4},
            {"tanggal_pemesanan": "2024-05-03", "peran": "art", "nama": "raa", "rating": 5},
            {"tanggal_pemesanan": "2024-05-02", "peran": "babysitter", "nama": "minja", "rating": 3},
        ]

        riwayat_pemesanan_sorted = sorted(riwayat_pemesanan, key=lambda x: x["tanggal_pemesanan"])
        
        for pemesanan in riwayat_pemesanan_sorted:
            rating_symbol = "⭐" * pemesanan["rating"]
            self.tree.insert("", "end", values=(pemesanan["tanggal_pemesanan"], pemesanan["peran"], pemesanan["nama"], rating_symbol))

        self.btn_tutup = tk.Button(self.frame_riwayat, text="Exit", command=self.window_riwayat.destroy, background='white', foreground='black')
        self.btn_tutup.pack(pady=10)


    def halaman_dekstop(self):
        self.frame_bawah.destroy()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.frame_dsk = Frame(self.master, width=screen_width, height=screen_height)
        self.frame_dsk.place(x=0, y=0)
        self.foto = Image.open("AssistSearch/3.png")
        self.foto = self.foto.resize((screen_width, screen_height))
        self.photoo = ImageTk.PhotoImage(self.foto)
        label_background = Label(self.frame_dsk, image=self.photoo)
        label_background.place(x=0, y=0)
        label_background.photo = self.photoo

        self.label_font = font.Font(family="Helvetica", size=9, underline=True)

        self.btn_dsk_art = tk.Button(self.frame_dsk, bg="#BED7DC", text="More info", fg="black", font=self.label_font, width=8, height=2, relief=FLAT, command=self.search_art)
        self.btn_dsk_art.place(x=420, y=580)
        self.btn_dsk_babbysitter = tk.Button(self.frame_dsk, bg="#BED7DC", text="More info", fg="black", font=self.label_font, width=8, height=2, relief=FLAT, command=self.search_babysitter)
        self.btn_dsk_babbysitter.place(x=980, y=580)

        self.label_font1 = font.Font(family="Helvetica", size=11, underline=True)

        # Tombol Riwayat Pemesanan di sebelah kanan atas
        self.btn_riwayat_pemesanan = tk.Button(self.frame_dsk, text="Riwayat Pemesanan", command=self.tampil_riwayat_pemesanan, bg='#4767A5', font=self.label_font1)
        self.btn_riwayat_pemesanan.place(x=screen_width - 200, y=20)

        # Tombol Exit di sebelah kiri bawah
        self.btn_exit = tk.Button(self.frame_dsk, text="Exit", command=self.kembali_ke_login, bg='#4767A5', width=8, height=1, font=self.label_font1 )
        self.btn_exit.place(x=170, y=20)

        def close_and_open_desktop(self):
            # Pastikan jendela pencarian babysitter dihancurkan
            if hasattr(self, 'window_babysitter') and self.window_babysitter.winfo_exists():
                self.window_babysitter.destroy()

            # Buka halaman dekstop setelah jendela saat ini dihancurkan
            self.halaman_dekstop()


        

    def search_art(self):
        if self.frame_bawah:
            self.frame_bawah.destroy()

        window_art_anggun = tk.Toplevel(self.master)
        window_art_anggun.title("Daftar ART")
        window_art_anggun.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")

        frame_daftar_art = tk.Frame(window_art_anggun, background='white')
        frame_daftar_art.pack(fill=tk.BOTH, expand=True)

        # Mengganti judul teks dengan gambar
        foto_judul = Image.open("AssistSearch/art.png")
        foto_judul = foto_judul.resize((window_art_anggun.winfo_screenwidth(), 80), Image.Resampling.LANCZOS)
        photo_judul = ImageTk.PhotoImage(foto_judul)
        judul_label = tk.Label(frame_daftar_art, image=photo_judul, background='white')
        judul_label.image = photo_judul  # Menyimpan referensi image
        judul_label.pack(pady=10)

        # Filter frame
        filter_frame = tk.Frame(frame_daftar_art, background='white')
        filter_frame.pack(fill=tk.X, pady=5)

        tk.Label(filter_frame, text="Asal Kota:", background='white').pack(side=tk.LEFT, padx=5)
        asal_kota_entry = tk.Entry(filter_frame)
        asal_kota_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Agama:", background='white').pack(side=tk.LEFT, padx=5)
        agama_entry = tk.Entry(filter_frame)
        agama_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Rating:", background='white').pack(side=tk.LEFT, padx=5)
        rating_entry = tk.Entry(filter_frame)
        rating_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(filter_frame, text="Search", command=lambda: apply_filters())
        search_button.pack(side=tk.LEFT, padx=5)

        # Tabel untuk menampilkan daftar ART
        tree = ttk.Treeview(frame_daftar_art, columns=("Nama", "Agama", "Asal Kota", "Rating"), show="headings")
        tree.heading("Nama", text="Nama")
        tree.heading("Agama", text="Agama")
        tree.heading("Asal Kota", text="Asal Kota")
        tree.heading("Rating", text="Rating")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        def buka_profil(event):
            item = tree.selection()
            nama_art = tree.item(item, "values")[0]
            df = pandas.read_csv('data_art.csv', delimiter=';', skiprows=0)
            dataselected = df[df['Nama'] == nama_art]
            print(dataselected.to_dict('list'))
            self.art_detail(dataselected.to_dict('list'))
        tree.bind("<Double-1>", buka_profil)

        # Ambil dan urutkan data dari fungsi ART
        df = pandas.read_csv('data_art.csv', skiprows=0, delimiter=';')
        data_art = [list(row) for row in df.values]

        
        # Load data ART ke dalam TreeView
        data_art_sorted = sorted(data_art, key=lambda x: x[3], reverse=True)

        def load_treeview(data):
            for item in tree.get_children():
                tree.delete(item)
            for art in data:
                rating_symbol = "⭐" * int(art[4])
                if art[4] % 1 >= 0.5:
                    rating_symbol += "⭐"
                tree.insert("", "end", values=(art[0], art[2], art[3], rating_symbol))
        
        load_treeview(data_art_sorted)
        def reopen_search_art(self):
            self.search_art()


        def apply_filters():
            filtered_data = list(data_art_sorted)
            asal_kota = asal_kota_entry.get().lower()
            agama = agama_entry.get().lower()
            try:
                rating = float(rating_entry.get())
            except ValueError:
                rating = None

            if asal_kota:
                filtered_data = [item for item in filtered_data if asal_kota in item[3].lower()]
            if agama:
                filtered_data = [item for item in filtered_data if agama in item[2].lower()]
            if rating is not None:
                filtered_data = [item for item in filtered_data if float(item[4]) >= rating]

            load_treeview(filtered_data)

        # Tombol Exit
        def go_back_to_desktop():
            window_art_anggun.destroy()
            self.halaman_dekstop()

        exit_button = tk.Button(frame_daftar_art, text="Exit", command=go_back_to_desktop)
        exit_button.pack(side=tk.BOTTOM, pady=90)

    def search_babysitter(self):
        if self.frame_bawah:
            self.frame_bawah.destroy()

        window_babysitter = tk.Toplevel(self.master)
        window_babysitter.title("Daftar Babysitter")
        window_babysitter.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")

        frame_daftar_babysitter = tk.Frame(window_babysitter, bg='white')
        frame_daftar_babysitter.pack(fill=tk.BOTH, expand=True)

        # Mengganti judul teks dengan gambar
        foto_judul = Image.open("AssistSearch/baby.png")
        foto_judul = foto_judul.resize((window_babysitter.winfo_screenwidth(), 80), Image.Resampling.LANCZOS)
        photo_judul = ImageTk.PhotoImage(foto_judul)
        judul_label = tk.Label(frame_daftar_babysitter, image=photo_judul, background='white')
        judul_label.image = photo_judul  # Menyimpan referensi image
        judul_label.pack(pady=10)

        judul_label = tk.Label(frame_daftar_babysitter, text="Babysitter", font=("Helvetica", 16, "bold"), bg='white', fg='black')
        judul_label.pack(pady=10)

        filter_frame = tk.Frame(frame_daftar_babysitter, bg='white')
        filter_frame.pack(fill=tk.X, pady=5)

        tk.Label(filter_frame, text="Asal Kota:", bg='white', fg='black').pack(side=tk.LEFT, padx=5)
        asal_kota_entry = tk.Entry(filter_frame)
        asal_kota_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Agama:", bg='white', fg='black').pack(side=tk.LEFT, padx=5)
        agama_entry = tk.Entry(filter_frame)
        agama_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Rating:", bg='white', fg='black').pack(side=tk.LEFT, padx=5)
        rating_entry = tk.Entry(filter_frame)
        rating_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(filter_frame, text="Search", command=lambda: apply_filters())
        search_button.pack(side=tk.LEFT, padx=5)

        tree = ttk.Treeview(frame_daftar_babysitter, columns=("Nama", "Agama", "Asal Kota", "Rating"), show="headings")
        tree.heading("Nama", text="Nama")
        tree.heading("Agama", text="Agama")
        tree.heading("Asal Kota", text="Asal Kota")
        tree.heading("Rating", text="Rating")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        def buka_profil(event):
            item = tree.selection()
            nama_art = tree.item(item, "values")[0]
            df = pandas.read_csv('data_babysitter.csv', delimiter=';', skiprows=0)
            dataselected = df[df['Nama'] == nama_art]
            print(dataselected.to_dict('list'))
            self.babysitter_detail(dataselected.to_dict('list'))

        tree.bind("<Double-1>", buka_profil)

        df = pandas.read_csv('data_babysitter.csv', skiprows=0, delimiter=';')
        data_babysitter = [list(row) for row in df.values]




        # Sort data by Rating descending
        data_babysitter_sorted = sorted(data_babysitter, key=lambda x: x[3], reverse=True)

        def load_treeview(data):
            tree.delete(*tree.get_children())
            for babysitter in data:
                rating_symbol = "⭐" * int(babysitter[4])
                if babysitter[4] % 1 >= 0.5:
                    rating_symbol += "⭐"
                tree.insert("", "end", values=(babysitter[0], babysitter[2], babysitter[3], rating_symbol))

        load_treeview(data_babysitter_sorted)

        def apply_filters():
            filtered_data = list(data_babysitter_sorted)
            asal_kota = asal_kota_entry.get().lower()
            agama = agama_entry.get().lower()
            try:
                rating = float(rating_entry.get())
            except ValueError:
                rating = None

            if asal_kota:
                filtered_data = [item for item in filtered_data if asal_kota in item[3].lower()]
            if agama:
                filtered_data = [item for item in filtered_data if agama in item[2].lower()]
            if rating is not None:
                filtered_data = [item for item in filtered_data if float(item[4]) >= rating]

            load_treeview(filtered_data)

         # Tombol Exit
        def go_back_to_desktop():
            window_babysitter.destroy()
            self.halaman_dekstop()

        exit_button = tk.Button(frame_daftar_babysitter, text="Exit", command=go_back_to_desktop)
        exit_button.pack(side=tk.BOTTOM, pady=90)

    def tampilkan_halaman_login(self):
        # Hancurkan frame desktop jika ada
        if hasattr(self, 'frame_dsk'):
            self.frame_dsk.destroy()

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        self.frame_bawah = Frame(self.master, width=screen_width, height=screen_height)
        self.frame_bawah.place(x=0, y=0)

        self.foto = Image.open("AssistSearch/1.png")
        self.foto = self.foto.resize((screen_width, screen_height))
        self.photoo = ImageTk.PhotoImage(self.foto)

        label_background = tk.Label(self.frame_bawah, image=self.photoo)
        label_background.place(x=0, y=0)
        label_background.photo = self.photoo

        self.label_username = tk.Label(self.frame_bawah, text="Username:", bg='#4767A5')
        self.label_username.place(x=870, y=320)

        self.entry_username = tk.Entry(self.frame_bawah)
        self.entry_username.place(x=975, y=320)

        self.label_password = tk.Label(self.frame_bawah, text="Password:", bg='#4767A5')
        self.label_password.place(x=870, y=370)

        self.entry_password = tk.Entry(self.frame_bawah, show="*")
        self.entry_password.place(x=975, y=370)

        self.btn_login = tk.Button(self.frame_bawah, text="Login", command=self.cek_login, bg='#4767A5')
        self.btn_login.place(x=900, y=430)

        self.btn_registrasi = tk.Button(self.frame_bawah, text="Registrasi", command=self.tampil_registrasi, bg='#4767A5')
        self.btn_registrasi.place(x=985, y=430)
    
    def kembali_ke_login(self):
        # Hancurkan frame desktop jika ada
        if hasattr(self, 'frame_dsk'):
            self.frame_dsk.destroy()

        # Tampilkan halaman login
        self.tampilkan_halaman_login()

    def art_detail(self, payload):

        if self.frame_bawah.destroy():
            window_art_detail = tk.Toplevel(self.root)
            window_art_detail.title("Desktop")
        else:
            self.master.resizable(width=tk.TRUE, height=tk.TRUE)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            self.frame_dsk = Frame(self.master,width=screen_width,height=screen_height)
            self.frame_dsk.place(x=0,y=0)
            self.foto=Image.open("AssistSearch/" + payload['Image'][0])
            self.foto=self.foto.resize((screen_width,screen_height))
            self.photoo=ImageTk.PhotoImage(self.foto)
            label_background = Label(self.frame_dsk, image=self.photoo)
            label_background.place(x=0, y=0)
            label_background.photo=self.photoo

            Nama_Nabila = tk.Label(self.frame_dsk, bg="white",text="Nama            : " + payload['Nama'][0],fg="black", font=("Britannic Bold",13), height=1)
            Nama_Nabila.place(x=600, y=210)

            Nabila_usia = tk.Label(self.frame_dsk, bg="white", text="Usia              : " + str(payload['Usia'][0]), fg="black", font=("Britannic Bold",13), height=1)
            Nabila_usia.place(x=600, y=240)

            Nabila_agama = tk.Label(self.frame_dsk, bg="white", text="Agama          : " + payload['Agama'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_agama.place(x=600, y=270)

            Nabila_status = tk.Label(self.frame_dsk, bg="white", text="Status           : " + payload['Status'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_status.place(x=600, y=300)

            Nabila_asal_kota = tk.Label(self.frame_dsk, bg="white", text="Asal kota       : " + payload["Asal"][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_asal_kota.place(x=600, y=330)

            Nabila_sebagai = tk.Label(self.frame_dsk, bg='white', text="Sebagai         : " + payload['Sebagai'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_sebagai.place(x=600, y=360)

            Nabila_pengalaman = tk.Label(self.frame_dsk, bg="white", text="Pengalaman  : " + payload['Pengalaman'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_pengalaman.place(x=600, y=390)

            Nabila_keterampilan = tk.Label(self.frame_dsk, bg="white", text="Keterampilan : " + payload['Keterampilan1'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan.place(x=600, y=420)

            Nabila_keterampilan2 = tk.Label(self.frame_dsk, bg="white", text=payload['Keterampilan2'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan2.place(x=710, y=450)

            Nabila_keterampilan3 = tk.Label(self.frame_dsk, bg="white", text=payload['Keterampilan3'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan3.place(x=710, y=480)

            Nabila_rating = tk.Label(self.frame_dsk, bg="#4767A5", text="⭐" * payload['Rating'][0], fg="gold", font=("Britannic Bold",16))
            Nabila_rating.place(x=530, y=586)

            Nabila_gaji = tk.Label(self.frame_dsk, bg="#4767A5", text=payload['Gaji'][0], fg="black", font=("Britannic Bold",16))
            Nabila_gaji.place(x=780, y=586)

            exit_button = tk.Button(self.frame_dsk, bg="#4767A5", text="Exit", fg="black", font=("Britannic Bold", 14), height=1, command=self.search_art)
            exit_button.place(x=390, y=580)

            pesan_button = tk.Button(self.frame_dsk, bg="#4767A5", text="Pesan", fg="black", font=("Britannic Bold", 14), height=1, width=10, command=lambda: self.add_calendar_art(payload))
            pesan_button.place(x=1050, y=580)

            
    def add_calendar_art(self, payload):
        # Hapus frame saat ini jika sudah ada
        if hasattr(self, 'frame_calendar_art'):
            self.frame_calendar_art.destroy()

        # Buat frame baru untuk kalender dan informasi pelanggan
        self.frame_calendar_art = Frame(self.frame_dsk, bg='#4767A5')
        self.frame_calendar_art.place(x=0, y=0, relwidth=1, relheight=1)  # Memenuhi seluruh area frame

        # Tambahkan gambar latar belakang
        self.foto = Image.open("AssistSearch/48.png")
        self.foto = self.foto.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.photoo = ImageTk.PhotoImage(self.foto)
        label_background = Label(self.frame_calendar_art, image=self.photoo)
        label_background.place(x=0, y=0, relwidth=1, relheight=1)
        label_background.photo = self.photoo  # Jaga agar gambar terjaga saat ditampilkan

        self.calendar_art = DateEntry(self.frame_dsk,width=22,font=("Times New Roman",15), selectmode='day')
        self.calendar_art.place(x=870, y=410)

        self.label_nama_art = Label(self.frame_dsk, text="Nama Pelanggan", font="Helvetica", bg='white')
        self.label_nama_art.place(x=655, y=290)

        self.entry_nama_art = Entry(self.frame_dsk , width=40)
        self.entry_nama_art.place(x=870, y=290)

        self.label_alamat_art = Label(self.frame_dsk, text="Alamat", font="Helvetica", bg='white')
        self.label_alamat_art.place(x=655, y=330)

        self.entry_alamat_art = Entry(self.frame_dsk , width=40)
        self.entry_alamat_art.place(x=870, y=330)

        self.label_nomor_art = Label(self.frame_dsk, text="Nomor HP", font="Helvetica", bg='white')
        self.label_nomor_art.place(x=655, y=370)

        self.entry_nomor_art = Entry(self.frame_dsk , width=40)
        self.entry_nomor_art.place(x=870, y=370)

        self.label_tanggal_art = Label(self.frame_dsk, text="Tanggal (MM/DD/YY)", font="Helvetica", bg='white')
        self.label_tanggal_art.place(x=655, y=410)

        self.btn_bayar_art = tk.Button(self.frame_dsk, text="Bayar",  bg="#4767A5", fg="black", font=("Britannic Bold", 12), height=1, width= 12, command=lambda: self.payment_art(payload))
        self.btn_bayar_art.place(x=950, y=600)

        # Tombol Exit
        exit_button = tk.Button(self.frame_dsk, bg="#4767A5", text="Exit", fg="black", font=("Britannic Bold", 12), height=1, width= 12, command=self.halaman_dekstop)
        exit_button.place(x=700, y=600)

    
 
    def babysitter_detail(self, payload):

        if self.frame_bawah.destroy():
            window_babbysitter_isabella = tk.Toplevel(self.root)
            window_babbysitter_isabella.title("Desktop")
        else:
            self.master.resizable(width=tk.TRUE, height=tk.TRUE)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            self.frame_dsk = Frame(self.master,width=screen_width,height=screen_height)
            self.frame_dsk.place(x=0,y=0)
            self.foto=Image.open("AssistSearch/" + payload['Image'][0])
            self.foto=self.foto.resize((screen_width,screen_height))
            self.photoo=ImageTk.PhotoImage(self.foto)
            label_background = Label(self.frame_dsk, image=self.photoo)
            label_background.place(x=0, y=0)
            label_background.photo=self.photoo

            Nama_Nabila = tk.Label(self.frame_dsk, bg="white",text="Nama            : " + payload['Nama'][0],fg="black", font=("Britannic Bold",13), height=1)
            Nama_Nabila.place(x=600, y=210)

            Nabila_usia = tk.Label(self.frame_dsk, bg="white", text="Usia              : " + str(payload['Usia'][0]), fg="black", font=("Britannic Bold",13), height=1)
            Nabila_usia.place(x=600, y=240)

            Nabila_agama = tk.Label(self.frame_dsk, bg="white", text="Agama          : " + payload['Agama'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_agama.place(x=600, y=270)

            Nabila_status = tk.Label(self.frame_dsk, bg="white", text="Status           : " + payload['Status'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_status.place(x=600, y=300)

            Nabila_asal_kota = tk.Label(self.frame_dsk, bg="white", text="Asal kota       : " + payload["Asal"][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_asal_kota.place(x=600, y=330)

            Nabila_sebagai = tk.Label(self.frame_dsk, bg='white', text="Sebagai         : " + payload['Sebagai'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_sebagai.place(x=600, y=360)

            Nabila_pengalaman = tk.Label(self.frame_dsk, bg="white", text="Pengalaman  : " + payload['Pengalaman'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_pengalaman.place(x=600, y=390)

            Nabila_keterampilan = tk.Label(self.frame_dsk, bg="white", text="Keterampilan : " + payload['Keterampilan1'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan.place(x=600, y=420)

            Nabila_keterampilan2 = tk.Label(self.frame_dsk, bg="white", text=payload['Keterampilan2'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan2.place(x=710, y=450)

            Nabila_keterampilan3 = tk.Label(self.frame_dsk, bg="white", text=payload['Keterampilan3'][0], fg="black", font=("Britannic Bold",13), height=1)
            Nabila_keterampilan3.place(x=710, y=480)

            Nabila_rating = tk.Label(self.frame_dsk, bg="#4767A5", text="⭐" * payload['Rating'][0], fg="gold", font=("Britannic Bold",16))
            Nabila_rating.place(x=530, y=586)

            Nabila_gaji = tk.Label(self.frame_dsk, bg="#4767A5", text=payload['Gaji'][0], fg="black", font=("Britannic Bold",16))
            Nabila_gaji.place(x=780, y=586)

            exit_button = tk.Button(self.frame_dsk, bg="#4767A5", text="Exit", fg="black", font=("Britannic Bold", 14), height=1, command=self.search_babysitter)
            exit_button.place(x=390, y=580)

            pesan_button = tk.Button(self.frame_dsk, bg="#4767A5", text="Pesan", fg="black", font=("Britannic Bold", 14), height=1, width=10, command=lambda: self.add_calendar_art(payload))
            pesan_button.place(x=1050, y=580)

    def data_customer(self):
        if self.frame_bawah.destroy():
            window_art = tk.Toplevel(self.root)
            window_art.title("Desktop")
        else:
            self.master.resizable(width=tk.TRUE, height=tk.TRUE)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            self.frame_dsk = Frame(self.master,width=screen_width,height=screen_height)
            self.frame_dsk.place(x=0,y=0)
            self.foto=Image.open("AssistSearch/48.png")
            self.foto=self.foto.resize((screen_width,screen_height))
            self.photoo=ImageTk.PhotoImage(self.foto)
            label_background = Label(self.frame_dsk, image=self.photoo)
            label_background.place(x=0, y=0)
            label_background.photo=self.photoo

            self.add_calendar_art()

    def show_selected_language_art(self):

        self.radio_button1_art = tk.Radiobutton(self.frame_pay_art, text="Cash", value= "Cash" , variable=self.selected_language ,bg='#4767A5', fg="white", command= self.show_selected_language_art)
        self.radio_button1_art.place(x=840 , y=600)

        self.radio_button2_art = tk.Radiobutton(self.frame_pay_art, text="Q-Ris", value= "Q-Ris" , variable=self.selected_language, bg='#4767A5', fg="white", command= self.show_selected_language_art)
        self.radio_button2_art.place(x=760 , y=600)

    def combo_bayar_art(self):
            # Combobox creation 
        self.combo_bersih_art = tk.StringVar() 
        self.metodechoosen_art = ttk.Combobox(self.frame_art, width = 27,state="readonly", textvariable = self.combo_bersih_art, values=["BNI", "BRI", "BCA", "BTN", "MANDIRI"]) 

        self.metodechoosen_art.place(x=775, y=460)
        self.metodechoosen_art.current()

        pass

    def payment_art(self, payload):
        confirm_payment = messagebox.askyesno("Konfirmasi Pembayaran", "Apakah Anda yakin ingin melakukan pembayaran?")

        if confirm_payment:

            namapelanggan = self.entry_nama_art.get()
            alamatpelanggan = self.entry_alamat_art.get()
            nomorhppelanggan = self.entry_nomor_art.get()
            tanggal = self.calendar_art.get_date()
            print(payload)

            self.payload_customer = { 'namapelanggan': namapelanggan, 'alamatpelanggan': alamatpelanggan, 'nomorhppelanggan': nomorhppelanggan, 'tanggal': tanggal, 'namaart': payload['Nama'][0], 'usiaart': payload['Usia'][0], 'agamaart': payload['Agama'][0], 'asalart': payload['Asal'][0], 'gajiart': payload['Gaji'][0] }

            # Jika konfirmasi diterima, menghancurkan frame yang sudah ada dan membuat yang baru untuk pembayaran
            if hasattr(self, 'frame_dsk') and self.frame_dsk.winfo_exists():
                self.frame_dsk.destroy()

            self.master.resizable(width=tk.TRUE, height=tk.TRUE)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            self.frame_pay_art = tk.Frame(self.master, width=screen_width, height=screen_height)
            self.frame_pay_art.place(x=0, y=0)
            
            # Memuat dan menampilkan background
            self.foto = Image.open("AssistSearch/49.png")
            self.foto = self.foto.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.photoo = ImageTk.PhotoImage(self.foto)
            label_background = tk.Label(self.frame_pay_art, image=self.photoo)
            label_background.place(x=0, y=0)
            label_background.photo = self.photoo

            # Radio Button untuk metode pembayaran
            self.payment_var = tk.IntVar(value=1)  # Set nilai awal untuk "Transfer"

            rb_transfer = tk.Radiobutton(self.frame_pay_art, text="Transfer", variable=self.payment_var, value=1,
                                        bg="#4767A5", command=self.show_bank_combobox)
            rb_transfer.place(x=400, y=300, width=120, height=35)

            rb_qris = tk.Radiobutton(self.frame_pay_art, text="Qris", variable=self.payment_var, value=2, bg="#4767A5",
                                    command=self.hide_bank_combobox)
            rb_qris.place(x=1050, y=500, width=100, height=35)

            self.bank_combobox = ttk.Combobox(self.frame_pay_art, values=["BRI", "BNI", "BCA"], state='readonly')
            self.bank_combobox.place(x=400, y=350, width=120, height=35)
            self.bank_combobox.bind("<<ComboboxSelected>>", self.show_bank_va)
            self.bank_combobox.place_forget()  # Initially hidden

            self.label_va_number = tk.Label(self.frame_pay_art, text="Pilih Bank", font=("Helvetica", 14), bg="#4767A5", fg="white")
            self.label_va_number.place(x=400, y=400, width=200, height=35)
            self.label_va_number.place_forget()  # Initially hidden


            self.btn_konfirmasi_art = tk.Button(self.frame_pay_art, text="Konfirmasi", bg="#4767A5", fg="black", font=("Britannic Bold", 12), command=self.konfirmasi_pesanan_art)
            self.btn_konfirmasi_art.place(x=630, y=600, width=140, height=40)

            self.btn_exit = tk.Button(self.frame_pay_art, text="Exit", command=self.add_calendar_art, bg='#4767A5', width=9, height=1, font=("Britannic Bold", 10))
            self.btn_exit.place(x=300, y=30)

        else:
            print("Pembayaran dibatalkan")

    def show_bank_combobox(self):
        self.bank_combobox.place(x=400, y=350, width=120, height=35)
        self.label_va_number.place_forget()

    def hide_bank_combobox(self):
        self.bank_combobox.place_forget()
        self.label_va_number.place_forget()

    def show_bank_va(self, event):
        selected_bank = self.bank_combobox.get()
        va_numbers = {
            "BRI": "1234567890",
            "BNI": "0987654321",
            "BCA": "1122334455"
        }
        va_number = va_numbers.get(selected_bank, "")
        self.label_va_number.config(text=f"VA: {va_number}")
        self.label_va_number.place(x=400, y=400, width=200, height=35)

    def konfirmasi_pesanan_art(self):
        self.window_konfirmasi = tk.Toplevel(self.master)
        self.window_konfirmasi.title("Konfirmasi Pesanan")
        self.window_konfirmasi.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")

        self.window_konfirmasi.configure(bg='white')

        # Muat gambar untuk judul
        image_path = "AssistSearch/art_konfirmasi.png"
        photo_image = Image.open(image_path)
        photo_image = photo_image.resize((self.master.winfo_screenwidth(), 100))
        photo_judul = ImageTk.PhotoImage(photo_image)
        
        # Tampilkan gambar sebagai judul
        judul_label = tk.Label(self.window_konfirmasi, image=photo_judul)
        judul_label.image = photo_judul  # simpan referensi agar tidak dihapus oleh pengumpul sampah
        judul_label.pack(pady=20)

        with open('data_customer.csv', 'a', ) as file:
            fieldnames = ['Nama','Tanggal','Alamat','Nomor HP','Nama ART','Usia','Agama','Asal Kota','Gaji'];
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writerow({'Nama': self.payload_customer['namapelanggan'], 'Tanggal': self.payload_customer['tanggal'], 'Alamat': self.payload_customer['alamatpelanggan'], 'Nomor HP': self.payload_customer['nomorhppelanggan'], 'Nama ART': self.payload_customer['namaart'], 'Usia': self.payload_customer['usiaart'], 'Agama': self.payload_customer['agamaart'], 'Asal Kota': self.payload_customer['asalart'], 'Gaji': self.payload_customer['gajiart']})

            

        # Setup tabel
        self.table = ttk.Treeview(self.window_konfirmasi, columns=("Nama", "Tanggal", "Alamat", "Nomor HP", "Nama ART", "Usia", "Agama", "Asal Kota", "Gaji"), show="headings")
        for col in ["Nama", "Tanggal", "Alamat", "Nomor HP", "Nama ART", "Usia", "Agama", "Asal Kota", "Gaji"]:
            self.table.heading(col, text=col)
        self.table.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Fungsi untuk memuat data dari CSV
        self.load_data_from_csv()

        # Tombol 'Selesai' untuk menutup jendela konfirmasi
        tk.Button(self.window_konfirmasi, text="Selesai", command=self.close_and_return_home, bg='white', fg='black', font=("Helvetica", 12)).pack(pady=20)


    def konfirmasi_pesanan_babysitter(self):
        # Membuat jendela konfirmasi baru
        self.window_konfirmasi = tk.Toplevel(self.master)
        self.window_konfirmasi.title("Konfirmasi Pesanan")
        self.window_konfirmasi.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")

        # Latar belakang putih untuk jendela konfirmasi
        self.window_konfirmasi.configure(bg='white')

        # Judul halaman konfirmasi
        # Judul halaman konfirmasi dengan background putih
        tk.Label(self.window_konfirmasi, text="ASISTEN RUMAH TANGGA KONFIRMASI PESANAN", font=("Helvetica", 16, "bold"), bg="black").pack(pady=20)
        tk.Label(self.window_konfirmasi, text="KONFIRMASI PESANAN", font=("Helvetica", 14), bg="black").pack(pady=10)
            

        # Membuat dan mengatur tabel untuk menampilkan data
        self.table = ttk.Treeview(self.window_konfirmasi, columns=("Nama", "Tanggal", "Alamat", "Nomor HP", "Nama ART", "Usia", "Agama", "Asal Kota", "Gaji"), show="headings")
        for col in ["Nama", "Tanggal", "Alamat", "Nomor HP", "Nama ART", "Usia", "Agama", "Asal Kota", "Gaji"]:
            self.table.heading(col, text=col)
        self.table.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Memuat data dari CSV dan menambahkannya ke tabel
        self.load_data_from_csv()

        # Tombol 'Selesai' untuk menutup jendela konfirmasi
        tk.Button(self.window_konfirmasi, text="Selesai", command=self.close_and_return_home, bg='white', fg='black', font=("Helvetica", 12)).pack(pady=20)
        
    def close_and_return_home(self):
        # Menutup jendela konfirmasi
        self.window_konfirmasi.destroy()
        # Memanggil halaman utama
        self.halaman_dekstop()

    def load_data_from_csv(self):
        import csv
        try:
            with open('data_customer.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.table.insert("", "end", values=(row["Nama"], row["Tanggal"], row["Alamat"], row["Nomor HP"],
                                                        row["Nama ART"], row["Usia"], row["Agama"], row["Asal Kota"], row["Gaji"]))
        except FileNotFoundError:
            print("File not found. Please ensure the 'data_customer.csv' file exists.")


    def close_confirmation_page(self):
        if hasattr(self, 'frame_konfirmasi') and self.frame_konfirmasi.winfo_exists():
            self.frame_konfirmasi.destroy()


root = tk.Tk()
app = AssistSearch(root)
root.mainloop()