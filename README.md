#  AI Resume Analyzer & Classifier

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)

A robust **Full-Stack AI Application** that automates resume screening. It parses PDF resumes, extracts key details (skills, contact info, education), calculates experience using smart date-logic, and classifies the candidate's role using Machine Learning.

---

##  Key Features

###  AI & NLP Capabilities
- **Role Classification:** Uses **TF-IDF & Logistic Regression** to classify resumes into roles like *Software Engineer, Data Scientist, DevOps, etc.* with a confidence score.
- **Smart Skill Extraction:** Hybrid approach using **Direct Matching** and **Sentence-Transformers (Deep Learning)** to identify technical skills semantically.
- **Information Extraction:** utilizes **SpaCy (NER)** and complex **Regex** to extract Name, Email, and Phone Number accurately.
- **Experience Calculator:** Intelligent logic to parse date ranges (e.g., "Jan 2019 - Present") and calculate total years of experience, assigning levels (*Junior/Mid/Senior*).

### 💻 Modern Frontend (UI/UX)
- **Drag & Drop Upload:** Seamless file handling.
- **Interactive Dashboard:** Beautiful visualization of extracted data using **Glassmorphism** design.
- **Real-time Analysis:** Instant feedback with loading animations.
- **Responsive Design:** Fully responsive UI built with **Tailwind CSS**.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI | High-performance API & Static File Serving |
| **Frontend** | Next.js (React), Tailwind | Modern, reactive User Interface |
| **ML/NLP** | Scikit-learn, SpaCy, Transformers | Text processing & Classification models |
| **PDF Parsing** | pdfplumber | Extracting raw text from PDF files |
| **Deployment** | Docker, Render | Containerization & Cloud Hosting |

---

##  How to Run Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (Optional)

### Method 1: Using Docker (Recommended)
This is the easiest way to run the app without installing dependencies manually.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer

2. **Build & Run**
   docker build -t resume-app .
   docker run -p 8000:8000 resume-app
3.**Access the App**
   Open http://localhost:8000 in your browser.
   
### Method 2: Manual Setup
# Create virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP Model
python -m spacy download en_core_web_sm

2 **Frontend Setup**
   cd frontend
   npm install
   npm run build
   cd ..


3. **Run the Application**
   python main.py

### How It Works (Architecture)
**Input** 
User uploads a PDF via the Next.js Frontend.
**Processing**
FastAPI receives the file.
pdfplumber converts PDF to raw text.
Cleaning: Text is normalized (removing special characters).
**Intelligence Layer**
Classification: The text is vectorized and passed through a pre-trained LogisticRegression model to predict the Job Role.
NER: SpaCy identifies the candidate's Name.
Semantic Search: Sentence-Transformers compares resume text against a known Skills Database to find matches (e.g., mapping "ReactJS" to "React").
**Output** 
JSON response is sent back to the frontend, which renders the Dashboard.

### Project Structure

resume-project/
├── backend/
│   ├── parser.py        # Logic for PDF parsing & Extraction
│   ├── classifier.py    # ML Model Training & Prediction logic
├── frontend/            # Next.js Application
│   ├── src/app/         # UI Components & Pages
│   ├── out/             # Static Build (Served by Python)
├── main.py              # Entry point (FastAPI Server)
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python Dependencies
└── model.pkl            # Trained ML Model

   
