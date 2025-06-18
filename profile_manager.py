# profile_manager.py

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) 
PROFILES_FILE = os.path.join(script_dir, "profiles.json") 

def get_default_profiles():
    """Mengembalikan dictionary profil default jika file tidak ditemukan."""
    return {
        "Tidak Ada": None,
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

def load_profiles():
    """Memuat profil dari file JSON. Jika file tidak ada, buat dengan data default."""
    if not os.path.exists(PROFILES_FILE):
        print(f"File '{PROFILES_FILE}' tidak ditemukan. Membuat file baru dengan data default.")
        default_profiles = get_default_profiles()
        save_profiles(default_profiles)
        return default_profiles
    
    try:
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error membaca '{PROFILES_FILE}'. Menggunakan data default.")
        return get_default_profiles()

def save_profiles(profiles):
    """Menyimpan dictionary profil ke dalam file JSON."""
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)
    print(f"Perubahan berhasil disimpan ke '{PROFILES_FILE}'.")