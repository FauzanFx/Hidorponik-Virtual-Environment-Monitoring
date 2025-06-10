# controller.py - VERSI FINAL YANG SUDAH DIPERBAIKI DAN LENGKAP

from datetime import datetime

class Controller:
    """Menghubungkan Model, View, dan Lingkungan."""
    def __init__(self, model, view, environment):
        self.model = model
        self.view = view
        self.environment = environment
        self.plant_profiles = self._load_plant_profiles()

    def _load_plant_profiles(self):
        """
        Memuat profil tanaman secara langsung dari dictionary (hardcoded).
        Ini adalah metode debugging untuk melewati proses pembacaan file.
        """
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

    # =======================================================================
    # == FUNGSI INI SEKARANG SUDAH LENGKAP DAN BENAR ==
    # =======================================================================
    def _run_automation_and_notifications(self):
        """Logika utama untuk cek sensor, notifikasi, dan kontrol otomatis."""
        # Langkah 0: Periksa apakah otomatisasi aktif. Jika tidak, berhenti di sini.
        if not self.model.automation_enabled:
            self.model.set_notification("Otomatisasi nonaktif. Kontrol manual diperlukan.")
            return

        # Langkah 1: Ambil profil yang aktif dari model
        profile = self.model.active_profile_data
        if not profile:
            self.model.set_notification("Pilih profil tanaman untuk memulai otomatisasi.")
            return

        # Langkah 2: Logika untuk membuat Notifikasi Peringatan
        ph_ok = profile["ph_min"] <= self.model.ph <= profile["ph_max"]
        temp_ok = profile["temp_min"] <= self.model.temperature <= profile["temp_max"]
        water_ok = 20 <= self.model.water_level <= 100

        notifications = []
        if not ph_ok:
            notifications.append(f"PERINGATAN: pH di luar rentang ({self.model.ph:.2f})!")
        if not temp_ok:
            notifications.append(f"PERINGATAN: Suhu di luar rentang ({self.model.temperature:.1f}°C)!")
        if not water_ok:
            notifications.append(f"PERINGATAN: Kandungan air di luar rentang ({self.model.water_level:.1f}%)!")
        if notifications:
            self.model.set_notification(" | ".join(notifications))
        else:
            self.model.set_notification("Semua sistem berjalan normal dalam rentang ideal.")

        if self.model.temperature > profile["temp_max"]:
            if not self.model.fan_on: self.toggle_fan()
        elif self.model.temperature < profile["temp_min"] + 1: # Histeresis
             if self.model.fan_on: self.toggle_fan()
        
        # Kontrol Lampu berdasarkan Jadwal
        current_hour = datetime.now().hour
        is_light_time = profile["auto_light_on_hour"] <= current_hour < profile["auto_light_off_hour"]
        
        if is_light_time and not self.model.light_on:
            self.toggle_light()
        elif not is_light_time and self.model.light_on:
            self.toggle_light()

        if not ph_ok: # Hanya bertindak jika pH di luar rentang
            if self.model.ph < profile["ph_min"]:
                # pH terlalu rendah, perlu dinaikkan
                self.environment.adjust_ph(0.1)
                print("AUTO: pH terlalu rendah! Menambahkan larutan pH Up...")
            elif self.model.ph > profile["ph_max"]:
                # pH terlalu tinggi, perlu diturunkan
                self.environment.adjust_ph(-0.1)
                print("AUTO: pH terlalu tinggi! Menambahkan larutan pH Down...")

        if not water_ok: # Hanya bertindak jika water level di luar rentang
            if self.model.water_level < 20:
                # Air terlalu rendah, perlu dinaikkan
                self.environment.adjust_water(0.1)
                print("AUTO: Air hampir habis! Menambahkan Air Up...")
            elif self.model.water_level == 99:
                # Air terlalu tinggi, perlu diturunkan
                print("AUTO: Air sudah cukup! Menghentikan Air Down...")

    def update_loop(self):
        """Loop utama untuk memperbarui data dan UI secara berkala."""
        self.environment.update()
        sensor_data = self.environment.get_sensor_data()
        self.model.update_sensor_data(sensor_data)
        self._run_automation_and_notifications() # Panggil fungsi yang sudah lengkap
        self.view.update_dashboard(self.model)
        self.view.update_graphs(self.model)
        self.view.parent.after(1000, self.update_loop)

    def toggle_automation(self):
        status = self.model.toggle_automation()
        print(f"Sinyal Otomatisasi: {'ON' if status else 'OFF'}")

    def change_plant_profile(self, profile_name):
        profile_data = self.plant_profiles.get(profile_name)
        self.model.load_profile(profile_name, profile_data)
        
    def get_profile_names(self):
        return list(self.plant_profiles.keys())
        
    def toggle_water_pump(self):
        status = self.model.toggle_water_pump()
        print(f"Sinyal Pompa Air: {'ON' if status else 'OFF'}")

    def toggle_light(self):
        status = self.model.toggle_light()
        self.environment.set_light(status)
        print(f"Sinyal Lampu: {'ON' if status else 'OFF'}")

    def toggle_fan(self):
        status = self.model.toggle_fan()
        self.environment.set_fan(status)
        print(f"Sinyal Kipas: {'ON' if status else 'OFF'}")
    
    def adjust_ph(self, amount):
        self.environment.adjust_ph(amount)
        print(f"Sinyal Penyesuaian pH: {amount}")

    def adjust_water(self, amount):
        self.environment.adjust_water(amount)
        print(f"Sinyal Penyesuaian Air: {amount}")