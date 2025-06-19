from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def precompute_jd_vector(jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    jd_vec = vectorizer.fit_transform([jd_text])
    return vectorizer, jd_vec[0]

def compute_similarity(vectorizer, jd_vec, resume_text):
    try:
        resume_vec = vectorizer.transform([resume_text])
        score = cosine_similarity(jd_vec, resume_vec)[0][0]
        return round(score * 100, 2)
    except Exception as e:
        print(f"❌ TF-IDF similarity error: {e}")
        return 0.0

def match_skills(text, skills):
    text_lower = text.lower()
    present = [skill for skill in skills if skill.lower() in text_lower]
    missing = list(set(skills) - set(present))
    score = round((len(present) / len(skills)) * 100, 2) if skills else 0.0
    return score, present, missing

def top_missing_keywords(jd_text, resume_text, top_n=30):
    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())
    missing_words = list(jd_words - resume_words)
    return sorted(missing_words, key=lambda w: len(w), reverse=True)[:top_n]
