# environment.py

import random

class HydroponicEnvironment:
    # Inisialisasi Lingkungan
    def __init__(self):
        self.ph = 7.0
        self.temperature = 25.0
        self.humidity = 60.0
        self.light_intensity = 0
        self.water_level = 100.0
        self._is_light_on = False
        self._is_fan_on = False
        self._is_refilling = False

    # Simulasi Perubahan Lingkungan Berkala
    def update(self):
        self.ph += random.uniform(-0.01, 0.01)
        self.ph = max(5.0, min(8.0, self.ph))

        if self._is_fan_on:
            self.temperature -= random.uniform(0.05, 0.1)
            self.humidity -= random.uniform(0.1, 0.2)
        else:
            self.temperature += random.uniform(-0.01, 0.05)
            self.humidity += random.uniform(0.05, 0.1)
        self.temperature = max(18.0, min(35.0, self.temperature))
        self.humidity = max(40.0, min(90.0, self.humidity))

        if self._is_light_on:
            self.light_intensity = random.randint(800, 1200)
            self.temperature += random.uniform(0.01, 0.05)
        else:
            self.light_intensity = 0

        if self._is_refilling:
            self.water_level += 5
            if self.water_level >= 100:
                self.water_level = 100.0
                self._is_refilling = False
        else:
            self.water_level -= random.uniform(0.01, 0.2)
            self.water_level = max(0, self.water_level)

    # Mengambil Data Sensor
    def get_sensor_data(self):
        return {
            "ph": self.ph,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "light": self.light_intensity,
            "water_level": self.water_level,
            "is_refilling": self._is_refilling
        }

    # Kontrol Manual: Menyesuaikan pH
    def adjust_ph(self, amount):
        self.ph += amount
        self.ph = max(5.0, min(8.0, self.ph))

    # Kontrol: Mengatur Lampu
    def set_light(self, status: bool):
        self._is_light_on = status

    # Kontrol: Mengatur Kipas
    def set_fan(self, status: bool):
        self._is_fan_on = status

    # Kontrol Manual: Menyesuaikan Level Air
    def adjust_water_level(self, amount):
        self.water_level += amount
        self.water_level = max(0.0, min(100.0, self.water_level))
        
    # Kontrol Otomatis: Mulai Isi Ulang Air
    def refill_water(self):
        if not self._is_refilling:
            self._is_refilling = True