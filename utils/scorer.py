from utils.matcher import (
    precompute_jd_vector,
    compute_similarity,
    match_skills,
    top_missing_keywords
)

def compute_scores(jd_text, resumes, mandatory_skills, must_have_skills):
    results = []
    vectorizer, jd_vec = precompute_jd_vector(jd_text)

    for idx, res in enumerate(resumes, 1):
        print(f"🔍 Scoring resume {idx}: {res['filename']}")

        sim_score = compute_similarity(vectorizer, jd_vec, res['text'])

        mand_score, mand_present, mand_missing = match_skills(res['text'], mandatory_skills)
        must_score, must_present, must_missing = match_skills(res['text'], must_have_skills)
        overall = round(0.4 * mand_score + 0.3 * must_score + 0.3 * sim_score, 2)

        # Clean presentation
        mand_present = mand_present or "N/A"
        mand_missing = mand_missing or "N/A"
        must_present = must_present or "N/A"
        must_missing = must_missing or "N/A"
        missing_keywords = top_missing_keywords(jd_text, res['text'])

        results.append({
            'filename': res['filename'],
            'name': res['name'],
            'email': res['email'],
            'phone': res['phone'],
            'overall': overall,
            'similarity': sim_score,
            'mand_score': mand_score,
            'mand_present': mand_present,
            'mand_missing': mand_missing,
            'must_score': must_score,
            'must_present': must_present,
            'must_missing': must_missing,
            'top_missing': missing_keywords or ["N/A"]
        })

    return results
