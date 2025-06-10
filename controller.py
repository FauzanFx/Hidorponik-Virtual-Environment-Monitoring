# controller.py - PERBAIKAN UNTUK ERROR 'water_ok' DAN TOMBOL OTOMATISASI
from datetime import datetime

class Controller:
    """Menghubungkan Model, View, dan Lingkungan."""
    def __init__(self, model, view, environment):
        self.model = model
        self.view = view
        self.environment = environment
        self.plant_profiles = self._load_plant_profiles()

    def _load_plant_profiles(self):
        """Memuat profil tanaman secara langsung dari dictionary (hardcoded)."""
        print("INFO: Memuat profil tanaman dari source code (hardcoded)...")
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

    def _run_automation_and_notifications(self):
        """Logika utama untuk cek sensor, notifikasi, dan kontrol otomatis."""
        if not self.model.automation_enabled:
            self.model.set_notification("Otomatisasi nonaktif. Kontrol manual diperlukan.")
            return
        if self.model.water_level <= 20 and not self.model.is_refilling:
            self.environment.refill_water()
        
        profile = self.model.active_profile_data
        if not profile:
            self.model.set_notification("Pilih profil tanaman untuk memulai otomatisasi.")
            return

        # --- PERBAIKAN 1: Mendefinisikan 'water_ok' ---
        ph_ok = profile["ph_min"] <= self.model.ph <= profile["ph_max"]
        temp_ok = profile["temp_min"] <= self.model.temperature <= profile["temp_max"]
        water_ok = self.model.water_level >= 20
        notifications = []
        if not ph_ok:
            notifications.append(f"PERINGATAN: pH di luar rentang ({self.model.ph:.2f})!")
        if not temp_ok:
            notifications.append(f"PERINGATAN: Suhu di luar rentang ({self.model.temperature:.1f}°C)!")
        # Menambahkan notifikasi untuk level air
        if not water_ok:
            notifications.append(f"PERINGATAN: Level air rendah ({self.model.water_level:.1f}%)!")

        if notifications:
            self.model.set_notification(" | ".join(notifications))
        else:
            self.model.set_notification("Semua sistem berjalan normal dalam rentang ideal.")

        # --- Otomatisasi pH ---
        if not ph_ok:
            if self.model.ph < profile["ph_min"]:
                self.environment.adjust_ph(0.1)
                print("AUTO: pH terlalu rendah! Menambahkan larutan pH Up...")
            elif self.model.ph > profile["ph_max"]:
                self.environment.adjust_ph(-0.1)
                print("AUTO: pH terlalu tinggi! Menambahkan larutan pH Down...")
        
        # --- Otomatisasi Suhu (Kipas) ---
        if self.model.temperature > profile["temp_max"]:
            if not self.model.fan_on: self.toggle_fan()
        elif self.model.temperature < profile["temp_min"] + 1:
             if self.model.fan_on: self.toggle_fan()
        
        # --- Otomatisasi Cahaya (Lampu) ---
        current_hour = datetime.now().hour
        is_light_time = profile["auto_light_on_hour"] <= current_hour < profile["auto_light_off_hour"]
        
        if is_light_time and not self.model.light_on:
            self.toggle_light()
        elif not is_light_time and self.model.light_on:
            self.toggle_light()

    def update_loop(self):
        """Loop utama untuk memperbarui data dan UI secara berkala."""
        self.environment.update()
        sensor_data = self.environment.get_sensor_data()
        self.model.update_sensor_data(sensor_data)
        
        # Panggil logika otomatisasi. Tampilan akan diupdate di akhir loop
        self._run_automation_and_notifications()
        
        # Perintahkan view untuk update semua elemen visual
        self.view.update_dashboard(self.model)

        # Jadwalkan pembaruan berikutnya
        self.view.parent.after(1000, self.update_loop)

    # ... (fungsi toggle_automation, change_plant_profile, get_profile_names, adjust_ph tidak berubah)
    def toggle_automation(self):
        status = self.model.toggle_automation()
        print(f"Sinyal Otomatisasi: {'ON' if status else 'OFF'}")

    def change_plant_profile(self, profile_name):
        profile_data = self.plant_profiles.get(profile_name)
        self.model.load_profile(profile_name, profile_data)
        
    def get_profile_names(self):
        return list(self.plant_profiles.keys())
        
    def adjust_ph(self, amount):
        self.environment.adjust_ph(amount)
        print(f"Sinyal Penyesuaian pH: {amount}")
        
    def adjust_water_level(self, amount):
        self.environment.adjust_water_level(amount)
        print(f"Sinyal Penyesuaian Level Air: {amount}%")

    # --- PERBAIKAN 2: Memaksa Update Tampilan Tombol ---
    def toggle_light(self):
        status = self.model.toggle_light()
        self.environment.set_light(status)
        print(f"Sinyal Lampu: {'ON' if status else 'OFF'}")
        # Segarkan tampilan tombol secara langsung
        if self.view:
            self.view.update_buttons(self.model)

    def toggle_fan(self):
        status = self.model.toggle_fan()
        self.environment.set_fan(status)
        print(f"Sinyal Kipas: {'ON' if status else 'OFF'}")
        # Segarkan tampilan tombol secara langsung
        if self.view:
            self.view.update_buttons(self.model)