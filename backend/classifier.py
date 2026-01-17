import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "model.pkl"

def train_model():
    print("Training Classifier Model...")
    # Synthetic Data representing the Mandatory Categories
    data = [
        
    (
        "Python, Django, Flask, REST API development, SQL & relational databases, backend architecture, authentication, performance optimization",
        "Software Engineer",
        "Experienced in building secure, scalable, and high-performance backend systems using Python frameworks and database-driven architectures."
    ),
    (
        "Java, Spring Boot, Microservices architecture, OOP principles, RESTful services, system design, scalability",
        "Software Engineer",
        "Specialized in enterprise-grade Java applications with clean object-oriented design and distributed microservices systems."
    ),
    (
        "React.js, JavaScript, HTML5, CSS3, UI/UX design, responsive layouts, component-based architecture",
        "Web Developer",
        "Focused on creating interactive, user-friendly, and visually appealing web interfaces with modern frontend technologies."
    ),
    (
        "Next.js, Tailwind CSS, Redux, responsive design, SSR, performance optimization",
        "Web Developer",
        "Builds fast, SEO-friendly, and scalable web applications with modern React frameworks and state management."
    ),
    (
        "Machine Learning, PyTorch, TensorFlow, AI models, Deep Learning, model training & evaluation",
        "AI/ML Engineer",
        "Develops intelligent systems and predictive models using state-of-the-art deep learning frameworks and techniques."
    ),
    (
        "Natural Language Processing, Computer Vision, Data Science, feature engineering, model deployment",
        "AI/ML Engineer",
        "Experienced in extracting insights from text, image, and structured data using advanced AI and data science methods."
    ),
    (
        "Jenkins, Docker, Kubernetes, AWS, CI/CD pipelines, cloud infrastructure, automation",
        "DevOps/Cloud Engineer",
        "Ensures reliable deployment, scalability, and automation of applications through modern DevOps practices and cloud platforms."
    ),
    (
        "Linux, Terraform, Ansible, Azure, infrastructure as code, configuration management",
        "DevOps/Cloud Engineer",
        "Designs and manages cloud infrastructure using IaC tools for secure, repeatable, and efficient deployments."
    ),
    (
        "Data Analysis, Pandas, NumPy, Data Visualization, Statistics, EDA, insights generation",
        "Data Scientist",
        "Transforms raw data into meaningful insights and actionable decisions through analytical and statistical techniques."
    ),
    (
        "Node.js, React, MongoDB, Express.js, MERN stack, REST APIs, full-stack architecture",
        "Full Stack Developer",
        "Builds complete end-to-end web applications, handling both frontend and backend with scalable full-stack solutions."
    )
]
    df = pd.DataFrame(data, columns=["text", "category"])
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(n_jobs=-1))
    ])
    pipeline.fit(df['text'], df['category'])
    joblib.dump(pipeline, MODEL_PATH)

def predict(text):
    if not os.path.exists(MODEL_PATH): train_model()
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([text])[0]
    # Get highest probability (Confidence Score)
    confidence = max(model.predict_proba([text])[0])
    return prediction, round(confidence, 2)