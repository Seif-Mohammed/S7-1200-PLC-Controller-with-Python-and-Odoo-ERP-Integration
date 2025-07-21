import sys
import snap7
from snap7.type import Areas
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QGroupBox, QGridLayout, 
                           QFrame, QLineEdit, QSpinBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import requests
import json
from threading import Thread
import datetime


class IOIndicator(QFrame):
    def __init__(self, label, io_type="input"):
        super().__init__()
        self.io_type = io_type
        self.state = False
        self.initUI(label)
    
    def initUI(self, label):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        
        layout = QVBoxLayout()
        
        # Label
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(self.label)
        
        # Status indicator
        self.status_label = QLabel("OFF")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.status_label)
        
        # Control buttons only for outputs
        if self.io_type == "output":
            button_layout = QHBoxLayout()
            
            self.on_btn = QPushButton("ON")
            self.on_btn.setStyleSheet("background-color: #90EE90; color: #006400; font-weight: bold;")
            self.on_btn.clicked.connect(lambda: self.set_state_requested(True))
            
            self.off_btn = QPushButton("OFF")
            self.off_btn.setStyleSheet("background-color: #FFB6C1; color: #8B0000; font-weight: bold;")
            self.off_btn.clicked.connect(lambda: self.set_state_requested(False))
            
            self.toggle_btn = QPushButton("TOGGLE")
            self.toggle_btn.setStyleSheet("background-color: #F0E68C; color: #8B8000; font-weight: bold;")
            self.toggle_btn.clicked.connect(lambda: self.toggle_requested())
            
            button_layout.addWidget(self.on_btn)
            button_layout.addWidget(self.off_btn)
            button_layout.addWidget(self.toggle_btn)
            
            layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.update_appearance()
    
    def toggle_requested(self):
        # Connected to main controller for toggle functionality
        pass
    
    def set_state_requested(self, state):
        # Connected to main controller for direct state setting
        pass
    
    def set_state(self, state):
        self.state = state
        self.update_appearance()
    
    def update_appearance(self):
        if self.state:
            self.status_label.setText("ON")
            self.setStyleSheet("background-color: #90EE90; border: 2px solid #32CD32;")
            self.status_label.setStyleSheet("color: #006400;")
        else:
            self.status_label.setText("OFF")
            self.setStyleSheet("background-color: #FFB6C1; border: 2px solid #DC143C;")
            self.status_label.setStyleSheet("color: #8B0000;")

