# SCSE4041 Milestone 2 submission checklist

**Work to confirm before submitting.** Use the Milestone 1 Team ID and exactly the same team name. Confirm the batch, faculty, leader, names, enrollments, and evidence-based contribution split with your team. Update `docs/submission-details.json` and run `python docs/build_reports.py` from the project root (requires `pip install reportlab`). This regenerates both PDFs with the confirmed team filenames and identical supporting text. Use filename-safe team name and ID strings. The current placeholder files should be replaced by the newly generated PDFs.

| Form field | Entry |
| --- | --- |
| Q1–Q7 | Confirmed Milestone 1 team details. Enter member enrollment numbers one per line. |
| Q8 | Choose the form option closest to prompt-engineered web application. |
| Q9 | ChatGPT, default settings. Exact model identifier was unavailable in the project session. |
| Q10 | 2 |
| Q11 | Evaluator-accessible prototype link. The deployed owner-private preview alone is insufficient. |
| Q12 | Public GitHub repository or an anyone-with-link Drive / OneDrive project folder. Upload the extracted project structure. |
| Q13 | Anyone-with-link Drive video or unlisted YouTube reel URL. |
| Q14 | 110 seconds for the included captioned reel. If you replace it with a continuous recording, enter its exact duration. |
| Q15 | Technical report |
| Q16 | `TeamName_TechnicalReport.pdf`, with the confirmed team name. |
| Q17 | 12 test inputs |
| Q18 | 3 prompt versions |
| Q19 | All modules working in the documented manual model workflow |
| Q20 | Copy the working module list below, one per line. |
| Q21 | `M2_TeamID_ActionTrace.pdf`, with the confirmed Team ID. |
| Q22 | One member per line, enrollment – name – main task. Match Section 7. |
| Q23 | Try T01 and T11 via replay. New transcripts use two manual ChatGPT prompts; no shared password or API key is required. |
| Q24 | Tick after all members agree to the contribution table. |

## Working modules

Meeting input  
Prompt generation  
ChatGPT extraction and audit  
Evidence and JSON checks  
Results and export

## Link checks and hand-in

- Put the three checked URLs in `docs/submission-details.json` before regenerating the report. If you use the Colab fallback, upload `code/ActionTrace_Colab.ipynb` and share the notebook with its output saved.
- Test each exact URL in incognito. Check both PDF names and sizes. Both files must be at most 10 MB.
- The included reel has captions over consecutive browser captures of real actions and recorded JSON. If your faculty requires continuous screen footage, record the same steps from the prototype and match the included reel timing. A suggested sequence is 10 seconds for the problem, 33 seconds for the prompt experiment, 51 seconds for the demo and 16 seconds for progress and next steps.
- The team leader submits once and checks the confirmation. The guide states the deadline is 22 November 2026 at 11:59 PM.
