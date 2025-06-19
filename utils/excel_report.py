import os
import pandas as pd
from datetime import datetime

def export_to_excel(results, output_folder="outputs"):
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f"Resume_Score_Report_{timestamp}.xlsx"
    output_path = os.path.join(output_folder, filename)

    # Prepare data
    rows = []
    for r in results:
        rows.append({
            "Generated At": timestamp,
            "Candidate Name": r['name'],
            "Email": r['email'],
            "Phone": r['phone'],
            "Resume File": r['filename'],
            "Overall Score": r['overall'],
            "Similarity Score": r['similarity'],
            "Mandatory Skill Score": r['mand_score'],
            "Mandatory Present": ", ".join(r['mand_present']) if isinstance(r['mand_present'], list) else r['mand_present'],
            "Mandatory Missing": ", ".join(r['mand_missing']) if isinstance(r['mand_missing'], list) else r['mand_missing'],
            "Must-have Skill Score": r['must_score'],
            "Must-have Present": ", ".join(r['must_present']) if isinstance(r['must_present'], list) else r['must_present'],
            "Must-have Missing": ", ".join(r['must_missing']) if isinstance(r['must_missing'], list) else r['must_missing'],
            "Top Missing JD Keywords": ", ".join(r['top_missing']) if isinstance(r['top_missing'], list) else r['top_missing']
        })

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    print(f"✅ Excel report saved at: {output_path}")
    return filename  # for linking in UI