class S7_1200_OptimizedGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # PLC connection variables
        self.plc = snap7.client.Client()
        self.PLC_IP = "192.168.0.1"
        self.RACK = 0
        self.SLOT = 1
        self.connected = False
        
        # I/O indicators dictionaries
        self.input_indicators = {}
        self.output_indicators = {}
        
        # Refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_io_status)
        self.refresh_interval = 100  # Fast refresh for better responsiveness
        
        # API configuration
        self.API_ENABLED = False
        self.API_URL = "http://192.168.74.130:8069/plc/entry"
        self.API_KEY = "PLCS71200"
        self.API_INTERVAL = 5000  # 5 seconds
        self.api_timer = QTimer()
        self.api_timer.timeout.connect(self.send_data_to_api)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("S7-1200 Optimized I/O Controller")
        self.setGeometry(100, 100, 1000, 700)
        
        main_layout = QVBoxLayout()
        
        # Connection section
        main_layout.addWidget(self.create_connection_section())
        
        # I/O sections
        io_layout = QHBoxLayout()
        io_layout.addWidget(self.create_inputs_section())
        io_layout.addWidget(self.create_outputs_section())
        
        main_layout.addLayout(io_layout)
        self.setLayout(main_layout)

    def enable_api(self, enabled):
        """Enable or disable API integration"""
        self.API_ENABLED = enabled
        self.API_URL = self.api_url_input.text()
        self.API_KEY = self.api_key_input.text()
        
        if enabled:
            self.api_timer.start(self.API_INTERVAL)
            self.api_enable_btn.setText("Disable API")
            self.api_enable_btn.setStyleSheet("background-color: #90EE90;")
        else:
            self.api_timer.stop()
            self.api_enable_btn.setText("Enable API")
            self.api_enable_btn.setStyleSheet("")

    def send_data_to_api(self):
        """Send current I/O status to external API"""
        if not self.connected or not self.API_ENABLED:
            return

        try:
            # Prepare data with more detailed structure
            data = {
                "plc": {
                    "ip": self.PLC_IP,
                    "rack": self.RACK,
                    "slot": self.SLOT
                },
                "inputs": {name: int(indicator.state) for name, indicator in self.input_indicators.items()},
                "outputs": {name: int(indicator.state) for name, indicator in self.output_indicators.items()},
                "timestamp": datetime.datetime.now().isoformat(),
                "api_key": self.API_KEY
            }

            # Send to API in a separate thread
            Thread(target=self._send_api_request, args=(data,)).start()

        except Exception as e:
            print(f"API Data Preparation Error: {str(e)}")

    def _send_api_request(self, data):
        """Thread-safe API request with proper error handling"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.API_KEY}"
            }
            
            # Use the exact API URL without appending paths
            response = requests.post(
                self.API_URL,  # Use the base URL directly
                data=json.dumps(data),
                headers=headers,
                timeout=5
            )
            
            # Check for successful response
            if response.status_code == 200:
                print("API Update Successful")
            else:
                print(f"API Request Failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"API Request Exception: {str(e)}")
        except Exception as e:
            print(f"Unexpected API Error: {str(e)}")
            
    def create_connection_section(self):
        group = QGroupBox("Connection Settings")
        layout = QGridLayout()
        
        # Connection parameters
        layout.addWidget(QLabel("PLC IP:"), 0, 0)
        self.ip_input = QLineEdit("192.168.0.1")
        layout.addWidget(self.ip_input, 0, 1)
        
        layout.addWidget(QLabel("Rack:"), 0, 2)
        self.rack_input = QSpinBox()
        self.rack_input.setRange(0, 7)
        self.rack_input.setValue(0)
        layout.addWidget(self.rack_input, 0, 3)
        
        layout.addWidget(QLabel("Slot:"), 0, 4)
        self.slot_input = QSpinBox()
        self.slot_input.setRange(0, 31)
        self.slot_input.setValue(1)
        layout.addWidget(self.slot_input, 0, 5)
        
        # Status and buttons
        self.connection_status = QLabel("Status: Disconnected")
        self.connection_status.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.connection_status, 1, 0, 1, 2)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_plc)
        layout.addWidget(self.connect_btn, 1, 2)
        
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_plc)
        self.disconnect_btn.setEnabled(False)
        layout.addWidget(self.disconnect_btn, 1, 3)
        
        # API controls
        layout.addWidget(QLabel("API:"), 2, 0)
        self.api_enable_btn = QPushButton("Enable API")
        self.api_enable_btn.setCheckable(True)
        self.api_enable_btn.clicked.connect(self.enable_api)
        layout.addWidget(self.api_enable_btn, 2, 1)
        
        self.api_url_input = QLineEdit(self.API_URL)
        layout.addWidget(self.api_url_input, 2, 2, 1, 2)
        
        self.api_key_input = QLineEdit(self.API_KEY)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.api_key_input, 2, 4, 1, 2)
        
        group.setLayout(layout)
        return group
    
    def create_inputs_section(self):
        group = QGroupBox("Digital Inputs (Read Only)")
        layout = QGridLayout()
        
        # Create input indicators I0.0 to I1.7
        row, col = 0, 0
        for byte_num in range(2):
            for bit_num in range(8):
                input_name = f"I{byte_num}.{bit_num}"
                indicator = IOIndicator(input_name, "input")
                self.input_indicators[input_name] = indicator
                layout.addWidget(indicator, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
        
        group.setLayout(layout)
        return group
    
    def create_outputs_section(self):
        group = QGroupBox("Digital Outputs (Read/Write)")
        layout = QGridLayout()
        
        # Control buttons for all outputs
        control_layout = QHBoxLayout()
        
        all_on_btn = QPushButton("All ON")
        all_on_btn.setStyleSheet("background-color: #90EE90; font-weight: bold;")
        all_on_btn.clicked.connect(self.set_all_outputs_on)
        control_layout.addWidget(all_on_btn)
        
        all_off_btn = QPushButton("All OFF")
        all_off_btn.setStyleSheet("background-color: #FFB6C1; font-weight: bold;")
        all_off_btn.clicked.connect(self.set_all_outputs_off)
        control_layout.addWidget(all_off_btn)
        
        layout.addLayout(control_layout, 0, 0, 1, 4)
        
        # Create output indicators Q0.0 to Q1.7
        row, col = 1, 0
        for byte_num in range(2):
            for bit_num in range(8):
                output_name = f"Q{byte_num}.{bit_num}"
                indicator = IOIndicator(output_name, "output")
                indicator.toggle_requested = lambda name=output_name: self.toggle_output(name)
                indicator.set_state_requested = lambda state, name=output_name: self.set_output_state(name, state)
                self.output_indicators[output_name] = indicator
                layout.addWidget(indicator, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
        
        group.setLayout(layout)
        return group
    
    def connect_plc(self):
        try:
            self.PLC_IP = self.ip_input.text()
            self.RACK = self.rack_input.value()
            self.SLOT = self.slot_input.value()
            
            self.plc.connect(self.PLC_IP, self.RACK, self.SLOT)
            
            if self.plc.get_connected():
                self.connected = True
                self.connection_status.setText("Status: Connected")
                self.connection_status.setStyleSheet("color: green;")
                self.connect_btn.setEnabled(False)
                self.disconnect_btn.setEnabled(True)
                self.refresh_timer.start(self.refresh_interval)
            else:
                self.connection_status.setText("Status: Connection Failed")
                self.connection_status.setStyleSheet("color: red;")
                
        except Exception as e:
            self.connection_status.setText(f"Status: Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")
    
    def disconnect_plc(self):
        try:
            self.refresh_timer.stop()
            if self.plc.get_connected():
                self.plc.disconnect()
            self.connected = False
            self.enable_api(False)
            self.connection_status.setText("Status: Disconnected")
            self.connection_status.setStyleSheet("color: black;")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
        except Exception as e:
            self.connection_status.setText(f"Status: Disconnect Error - {str(e)[:30]}...")
    
    def refresh_io_status(self):
        if not self.connected:
            return
        
        try:
            # Read digital inputs (2 bytes for I0.0-I1.7)
            inputs_data = self.plc.read_area(Areas.PE, 0, 0, 2)
            for byte_num in range(2):
                for bit_num in range(8):
                    input_name = f"I{byte_num}.{bit_num}"
                    bit_value = bool((inputs_data[byte_num] >> bit_num) & 1)
                    self.input_indicators[input_name].set_state(bit_value)
            
            # Read digital outputs (2 bytes for Q0.0-Q1.7)
            outputs_data = self.plc.read_area(Areas.PA, 0, 0, 2)
            for byte_num in range(2):
                for bit_num in range(8):
                    output_name = f"Q{byte_num}.{bit_num}"
                    bit_value = bool((outputs_data[byte_num] >> bit_num) & 1)
                    self.output_indicators[output_name].set_state(bit_value)
            
        except Exception as e:
            self.connection_status.setText(f"Status: Read Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")
    
    def set_output_state(self, output_name, state):
        if not self.connected:
            return
        
        try:
            # Parse output name
            parts = output_name.replace('Q', '').split('.')
            byte_num = int(parts[0])
            bit_num = int(parts[1])
            
            # Read current outputs
            outputs_data = self.plc.read_area(Areas.PA, 0, byte_num, 1)
            current_byte = outputs_data[0]
            
            # Set or clear bit
            if state:
                new_byte = current_byte | (1 << bit_num)
            else:
                new_byte = current_byte & ~(1 << bit_num)
            
            # Write back
            self.plc.write_area(Areas.PA, 0, byte_num, bytearray([new_byte]))
            
        except Exception as e:
            self.connection_status.setText(f"Status: Write Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")
    
    def toggle_output(self, output_name):
        if not self.connected:
            return
        
        try:
            # Parse output name
            parts = output_name.replace('Q', '').split('.')
            byte_num = int(parts[0])
            bit_num = int(parts[1])
            
            # Read current outputs
            outputs_data = self.plc.read_area(Areas.PA, 0, byte_num, 1)
            current_byte = outputs_data[0]
            
            # Toggle bit
            new_byte = current_byte ^ (1 << bit_num)
            
            # Write back
            self.plc.write_area(Areas.PA, 0, byte_num, bytearray([new_byte]))
            
        except Exception as e:
            self.connection_status.setText(f"Status: Toggle Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")
    
    def set_all_outputs_on(self):
        if not self.connected:
            return
        
        try:
            self.plc.write_area(Areas.PA, 0, 0, bytearray([0xFF, 0xFF]))
        except Exception as e:
            self.connection_status.setText(f"Status: All ON Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")
    
    def set_all_outputs_off(self):
        if not self.connected:
            return
        
        try:
            self.plc.write_area(Areas.PA, 0, 0, bytearray([0x00, 0x00]))
        except Exception as e:
            self.connection_status.setText(f"Status: All OFF Error - {str(e)[:30]}...")
            self.connection_status.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = S7_1200_OptimizedGUI()
    gui.show()
    sys.exit(app.exec())