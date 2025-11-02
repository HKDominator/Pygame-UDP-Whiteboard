# 🎨 Pygame-UDP-Whiteboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-orange?logo=pygame)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Pygame-UDP-Whiteboard** is a real-time collaborative whiteboard built with **Python**, **Pygame**, and **UDP sockets**.  
Multiple users on the same network can draw together — shapes are broadcast over UDP packets and instantly displayed on all clients.

---

## 🚀 Features

- 🖊️ **Real-time collaborative drawing**
- 🌐 **UDP-based networking** (lightweight & low-latency)
- 🎨 **Three Drawing Modes**  
  - Line  
  - Rectangle  
  - Circle
- 🧩 **Toggle Fill / Outline**
- ⚡ **Concurrent drawing receiver using threads**
- 💡 **Lightweight, stateless client-server architecture**

---

## 🧠 How It Works

1. **Clients** send shape data (type, coordinates, color, etc.) to the **server**.  
2. The **server** rebroadcasts the data to every client on the network.  
3. All **clients** receive and render the drawings locally using Pygame.

---

## 📁 Project Structure

<pre>
Pygame-UDP-Whiteboard/
│
├── server.py      # UDP broadcast server
├── client.py      # Pygame-based drawing client
└── README.md      # You are here
</pre>

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
<pre><code>git clone https://github.com/yourusername/Pygame-UDP-Whiteboard.git
cd Pygame-UDP-Whiteboard
</code></pre>

### 2️⃣ Install dependencies
Make sure you have **Python 3.8+** and **Pygame** installed:
<pre><code>pip install pygame
</code></pre>

### 3️⃣ Run the server
On one machine (or locally for testing):
<pre><code>python server.py
</code></pre>

### 4️⃣ Run the client
On the same or other computers connected to the same network:
<pre><code>python client.py
</code></pre>

> ⚙️ **Note:**  
> Update the IPs in both files if needed to match your local network:  
> 
> <pre><code>SERVER_HOST = '10.152.3.6'
BROADCAST_IP = '10.152.255.255'
SERVER_PORT = 1234
</code></pre>

---

## 🎮 Controls

| Key | Action |
|-----|---------|
| `1` | Draw **Line** (Blue de France) |
| `2` | Draw **Rectangle** (Jasmine) |
| `3` | Draw **Circle** (Lavender) |
| `F` | Toggle **Fill / Outline** |
| 🖱️ Mouse | Click and drag to draw shapes |

---

## 🧱 Technical Details

- **Protocol:** UDP (stateless, low latency)  
- **Serialization:** Binary encoding with `struct`  
- **Concurrency:** Threaded receiver using `queue.Queue`  
- **Graphics:** Rendered using Pygame (`pygame.draw`)  
- **Error Handling:** Graceful socket teardown and exception handling  

---

## 💡 Example Use Case

Start the **server** on one computer, and run multiple **clients** on different devices within the same network.  
All participants can draw together in real-time — ideal for:

- Collaborative sketching  
- Teaching & brainstorming  
- Rapid UI/UX prototyping  
- Fun multiplayer creativity projects  

---

## 🔮 Future Improvements

- ✍️ Add freehand brush & adjustable thickness  
- 👥 Add usernames and color assignment per client  
- 💾 Save / Load drawings  
- 🔒 Add message integrity and simple authentication  
- 🌈 Add GUI elements (toolbars, color picker, shape selector)

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Andrei Bodrogean**  
🎓 Computer Science Student at UBB Cluj  
📍 Built for learning, collaboration, and fun  
💬 Contributions and feedback are always welcome!
