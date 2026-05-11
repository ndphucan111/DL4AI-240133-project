---
title: Stock Api Backend - AI-Powered Stock Prediction
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

---

# **Final project - Spring 2026**

* **Course:** CS313 - Deep Learning for Artificial Intelligence 


* **Project:** Time-series data and application to stock markets 


* **Author:** **Nguyen Do Phuc An - 240133**

---

## **1. Overview**

This project applies **Deep Learning (LSTM)** models to analyze stock market data from **Nasdaq and Vietnam**. The system processes large datasets, providing forecasts and comparisons between the two data streams. The system goes beyond simply training the model; it's deployed as a complete **SaaS platform**.

* The model aims to predict prices based on **six technical characteristics** (**Open, High, Low, Close, Adj Close, Volume**) instead of just the opening price. It can predict prices for a specific day (**$k^{th}$ day**) or a series of **k consecutive days** in the future.


* The model automatically identifies **Buy and Sell points** based on the model's training results, probability, and expected profit threshold. Then, based on statistics, it suggests an **optimal investment portfolio** based on the risk-return ratio for different investor groups (i.e., using past results to provide an average, safe point for the present).



Additionally, **AI-Powered Stock Prediction** is a web demo showing the results of training the model in use (**Run the demo on Hugging Face Space**).

---

## **2. Technology Stack**

* **Core AI:** Python, TensorFlow (LSTM), Scikit-learn, Pandas, Numpy 

* **Backend:** FastAPI (REST API Service) 

* **Frontend:** Streamlit 

* **Deployment:** Docker, Hugging Face Spaces 


---

## **3. Repository Structure**

* **`csv/`**: Uncompressed stock data files.
* **`graph/`**: Graphs from the notebook.
* **`models/`**: Trained models (**`.keras`**).
* **`.gitattributes` & `.gitignore**`: Git configuration files.
* **`240133_Final_project_DL4AI.ipynb`**: Notebook containing the entire training process (**Tasks 1-4**).
* **`app.py`**: Web frontend using **Streamlit** code (**Task 5.2**).
* **`main.py`**: API (**Backend**) on **FastAPI**, used to load the model and handle forecasting requests (**Task 5.1**).
* **`Dockerfile` & `start.sh**`: Docker to package everything into a container, used to deploy to Hugging Face or other Cloud platforms.
* **`requirements.txt`**: Libraries to download (**TensorFlow, FastAPI, Streamlit...**) to run the project.
* **`README.md`**: Overview, instructions for running and using the project. 


---

## **4. Project Execution Guide**

### **A. First Step**

**Clone the repository:**

```bash
git clone https://github.com/ndphucan111/DL4AI-240133-project.git
cd DL4AI-240133-project

```

**Install dependencies:**

```bash
pip install -r requirements.txt

```

**Run the system:**

```bash
./start.sh

```

### **B. Run Notebook (`240133_Final_project_DL4AI.ipynb`)**

* Follow the detailed instructions in **Notebook** to retrieve data and models (**Google Colab** or **local help** provided).
* Run each code **sequentially** (you can skip running the model code as it's already available).

### **C. Running API and Web**

#### **1. Run Local Setup**

* **For backend (FastAPI):** Open Terminal and run: `python main.py` (The API service will default to running at: **http://localhost:8000**). 


* **For frontend (Streamlit):** Open another Terminal and run: `streamlit run app.py` (The web interface will automatically open in the browser at: **http://localhost:8501**).

#### **2. Run Automatic Script**

Open Terminal and run:

```bash
chmod +x start.sh
./start.sh

```

#### **3. Run Docker (Recommended)**

* **Build Image:**
`docker build -t dl4ai-stock-app .`
* **Run Container:**
`docker run -p 7860:7860 dl4ai-stock-app`

---

## **5. Live Demo**

🚀 **Live demo link for AI-Powered Stock Prediction:** [https://huggingface.co/spaces/ndphucan/stock-api-backend](https://huggingface.co/spaces/ndphucan/stock-api-backend)
