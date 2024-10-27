
# Network IP Checker

A live network administration tool to check external and internal IP addresses. Built using **Python (Flask)** for the backend and **JavaScript/HTML** for the frontend, this application is ideal for network administrators looking to monitor IP addresses in real time.

## Features

- **External IP Check**: Fetches and displays the current external IP address.
- **Internal IP Check**: Displays local network IPs, such as internal IPs of connected devices.
- **Real-time Updates**: Option to refresh IP information automatically at set intervals.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/network-ip-checker.git
   cd network-ip-checker
   ```

2. **Install required dependencies**:

   This app requires Python, Flask, and Requests. You can install them with:

   ```bash
   pip install flask requests
   ```

## Usage

1. **Start the Flask Server**:

   ```bash
   python app.py
   ```

2. **Open the Application**:

   Go to `http://127.0.0.1:5000` in your web browser to view the network IP checker interface.

## File Structure

```
network-ip-checker/
├── app.py                 # Flask backend script
├── templates/
│   └── index.html         # Frontend HTML file
└── README.md              # Project documentation
```

## Contributing

Feel free to fork the repository and submit pull requests if you want to contribute new features or fix issues.

## License

This project is licensed under the MIT License.

---
