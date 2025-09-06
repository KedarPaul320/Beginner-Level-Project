import qrcode
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image

# Function to generate QR code
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    return img

class StudentQRGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Student QR Code Generator")
        self.setGeometry(100, 100, 400, 500)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create form layout for input fields
        form_layout = QGridLayout()
        
        # Create labels and input fields
        self.name_label = QLabel("Name:")
        self.id_label = QLabel("Student ID:")
        self.department_label = QLabel("Department:")
        self.email_label = QLabel("Email:")
        
        self.name_entry = QLineEdit()
        self.id_entry = QLineEdit()
        self.department_entry = QLineEdit()
        self.email_entry = QLineEdit()
        
        # Add to form layout
        form_layout.addWidget(self.name_label, 0, 0)
        form_layout.addWidget(self.name_entry, 0, 1)
        form_layout.addWidget(self.id_label, 1, 0)
        form_layout.addWidget(self.id_entry, 1, 1)
        form_layout.addWidget(self.department_label, 2, 0)
        form_layout.addWidget(self.department_entry, 2, 1)
        form_layout.addWidget(self.email_label, 3, 0)
        form_layout.addWidget(self.email_entry, 3, 1)
        
        # Create button
        self.generate_button = QPushButton("Generate QR Code")
        self.generate_button.clicked.connect(self.create_student_qr_code)
        
        # Create QR code display label
        self.qr_label = QLabel()
        self.qr_label.setMinimumSize(200, 200)
        self.qr_label.setStyleSheet("border: 1px solid black;")
        
        # Add widgets to main layout
        layout.addLayout(form_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.qr_label)
    
    def create_student_qr_code(self):
        name = self.name_entry.text()
        student_id = self.id_entry.text()
        department = self.department_entry.text()
        email = self.email_entry.text()

        if not name or not student_id or not department or not email:
            QMessageBox.critical(self, "Error", "All fields are required!")
            return

        student_details = {
            'name': name,
            'id': student_id,
            'department': department,
            'email': email
        }

        data = f"Name: {student_details['name']}\n" \
               f"ID: {student_details['id']}\n" \
               f"Department: {student_details['department']}\n" \
               f"Email: {student_details['email']}"

        filename = f"{student_details['id']}_qrcode.png"
        img = generate_qr_code(data, filename)
        
        self.display_qr_code(img)

    def display_qr_code(self, img):
        img = img.resize((300, 300))  # Resize if needed
        
        # Convert PIL Image to QPixmap
        img_rgb = img.convert('RGB')
        width, height = img_rgb.size
        img_bytes = img_rgb.tobytes('raw', 'RGB')
        
        from PyQt5.QtGui import QImage
        qimage = QImage(img_bytes, width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        
        self.qr_label.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = StudentQRGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
