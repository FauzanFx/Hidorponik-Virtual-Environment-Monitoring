# controller.py

from datetime import datetime
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
import profile_manager
from profile_dialog import ProfileDialog


class Controller:
    # Inisialisasi Controller
    def __init__(self, model, environment):
        self.model = model
        self.view = None
        self.environment = environment
        self.plant_profiles = profile_manager.load_profiles()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_loop)
    
     # Fungsi untuk memeriksa apakah nilai input user berada dalam rentang
    def range_check(self, ph_min, ph_max, temp_min, temp_max):
        if ph_min > ph_max or temp_min > temp_max:
            return False,  "Data yang dimasukkan harus sesuai!"
        if ph_max > 8 or ph_min < 5:
            return False, "pH aman hanya dari rentang 5-8"
        if temp_max > 35 or temp_min < 18:
            return False,"Suhu aman hanya dari rentang 18-35"
        return True, None
        
    def add_profile(self):
        dialog = ProfileDialog(self.view)
        if dialog.exec(): # Menampilkan dialog dan menunggu hasil
            new_data = dialog.get_profile_data()
            profile_name = new_data["name"]
            if profile_name and profile_name not in self.plant_profiles:
                self.plant_profiles[profile_name] = new_data
                valid, error_massage = self.range_check(new_data["ph_min"],new_data["ph_max"],new_data["temp_min"],new_data["temp_max"])
                if not valid:
                    return QMessageBox.warning(self.view, "Error", error_massage)
                profile_manager.save_profiles(self.plant_profiles)
                self.view.refresh_profile_dropdown() # Perbarui dropdown di view
                print("Profil berhasil ditambahkan")
            else:
                QMessageBox.warning(self.view, "Error", "Nama profil tidak boleh kosong atau sudah ada!")
            

    def edit_profile(self):
        current_profile_name = self.model.active_profile_name
        if current_profile_name is None or current_profile_name == "Tidak Ada":
            QMessageBox.information(self.view, "Info", "Pilih profil yang valid untuk diedit.")
            return
        
        current_data = self.plant_profiles[current_profile_name]
        dialog = ProfileDialog(self.view, profile_data=current_data)
        
        if dialog.exec():
            updated_data = dialog.get_profile_data()
            valid, error_massage = self.range_check(updated_data["ph_min"],updated_data["ph_max"],updated_data["temp_min"],updated_data["temp_max"])
            if not valid:
                return QMessageBox.warning(self.view, "Error", error_massage)
            self.plant_profiles[current_profile_name] = updated_data
            profile_manager.save_profiles(self.plant_profiles)
            self.change_plant_profile(current_profile_name)
            print("Profil berhasil diedit")

    def delete_profile(self):
        current_profile_name = self.model.active_profile_name
        if current_profile_name is None or current_profile_name == "Tidak Ada":
            QMessageBox.information(self.view, "Info", "Pilih profil yang valid untuk dihapus.")
            return

        reply = QMessageBox.question(self.view, "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus profil '{current_profile_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            del self.plant_profiles[current_profile_name]
            print("Profil berhasil dihapus")
            profile_manager.save_profiles(self.plant_profiles)
            self.view.refresh_profile_dropdown()
            # Set ke profil "Tidak Ada"
            self.view.profile_dropdown.setCurrentText("Tidak Ada")
            self.model.active_profile_name = None
    # Memulai Timer Loop
    def start_update_loop(self):
        self.timer.start()
    
    # Loop Pembaruan Utama (dipanggil oleh Timer)
    def update_loop(self):
        self.environment.update()
        sensor_data = self.environment.get_sensor_data()
        self.model.update_sensor_data(sensor_data)
        
        self._run_automation_and_notifications()
        
        if self.view:
            self.view.update_dashboard(self.model)

    # Memuat Profil Tanaman (Hardcoded)
    def _load_plant_profiles(self):
        hardcoded_profiles = {
            "Selada": {
                "name": "Selada", "ph_min": 5.8, "ph_max": 6.5, "temp_min": 20.0, "temp_max": 25.0,
                "auto_light_on_hour": 6, "auto_light_off_hour": 22
            },
            "Tomat": {
                "name": "Tomat", "ph_min": 6.0, "ph_max": 6.8, "temp_min": 22.0, "temp_max": 28.0,
                "auto_light_on_hour": 5, "auto_light_off_hour": 21
            },
            "Cabai": {
                "name": "Cabai", "ph_min": 5.5, "ph_max": 6.5, "temp_min": 23.0, "temp_max": 30.0,
                "auto_light_on_hour": 6, "auto_light_off_hour": 22
            }
        }
        hardcoded_profiles["Tidak Ada"] = None
        return hardcoded_profiles

    # Logika Otomatisasi dan Notifikasi
    def _run_automation_and_notifications(self):
        profile = self.model.active_profile_data
        if not profile:
            self.model.set_notification("HINT: Pilih profil tanaman untuk memulai otomatisasi.")
            return

        if not self.model.automation_enabled:
            self.model.set_notification("HINT: Otomatisasi nonaktif. Kontrol manual diperlukan.")
            return
        
        if self.model.water_level <= 20 and not self.model.is_refilling:
            self.environment.refill_water()
        
        
        ph_ok = profile["ph_min"] <= self.model.ph <= profile["ph_max"]
        temp_ok = profile["temp_min"] <= self.model.temperature <= profile["temp_max"]
        water_ok = self.model.water_level >= 20
        notifications = []

        if not ph_ok:
            notifications.append(f"PERINGATAN: pH di luar rentang ({self.model.ph:.2f})!")
        if not temp_ok:
            notifications.append(f"PERINGATAN: Suhu di luar rentang ({self.model.temperature:.1f}°C)!")
        if not water_ok:
            notifications.append(f"PERINGATAN: Level air rendah ({self.model.water_level:.1f}%)!")

        if notifications:
            self.model.set_notification(" | ".join(notifications))
        else:
            self.model.set_notification("Semua sistem berjalan normal dalam rentang ideal.")

        if not ph_ok:
            if self.model.ph < profile["ph_min"]:
                self.environment.adjust_ph(0.1)
            elif self.model.ph > profile["ph_max"]:
                self.environment.adjust_ph(-0.1)
        
        if self.model.temperature > profile["temp_max"]:
            if not self.model.fan_on: self.toggle_fan()
        elif self.model.temperature < profile["temp_min"] + 1:
            if self.model.fan_on: self.toggle_fan()
        
        current_hour = datetime.now().hour
        is_light_time = profile["auto_light_on_hour"] <= current_hour < profile["auto_light_off_hour"]
        
        if is_light_time and not self.model.light_on or self.model.temperature < profile["temp_min"] + 1 and not self.model.light_on:
            self.toggle_light()
        elif not is_light_time and self.model.light_on and not self.model.temperature < profile["temp_min"] + 1:
            self.toggle_light()

    # Aksi: Mengubah Status Otomatisasi
    def toggle_automation(self):
        self.model.toggle_automation()

    # Aksi: Mengganti Profil Tanaman
    def change_plant_profile(self, profile_name):
        profile_data = self.plant_profiles.get(profile_name)
        self.model.load_profile(profile_name, profile_data)
        
    # Mengambil Daftar Nama Profil
    def get_profile_names(self):
        return list(self.plant_profiles.keys())
        
    # Aksi: Mengubah Status Lampu
    def toggle_light(self):
        status = self.model.toggle_light()
        self.environment.set_light(status)

    # Aksi: Mengubah Status Kipas
    def toggle_fan(self):
        status = self.model.toggle_fan()
        self.environment.set_fan(status)
    
    # Aksi Manual: Menyesuaikan pH
    def adjust_ph(self, amount):
        print(f"Sinyal Manual Penyesuaian pH: {amount}")
        self.environment.adjust_ph(amount)
        
        sensor_data = self.environment.get_sensor_data()
        self.model.update_sensor_data(sensor_data)
        if self.view:
            self.view.update_dashboard(self.model)

    # Aksi Manual: Menyesuaikan Level Air
    def adjust_water_level(self, amount):
        print(f"Sinyal Manual Penyesuaian Level Air: {amount}%")
        self.environment.adjust_water_level(amount)
        
        sensor_data = self.environment.get_sensor_data()
        self.model.update_sensor_data(sensor_data)
        if self.view:
            self.view.update_dashboard(self.model)