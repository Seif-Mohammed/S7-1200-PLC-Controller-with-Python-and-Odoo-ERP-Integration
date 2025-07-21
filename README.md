# S7-1200 PLC I/O Controller

A modern Python-based GUI application for monitoring and controlling Siemens S7-1200 PLCs with real-time I/O visualization and external API integration.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-orange)
![SNAP7](https://img.shields.io/badge/PLC-SNAP7-red)

## 🚀 Features

- **Real-time I/O Monitoring**: Monitor digital inputs (I0.0-I1.7) and outputs (Q0.0-Q1.7) in real-time
- **Interactive Output Control**: Individual output control with ON/OFF/TOGGLE buttons
- **Batch Operations**: Control all outputs simultaneously with "All ON" and "All OFF" functions
- **External API Integration**: Send PLC data to external systems (Odoo ERP integration ready)
- **Visual Status Indicators**: Color-coded I/O status with intuitive green/red indicators
- **Connection Management**: Easy PLC connection setup with IP, Rack, and Slot configuration
- **Fast Refresh Rate**: 100ms refresh interval for responsive monitoring
- **Error Handling**: Comprehensive error handling with user-friendly status messages

## 📋 Requirements

### Hardware
- Siemens S7-1200 PLC
- Ethernet connection between PC and PLC
- Compatible I/O modules

### Software Dependencies
```
python>=3.8
PyQt6>=6.0.0
python-snap7>=1.0
requests>=2.25.0
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/s7-1200-plc-controller.git
cd s7-1200-plc-controller
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install SNAP7 Library
Download and install the SNAP7 library for your operating system:
- **Windows**: Download from [SNAP7 Official Site](http://snap7.sourceforge.net/)
- **Linux**: `sudo apt-get install libsnap7-1 libsnap7-dev`
- **macOS**: `brew install snap7`

## 🚦 Quick Start

1. **Configure your PLC network settings**:
   - Default IP: `192.168.0.1`
   - Default Rack: `0`
   - Default Slot: `1`

2. **Run the application**:
   ```bash
   python ODOO-S7.py
   ```

3. **Connect to PLC**:
   - Enter your PLC's IP address
   - Set appropriate Rack and Slot values
   - Click "Connect"

4. **Monitor and Control**:
   - View real-time input states in the "Digital Inputs" section
   - Control outputs using individual buttons or batch operations
   - Enable API integration for external system communication

## 📊 API Integration

The application supports external API integration for sending PLC data to external systems like ERP or SCADA systems.

### API Configuration
- **URL**: Configure your API endpoint
- **Key**: Set authentication key
- **Interval**: 5-second default transmission interval

### API Data Format
```json
{
  "plc": {
    "ip": "192.168.0.1",
    "rack": 0,
    "slot": 1
  },
  "inputs": {
    "I0.0": 1,
    "I0.1": 0,
    "...": "..."
  },
  "outputs": {
    "Q0.0": 1,
    "Q0.1": 0,
    "...": "..."
  },
  "timestamp": "2025-01-21T10:30:00.000000",
  "api_key": "PLCS71200"
}
```

## 🏗️ Project Structure

```
s7-1200-plc-controller/
│
├── ODOO-S7.py              # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
│
├── docs/                  # Documentation
│   ├── installation.md   # Detailed installation guide
│   ├── api-reference.md  # API documentation
│   └── troubleshooting.md # Common issues and solutions
│
├── examples/             # Example configurations
│   ├── plc-config.json  # Sample PLC configurations
│   └── api-examples.py   # API integration examples
│
└── screenshots/          # Application screenshots
    ├── main-interface.png
    ├── connection-setup.png
    └── io-monitoring.png
```

## 🔧 Configuration

### PLC Configuration
The application supports standard S7-1200 configurations:

- **CPU Models**: All S7-1200 series CPUs
- **Communication**: Ethernet TCP/IP (Port 102)
- **I/O Range**: 
  - Inputs: I0.0 to I1.7 (16 digital inputs)
  - Outputs: Q0.0 to Q1.7 (16 digital outputs)

### Network Setup
Ensure your PLC is configured for Ethernet communication:
1. Set static IP address in TIA Portal
2. Enable "Permit access with PUT/GET communication"
3. Configure firewall settings if necessary

## 🐛 Troubleshooting

### Common Issues

**Connection Failed**
- Verify PLC IP address and network connectivity
- Check PLC configuration in TIA Portal
- Ensure SNAP7 library is properly installed

**API Integration Issues**
- Verify API endpoint URL and authentication
- Check network connectivity to API server
- Review API server logs for error details

**Performance Issues**
- Adjust refresh interval if experiencing lag
- Check network latency to PLC
- Monitor system resources

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### I/O Monitoring
![I/O Monitoring](screenshots/io-monitoring.png)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SNAP7 Library](http://snap7.sourceforge.net/) - S7 communication protocol implementation
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Cross-platform GUI toolkit
- [Siemens](https://www.siemens.com/) - S7-1200 PLC platform

## 📞 Support

If you have questions or need support:

- 📧 Email: your.email@domain.com
- 💬 Issues: [GitHub Issues](https://github.com/Seif-Mohammed/S7-1200-PLC-Controller-with-Python-and-Odoo-ERP-Integration/issues)
- 📖 Documentation: [Wiki](https://github.com/Seif-Mohammed/S7-1200-PLC-Controller-with-Python-and-Odoo-ERP-Integration/wiki)

## 🔄 Changelog

### v1.0.0 (2025-01-21)
- Initial release
- Real-time I/O monitoring
- Output control functionality
- API integration support
- Comprehensive error handling

---
