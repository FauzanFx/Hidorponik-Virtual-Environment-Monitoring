# environment.py

import random
class HydroponicEnvironment:
    """
    Mensimulasikan lingkungan hidroponik.
    Perubahan nilai dibuat agar terasa natural (berubah perlahan).
    """
    def __init__(self):
        self.ph = 7.0
        self.temperature = 25.0
        self.humidity = 60.0
        self.light_intensity = 0  # 0: mati, >0: hidup
        self.water_level = 100.0
        # Status kontrol internal lingkungan
        self._is_light_on = False
        self._is_fan_on = False
        self._is_refilling = False

    def update(self):
        """Panggil metode ini secara berkala untuk mensimulasikan perubahan waktu."""
        # Simulasi perubahan pH
        self.ph += random.uniform(-0.01, 0.01)
        self.ph = max(5.0, min(8.0, self.ph)) # Jaga pH dalam rentang wajar

        # Simulasi perubahan suhu dan kelembapan
        if self._is_fan_on:
            self.temperature -= random.uniform(0.05, 0.1) # Kipas mendinginkan
            self.humidity -= random.uniform(0.1, 0.2)
        else:
            self.temperature += random.uniform(-0.05, 0.05) # Suhu naik perlahan
            self.humidity += random.uniform(0.05, 0.1)

        self.temperature = max(18.0, min(35.0, self.temperature))
        self.humidity = max(40.0, min(90.0, self.humidity))

        # Simulasi intensitas cahaya
        if self._is_light_on:
            self.light_intensity = random.randint(800, 1200) # Satuan lux (contoh)
            self.temperature += random.uniform(0.01, 0.05)
        else:
            self.light_intensity = 0

        # Simulasi tingkat Air
        if self._is_refilling:
            # Jika "mode mengisi" aktif, tambah level air
            self.water_level += 5  # Tambah 5% setiap detik, bisa diubah
            if self.water_level >= 100:
                self.water_level = 100.0
                self._is_refilling = False
        else:
            self.water_level -= random.uniform(0.01, 0.2)
            self.water_level = max(0, self.water_level)

    def get_sensor_data(self):
        """Mengembalikan data sensor saat ini dalam bentuk dictionary."""
        return {
            "ph": self.ph,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "light": self.light_intensity,
            "water_level": self.water_level,
            "is_refilling": self._is_refilling
        }

    # --- Metode Kontrol Lingkungan ---
    def adjust_ph(self, amount):
        """Menyesuaikan pH (simulasi penambahan larutan pH up/down)."""
        self.ph += amount
        self.ph = max(5.0, min(8.0, self.ph))

    def set_light(self, status: bool):
        """Menyalakan atau mematikan lampu."""
        self._is_light_on = status

    def set_fan(self, status: bool):
        """Menyalakan atau mematikan kipas/ventilasi."""
        self._is_fan_on = status

    def adjust_water_level(self, amount):
        """Menyesuaikan tingkat Air (simulasi penambahan Air)"""
        self.water_level += amount
        self.water_level = max(0.0, min(100.0, self.water_level))

    def refill_water(self):
        if not self._is_refilling:
            self._is_refilling = True