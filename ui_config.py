# ui_config.py

# --- Definisi Variabel Warna ---
SUCCESS_COLOR = "#7fb65e"
WARNING_COLOR = "#fbb142"
DANGER_COLOR = "#EA6948"
OFF_COLOR = "#B0B0B0"
WATER_COLOR = "#1cb2b4"

# --- STYLE SHEET UTAMA (QSS) ---
STYLE_SHEET = """
    QWidget {
        background-color: #F5F5F5;
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 13px;
    }
    QGroupBox {
        font-size: 15px;
        font-weight: bold;
        color: #655f3e;
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        left: 10px;
    }
    QLabel {
        color: #655f3e;
        padding: 2px;
    }
    QLabel[status="normal"] {
        color: #655f3e;
    }
    QLabel[status="success"] {
        color: #2bf728;
        font-weight: bold;
        border: 1px solid #45ff54;
        border-radius: 4px;
        background-color: #e7feec;
        padding: 5px;
    }
    QLabel[status="warning"] {
        color: #fbb142;
        font-weight: bold;
        border: 1px solid #f8bd56;
        border-radius: 4px;
        background-color: #fef5e7;
        padding: 5px;
    }
    QLabel[status="warning2"] {
        color: #ff3512;
        font-weight: bold;
        border: 1px solid #ff3300;
        border-radius: 4px;
        background-color: #fee7e7; 
        padding: 5px;
    }
    QComboBox {
        color: #655f3e;
        border: 1px solid #D0D0D0;
        padding: 5px;
        border-radius: 3px;
        background-color: white;
    }
    QComboBox QAbstractItemView {
        color: #655f3e;
        background-color: white;
        border: 1px solid #D0D0D0;
        selection-background-color: #1cb2b4;
        outline: 0px; 
    }
    QPushButton[status="on"] {
        background-color: #1cb2b4;
        color: white;
        font-weight: bold;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton[status="on"]:hover {
        background-color: #189a9c;
    }
    QPushButton[status="off"] {
        background-color: #E0E0E0;
        color: #6c757d;
        font-weight: normal;
        border: 1px solid #D0D0D0;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton[status="off"]:hover {
        background-color: #D3D3D3;
    }
    QPushButton {
        background-color: #7fb65e;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #6f9a54;
    }
    QDialog#ProfileDialog QLineEdit,
QDialog#ProfileDialog QDoubleSpinBox,
QDialog#ProfileDialog QSpinBox {
    color: #655f3e; /* Warna teks HANYA untuk input di dalam ProfileDialog */
    background-color: #FFFFFF;
    border: 1px solid #D0D0D0;
    padding: 5px;
    border-radius: 3px;
}

QDialog#ProfileDialog QLineEdit:focus,
QDialog#ProfileDialog QDoubleSpinBox:focus,
QDialog#ProfileDialog QSpinBox:focus {
    border: 1px solid #1cb2b4; /* Highlight saat aktif */
}

QDialog#ProfileDialog QLineEdit:read-only {
    background-color: #F0F0F0; 
    color: #777777;
}

"""