import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "model.pkl"

def train_model():
    print("Training Classifier Model...")
    
    # Synthetic Data (Fixed: Combined Skills + Description into one Text field)
    # Format: (Text, Category)
    data = [
        (
            "Python, Django, Flask, REST API development, SQL & relational databases, backend architecture, authentication, performance optimization. Experienced in building secure, scalable, and high-performance backend systems using Python frameworks and database-driven architectures.",
            "Software Engineer"
        ),
        (
            "Java, Spring Boot, Microservices architecture, OOP principles, RESTful services, system design, scalability. Specialized in enterprise-grade Java applications with clean object-oriented design and distributed microservices systems.",
            "Software Engineer"
        ),
        (
            "React.js, JavaScript, HTML5, CSS3, UI/UX design, responsive layouts, component-based architecture. Focused on creating interactive, user-friendly, and visually appealing web interfaces with modern frontend technologies.",
            "Web Developer"
        ),
        (
            "Next.js, Tailwind CSS, Redux, responsive design, SSR, performance optimization. Builds fast, SEO-friendly, and scalable web applications with modern React frameworks and state management.",
            "Web Developer"
        ),
        (
            "Machine Learning, PyTorch, TensorFlow, AI models, Deep Learning, model training & evaluation. Develops intelligent systems and predictive models using state-of-the-art deep learning frameworks and techniques.",
            "AI/ML Engineer"
        ),
        (
            "Natural Language Processing, Computer Vision, Data Science, feature engineering, model deployment. Experienced in extracting insights from text, image, and structured data using advanced AI and data science methods.",
            "AI/ML Engineer"
        ),
        (
            "Jenkins, Docker, Kubernetes, AWS, CI/CD pipelines, cloud infrastructure, automation. Ensures reliable deployment, scalability, and automation of applications through modern DevOps practices and cloud platforms.",
            "DevOps/Cloud Engineer"
        ),
        (
            "Linux, Terraform, Ansible, Azure, infrastructure as code, configuration management. Designs and manages cloud infrastructure using IaC tools for secure, repeatable, and efficient deployments.",
            "DevOps/Cloud Engineer"
        ),
        (
            "Data Analysis, Pandas, NumPy, Data Visualization, Statistics, EDA, insights generation. Transforms raw data into meaningful insights and actionable decisions through analytical and statistical techniques.",
            "Data Scientist"
        ),
        (
            "Node.js, React, MongoDB, Express.js, MERN stack, REST APIs, full-stack architecture. Builds complete end-to-end web applications, handling both frontend and backend with scalable full-stack solutions.",
            "FullStack Developer"
        )
    ]
    
    # Now creates DataFrame correctly with 2 columns
    df = pd.DataFrame(data, columns=["text", "category"])
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(n_jobs=1)) # n_jobs=1 ensures stability
    ])
    
    pipeline.fit(df['text'], df['category'])
    joblib.dump(pipeline, MODEL_PATH)
    print("Model trained successfully.")

def predict(text):
    if not os.path.exists(MODEL_PATH):
        train_model()
    
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([text])[0]
    # Get highest probability (Confidence Score)
    confidence = max(model.predict_proba([text])[0])
    
    return prediction, round(confidence, 2)