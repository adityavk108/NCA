# Neural Cellular Automata (NCA)
## Inspiration
I first came across Neural Cellular Automata (NCA) while watching a very interesting YouTube video by [Emergent Garden](https://x.com/max_romana?mx=2). 
The idea of using the concept of convolution to implement a Cellular Automata fascinated me and I wanted to see if I could implement it myself and tinker around. 


**Sources:**
- [YouTube Video: "What are neural cellular automata?"](https://www.youtube.com/watch?v=3H79ZcBuw4M) 
- https://neuralpatterns.io/


![waves2](https://github.com/user-attachments/assets/e903a60a-6381-46cf-bfc8-07a0c3d346f8)


---

## What is Cellular Automata?
Cellular Automata (CA) are mathematical models that consist of a grid of cells, where each cell may hold a value (classically a 0 or 1). In every update, a set of simples rules are applied to each cell determine it's next state, usually involving the state 
of it's neighbours. These simple rules can give rise to incredibly complex behaviors, such as:
- [Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), a famous mathematical model with simple rules giving rise to complex life-like patterns
- [Wolfram's rule 30](https://en.wikipedia.org/wiki/Rule_30), another famous CA mimicking natural patterns from simple rules
- Simulations of natural phenomena like fire, waves, and patterns in animal skins, used in biological and chemical modeling

CA have been widely studied in physics, artificial life, and even cryptography due to their ability to model highly complex systems with local interactions.


![conwaygif](https://github.com/user-attachments/assets/87e1b74c-5695-4d9f-99b8-0b3e315885e3)

## What is Neural Cellular Automata (NCA)?
Neural Cellular Automata extend traditional CA by introducing **neural networks** to learn update rules instead of manually defining them. This means that rather than relying on fixed, pre-programmed rules, each cell in the grid has a **small neural network** 
that decides its state dynamically based on local interactions. This approach makes CA more flexible and adaptive, enabling complex patterns to emerge organically.

![pathsgif](https://github.com/user-attachments/assets/16219299-ccbd-4f6c-9a2a-6efb7cbcf315)


### **Key Features of NCA:**
- **Self-Organization** – Grows patterns from random noise, capable of forming complex designs over time
- **Robustness** – Can regenerate patterns even after damage, making it an interesting model for biological regeneration
- **Emergent Behavior** – Displays complex dynamics from simple interactions, similar to natural morphogenesis
- **Scalability** – Works on arbitrary grid sizes without global control, allowing decentralized growth patterns

---

## How Does It Work?
At each time step, every cell in the grid updates its state based on its local neighborhood. Unlike traditional CA, where the rules are predefined, NCA learns an update function using a **Convolutional Neural Network (CNN)**.
In our case, we use a fixed filter as a proof of concept of NCA.

1. **State Representation** – Each cell maintains a **hidden state vector** (e.g., 16-dimensional instead of just binary on/off). This allows the system to store information across multiple time steps.
2. **Neighborhood Interaction** – A **convolution operation** is applied, allowing each cell to “see” its neighbors and exchange information.
3. **Update Rule (Neural Network)** – A tiny **convolution filter** processes this local information and outputs the new state.
4. **Global Emergence** – Over time, the system self-organizes into patterns, structures, or regenerates damaged areas.

### **Understanding Convolution in NCA**
Convolution is the core operation in NCA. It works by sliding a small **filter (kernel)** across the grid and computing a weighted sum of neighboring cell states. This allows each cell to:
- Detect edges and structures, essential for forming distinct shapes
- Exchange information with its neighbors, helping in cooperative growth
- Learn transformation rules via neural networks, adapting its state based on learned behaviors

![wolframgif](https://github.com/user-attachments/assets/80413c5e-6ec9-46e5-a4f0-506de6dc7f6c)

---

## Usage Guide

### **Installation**
Ensure you have Python and the required dependencies installed:
```bash
# Clone the repository
git clone https://github.com/adityavk108/NCA.git
cd NCA
# Install dependencies
pip install -r requirements.txt
```

### **Running the Program**
To generate an NCA pattern, run:
```bash
python main.py
```
or simply click on `main.py` in your file explorer.
To see the Wolfram's rule 30 simulation click on `wolfram.py`

### **User Interface**
![Screenshot 2025-02-06 220451](https://github.com/user-attachments/assets/e8f98034-0579-46f6-bbfc-c2a1e2d319f9)

### **Usage Instructions**

### **Restarts**
Use restarts to refresh the frame with specific values:  
- `randints`: Assigns random values of `1` or `0` to each pixel.  
- `randfloats`: Assigns random floating-point values.  
- `center`: Assigns a value of `1` at the center pixel and `0` for all others.  

### **Load**
Pick a preset simulation to load. You may need to select a restart option to initialize it properly.  

### **Recording**
- Click **Start** to begin recording generated frames.  
- Click **Stop** to stop recording.  
- The video is saved as `render.avi`.  
- ⚠ **Caution:** The video file may get corrupted if it is too short or if the program is stopped abruptly.  

### **Custom Filters**
- Click **Random Filters** to randomly set the filter.  
- You can also manually set the activation function for the filters.  

Enjoy experimenting with cellular automata simulations! 

## Contributions
This project is an ongoing exploration of self-organizing systems. Contributions in terms of code improvements, new visualization techniques, and experimental extensions are welcome. Feel free to contribute by submitting issues, pull requests, or suggestions.

## Future Work
 **Enhancements & Next Steps:**
- Implementing 3D NCA models for volumetric growth simulations 
- Training models on different biological patterns 
- Optimizing real-time performance using GPU acceleration 
- Experimenting with reinforcement learning for adaptive NCA behaviors 

 **Happy Exploring Neural Cellular Automata!**

