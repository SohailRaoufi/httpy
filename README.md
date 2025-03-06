### **Httpy - A Lightweight HTTP Server**  

![Httpy](https://img.shields.io/badge/Python-3.x-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)  

Httpy is a simple and lightweight HTTP server written in Python. It serves static files and directories, allowing users to browse files from their local system over a network.  

---

## **🚀 Features**  
✅ Minimalistic HTTP server using pure Python sockets  
✅ Supports **file serving** for HTML, CSS, JS, images, etc.  
✅ Supports **Log Levels**.  
✅ **Directory listing** when accessing folders  
✅ Handles basic HTTP request parsing  
✅ Supports **custom host, port, and directory** via command-line arguments  
✅ Graceful shutdown with `Ctrl + C`  

---

## **📌 Installation & Usage**  

### **1️⃣ Install Python**  
Make sure you have **Python 3.x** installed.  

### **2️⃣ Clone the Repository**  
```bash
git clone https://github.com/sohailraoufi/httpy.git
cd httpy
```

### **3️⃣ Run the Server**  
Start the server with:  
```bash
python httpy.py --host 0.0.0.0 --port 8080 --path /your/directory --log
```
Or simply use the default settings:  
```bash
python httpy.py
```

### **4️⃣ Access the Server**  
Open your browser and go to:  
```
http://localhost:8001
```

---

## **🛠 Command-Line Arguments**  
| Argument   | Description                                   | Default Value  |
|------------|-----------------------------------------------|----------------|
| `--host`   | The hostname or IP address to bind to        | `localhost`    |
| `--port`   | The port number for the server               | `8001`         |
| `--path`   | The directory to serve                       | `current dir`  |
| `--log`    | Allow to show the log.                       | `False`  |

Example usage:  
```bash
python httpy.py --host 0.0.0.0 --port 9000 --path ~/public_html --log
```

---

## **📂 Directory Listing Example**  
When accessing a directory, Httpy generates an **HTML page** listing all files and subdirectories:  
```
/my-folder
    ├── index.html
    ├── style.css
    ├── script.js
    └── images/
```
Clicking a file will open it in the browser.

---

## **🛑 Stopping the Server**  
To gracefully shut down the server, press **`Ctrl + C`**.  

---

## **📝 License**  
This project is licensed under the **MIT License**.  

---

