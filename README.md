# 🩺 MLops_prediction_app

This is a end to end deployed machine learning system with basic MLOps principles.

---

# 📌 Project Overview

An end-to-end deployed ML inference system with basic MLOps principles.  

The frontend is made by **Streamlit** and the backend is served via **FastAPI**.  

To include containerization too, I containerized the whole backend service into a **Docker container** which was deployed on **Render**.

---

# 🏗 Architecture

Project follows a client-server architecture.

```
User
  ↓
Streamlit Frontend
  ↓ HTTP POST
FastAPI Backend
  ↓
ML Model (Logistic Regression)
  ↓
JSON Response
```

---

# 🔄 System Flow

1. User interacts with Streamlit web interface.  
2. Streamlit collects the data and sends it to the FastAPI backend by HTTP POST request.  
3. The FastAPI server receives the data, performs necessary preprocessing, and passes it to the trained Logistic Regression model (.pkl file).  
4. The model generates a prediction.  
5. Streamlit receives the prediction and displays it on the interface.  

---

# 🤖 Model Details

Logistic Regression model was used.

We had two target variables:
- `0` → Non-diabetic  
- `1` → Diabetic  

Logistic regression uses the **sigmoid function** to squash the output between 0 and 1 (a probability).

---

## 📊 Train-Test Split

Data was split into **80/20**:

- 80% → Training set  
- 20% → Testing set  

---

## ⚙️ Preprocessing – StandardScaler

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### fit_transform()
- Calculates statistics (mean, std) from X_train  
- Uses those stats to scale X_train  
- Used only on training data  

### transform()
- Uses already calculated statistics  
- Applies scaling to X_test  

---

## ⚖️ Handling Class Imbalance

Dataset distribution:

```
0 → 500
1 → 268
```

Used:

```python
class_weight="balanced"
```

It gives higher weight to the minority class and lower weight to the majority class.

This improved recall and other classification metrics.

---

## 📈 Threshold Optimization

Default threshold = 0.5

Results:

```
Accuracy: 0.7337
Recall: 0.7037
Precision: 0.6031
F1: 0.6495
```

In medical screening, recall and precision are more prioritized metrics.

So I lowered the threshold to **0.48**.

Results with 0.48 threshold:

```
Accuracy: 0.7597
Recall: 0.7963
Precision: 0.6231
F1: 0.6991
```

---

## 📌 Metric Interpretation

**Recall (Sensitivity) = 80%**

- Out of all actual diabetic patients, the model correctly identifies 80% of them.  
- Missing a diabetic patient (false negative) can delay treatment and lead to serious complications.  
- We prioritize high recall to minimize missed cases.

**Precision = 62%**

- Of all patients flagged as diabetic, 62% are truly diabetic.  
- False positives mean unnecessary follow-up tests, but less harmful than missing real cases.

**Accuracy = 76%**

Accuracy looks decent but can be misleading in imbalanced datasets.

---

# 📂 Project Structure

```
MLops_prediction_app/
│
├── MLops_diabetes_pred/
│   ├── backend/
│   │   ├── src/
│   │   ├── models/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── frontend/
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── data/
│   └── notebooks/
│
└── README.md
```

---

## notebooks/
Contains the python notebook used initially for data exploration and finding patterns in the dataset.

## frontend/
Contains the Streamlit UI code.

## backend/
Contains:
- `src/` → training script and FastAPI app  
- `models/` → serialized model and scaler  
- `Dockerfile` → instructions to containerize the backend  

The blueprint of the backend is called a **Docker image**, and when that image runs (locally or on cloud), it is called a **Docker container**.

---

# ⚡ How the Backend Works

The backend exposes an HTTP endpoint:

```
POST /predict
```

When a request is received:

- Input data is validated using a Pydantic schema.
- Features are converted into NumPy format.
- StandardScaler transforms the input.
- Logistic Regression computes probability.
- Classification threshold is applied.
- JSON response is returned.

The FastAPI application runs on top of **Uvicorn**, which is responsible for handling incoming HTTP requests.

---

# 🌐 Deployment on Render

The backend is deployed on Render using Docker.

Deployment flow:

1. Render pulls the GitHub repository.
2. Detects the Dockerfile.
3. Builds the Docker image.
4. Runs the container.
5. Exposes a public URL.

---

# 🚀 Running the Project Locally

This project consists of two independent services:

- Backend (FastAPI)
- Frontend (Streamlit)

---

## 🔹 Clone the Repository

```bash
git clone https://github.com/abd-04/MLops_prediction_app.git
cd MLops_prediction_app
```

---

## 🔹 Running Backend

```bash
cd MLops_diabetes_pred/backend
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 10000
```

---

## 🔹 Running the Frontend

Open a new terminal window:

```bash
cd MLops_diabetes_pred/frontend
pip install -r requirements.txt
streamlit run app.py
```

To run locally, update the `requests.post()` inside `frontend/app.py`  
from the Render endpoint to:

```
http://localhost:10000/predict
```

⚠ **The backend should be running before the frontend.**

---

# 🎯 Future Milestones

- Add monitoring  
- Add CI/CD complete pipeline  
- Improve production-level automation  

---
