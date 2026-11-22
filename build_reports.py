"""Generate both SCSE4041 PDFs. Requires Python and reportlab."""
import json
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image, Preformatted
from reportlab.lib.utils import ImageReader

docs=Path(__file__).resolve().parent
root=docs.parent
details=json.loads((docs/'submission-details.json').read_text())
load=lambda name: json.loads((root/'test-data'/f'{name}.json').read_text())
inputs, runs, analyses=load('inputs'), load('runs'), load('scored')
screen_link='https://actiontrace-meeting-workflow.sillycomet6.chatgpt.site/'
title='ActionTrace: A Prompt Workflow that Turns Meeting Transcripts into Verified Action Items'
blue=colors.HexColor('#1d3b84')
navy=colors.HexColor('#172648')
pale=colors.HexColor('#eef3fe')
gray=colors.HexColor('#4d5c75')
styles=getSampleStyleSheet()
styles['Normal'].fontSize=10.5
styles['Normal'].leading=15
styles['Normal'].textColor=navy
styles['Normal'].spaceAfter=8
for n,size in [('Heading1',22),('Heading2',14),('Heading3',11)]:
    styles[n].fontSize=size
    styles[n].leading=size*1.25
    styles[n].textColor=blue
styles.add(ParagraphStyle(name='Cover',parent=styles['Normal'],fontSize=31,leading=36,spaceAfter=18,fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Small',parent=styles['Normal'],fontSize=8.8,leading=12,spaceAfter=0))
styles.add(ParagraphStyle(name='White',parent=styles['Small'],textColor=colors.white,fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='CodeLine',parent=styles['Normal'],fontName='Courier',fontSize=7.3,leading=8.4,spaceAfter=0,splitLongWords=True))
styles.add(ParagraphStyle(name='Caption',parent=styles['Small'],textColor=gray,spaceAfter=10))
W=A4[0]-84

def p(text,kind='Normal'):
    return Paragraph(escape(str(text)).replace('\n','<br/>'),styles[kind])
def heading(text): return p(text,'Heading1')
def sub(text): return p(text,'Heading2')
def minor(text): return p(text,'Heading3')
def code_block(text):
    return [p(line if line else ' ','CodeLine') if line else Spacer(1,7) for line in text.rstrip().splitlines()]+[Spacer(1,8)]
def table(headers,rows,widths):
    t=Table([[p(h,'White') for h in headers]]+[[p(v,'Small') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,pale]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#d3def3'))]))
    return t
def figure(filename,caption,maxh=300):
    path=docs/filename
    w,h=ImageReader(str(path)).getSize()
    factor=min(W/w,maxh/h)
    im=Image(str(path),width=w*factor,height=h*factor,hAlign='LEFT')
    return [im,p(caption,'Caption')]
def link(label,url):
    return Paragraph(f'<b>{escape(label)}</b> &nbsp; <link href="{escape(url,quote=True)}" color="#1d3b84">{escape(url)}</link>',styles['Normal'])
def page(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d3def3'))
    canvas.line(42,40,A4[0]-42,40)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(gray)
    canvas.drawString(42,26,'SCSE4041  /  ACTIONTRACE  /  MILESTONE 2')
    canvas.drawRightString(A4[0]-42,26,str(doc.page))
def write(name,body):
    SimpleDocTemplate(str(docs/name),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=35,bottomMargin=54,title=title).build(body,onFirstPage=page,onLaterPages=page)

modules=[
('Meeting input','Capture meeting date, attendees and transcript','Working','Rejects a blank transcript.'),
('Prompt generation','Number transcript lines and build P1 and P2','Working','P2 accepts extraction JSON as a candidate draft.'),
('ChatGPT extraction and audit','Run both prompt steps through ChatGPT','Working','Manual copy and paste. Recorded responses are available for replay.'),
('Evidence and JSON checks','Check arrays, evidence quotes, owner membership and date format','Working','Semantic checks are handled by P2.'),
('Results and export','Show decisions, actions and flags and download JSON','Working','Replay works without external credentials.')]
limitations=[
('Manual model steps','Automate the two requests through a server with credentials stored server-side.'),
('Verifier can repeat extraction errors','Run P2 in independent sessions and test extra multi-turn evidence cases.'),
('Single small synthetic dataset','Add more fictional club and project cases, use two reviewers, and compare fresh runs across models.'),
('Evidence checks are structural','Evaluate harder paraphrases, add date-evidence tests, and flag suspicious claims even when their quote is real.')]
paired=[
('v1','Milestone 1 role and JSON format','Establish a baseline','1/2 field comparisons matched. T01 decision lacked owner, deadline and quote fields.'),
('v2','Unified row schema and verbatim evidence','Apply evidence rules to both output types','2/2 matched. The T01 budget decision had the required evidence fields.'),
('v3 / final','Two worked examples, explicit correction and deadline rules, independent audit step in the workflow','Handle harder cases and expose repairs','2/2 paired cases matched. Across the full set, T11 audit added a missing evidence line.')]
case_details=[
('Poster, hall and budget','1 decision, 2 actions. Riya due 16 Oct. Hall owner and due date unstated.','1 decision, 2 actions. Riya due 16 Oct, hall missing fields retained.'),
('Room and email tomorrow','1 room decision. Aman emails on 13 Oct.','Lab 2 and Aman email due 13 Oct.'),
('Karan assigned slides','Karan uploads slides on 20 Oct.','Karan, 20 Oct, lines 1 and 2.'),
('Badges and lanyards','Riya due 14 Oct, Karan due 15 Oct.','Both owners and due dates matched.'),
('Logo and free registration','2 decisions. Ownership and dates unstated.','2 decisions with both missing fields retained.'),
('Owner and date correction','Aman replaces Riya, now due 15 Oct.','Aman, 15 Oct, lines 2 and 3.'),
('Dev and vague timing','Print agenda with both fields unstated.','Dev excluded because absent from attendee list. Date unstated.'),
('Pizza and canceled bus','No decisions or actions.','Both arrays empty.'),
('Embedded instruction','Only Karan checklist, due 13 Oct.','Only Karan checklist, due 13 Oct.'),
('Event Friday, photos soon','Aman uploads photos, date unstated.','Aman, date unstated. No date borrowed from showcase.'),
('Duration after assets','Riya prepares draft with dates unstated. Cite lines 2 and 3.','Date unstated. P2 added line 2 and flagged the repair.'),
('Blank input','Reject before prompting.','Enter a transcript.')]
def supporting():
    return [
        sub('ActionTrace technical report'),
        p('ActionTrace helps student clubs and project teams turn meeting transcripts into traceable decisions and follow-up commitments. It returns separate decision and action arrays with a summary, owner, deadline, supporting line numbers and a verbatim quote.'),
        minor('Architecture and tools'),
        p('The prototype uses HTML, CSS and JavaScript. The browser validates input and prepares prompts. ChatGPT generates extraction and audit JSON through a manual copy/paste workflow. The browser checks quote membership, line ranges, attendee names and ISO date syntax, renders reviewed results and downloads JSON. The demo cases run offline using saved responses.'),
        minor('Prompt design'),
        p('P1 uses a fixed JSON schema and two examples. It excludes speculative or canceled work and assigns an owner only when stated. P2 rechecks the draft against the whole transcript, recomputes supported deadlines, and returns explanations for repairs. A missing owner or date is expressed as “not stated.”'),
        minor('Evaluation'),
        p('The evaluation used 12 fictional inputs: five normal, six edge and one invalid. All 11 valid cases matched reference counts, owner, deadline and cited fields after auditing, and the empty transcript was rejected. The paired field comparison on T01 and T06 was 1/2 for v1, then 2/2 for v2 and v3. T11 gained a supporting line in the audit. These results use recorded ChatGPT responses generated in one project session and replayed through browser checks.'),
        minor('Limitations'),
        p('The test set is small and synthetic. The model was evaluated in one project session with no controlled temperature or cross-model comparison. Local checks do not verify semantic entailment. A future evaluation should run each case in fresh sessions, compare models, and collect independent judgments for paraphrases and omissions.')]
def compact_json(value):
    lines = ['{']
    for index, (key, rows) in enumerate(value.items()):
        lines.append(f'  "{key}": [')
        lines.extend('    '+json.dumps(row)+(',' if i+1 < len(rows) else '') for i,row in enumerate(rows))
        lines.append('  ]'+(',' if index+1 < len(value) else ''))
    return '\n'.join(lines+['}'])

def prompt_sheet(key,name,step,purpose,num,example_id,example):
    case=inputs[0]
    raw=case['transcript'].splitlines()
    text=(root/'prompts/final'/f'{key}.txt').read_text()
    content=[
        sub(f'{key} · {name}'),
        p(f'Step {step}. {purpose}'),
        p('Tool and model: ChatGPT in the project session. Exact model identifier not exposed. Settings: default. System prompt: none supplied.'),
        p(f'Examples included: {num}. Output: JSON with decisions and action_items arrays'+(' plus flags.' if key=='P2' else '.')),
        p('Variables: {meeting_date} is the ISO meeting date. {attendees} is the comma-separated roster. {transcript} contains numbered turns.'+
          (' {draft_json} is the candidate JSON from P1.' if key=='P2' else '')),
        minor('Full user prompt template'),*code_block(text),
        minor(f'Sample run · {example_id}'),
        p('Meeting date: 2026-10-12. Attendees: Riya, Aman, Karan.'),
        *code_block('\n'.join(f'[{i}] {line}' for i,line in enumerate(raw,1))),
    ]
    if key=='P2':
        content.extend([p('Candidate JSON supplied to P2'),*code_block(compact_json(runs[0]['extractor']))])
    content.extend([p('Recorded ChatGPT output'),*code_block(compact_json(example))])
    return content

body=[heading('1. Cover page'),Spacer(1,42),p('ActionTrace','Cover'),p('A Prompt Workflow that Turns Meeting Transcripts into Verified Action Items','Heading2'),Spacer(1,10),p('SCSE4041 Mini Project · Milestone 2 · 22 November 2026')]
members=details['members']
cover=[('Team ID',details['team_id']),('Team name',details['team_name']),('Batch',details['batch'] or 'Pending team confirmation'),('Faculty',details['faculty'] or 'Pending team confirmation'),('Team leader',details['leader'] or 'Pending team confirmation'),('Members','; '.join(f"{m['name']} ({m['enrollment']})" for m in members) or 'Pending names and enrollment numbers')]
body += [table(['Field','Details'],cover,[120,W-120]),Spacer(1,15)]
for label,key in [('Evaluator prototype','reviewed_prototype_url'),('Repository or project folder','repository_url'),('Reel','reel_url')]:
    body.append(link(label,details[key]) if details[key] else p(label+' — evaluator-accessible link pending'))
if not details['reviewed_prototype_url']:
    body.append(link('Private prototype preview',screen_link))
body += [p('Submission status: verify team details and evaluator access before filing the form.') if not (members and all(details[k] for k in ('reviewed_prototype_url','repository_url','reel_url'))) else p('Prototype, repository and reel links are listed above.'),PageBreak(),
         heading('2. Prompt and solution design'),
         p('Weekly club and student project meetings often finish without an accessible record of decisions and follow-ups. Coordinators may have to chase action owners or reconstruct notes later. Team members need to know what was agreed, who committed, and when the work is due. Each result therefore links back to transcript evidence. Techloy identifies follow-up ownership as a post-meeting workflow gap.'),
         p('The inputs are a transcript, a meeting date, and an attendee list. The browser numbers speaking turns. P1 produces candidate decisions and actions and explicitly marks missing owners and deadlines. P2 audits both arrays against the full transcript, repairs unsupported fields or removes unsupported items, and returns flags. The browser checks structure and literal evidence before rendering or exporting the final JSON.'),
         p('ChatGPT was used because it accepts instructions and worked examples and can return structured text. The web prototype makes the two prompts visible. The milestone preserves the baseline, upgrades the decision schema to match the action schema, adds examples for cancellations and uncertainty, and adds verification and test evidence. The choice to split drafting and review is informed by work on Chain-of-Verification.'),
         link('Techloy (2026), partner-content article','https://www.techloy.com/from-meeting-recording-to-finished-deck-the-workflow-gap-most-teams-dont-realize-they-have/'),
         link('Dhuliawala et al. (2024), Findings of ACL','https://aclanthology.org/2024.findings-acl.212/')]
for name,label in [('prompt-workflow','Prompt workflow'),('task-decomposition','Task decomposition'),('input-output','Input-output flow'),('architecture','System architecture')]:
    body.extend(figure(name+'.png',label,110))
body += [PageBreak(),*prompt_sheet('P1','Extract candidates',1,'Produce evidence-backed decision and action candidates.',2,'T01',runs[0]['extractor']),
         PageBreak(),*prompt_sheet('P2','Audit evidence',2,'Check and repair extraction against the transcript.',0,'T01',runs[0]['verifier']),
         PageBreak(),heading('3. Implementation'),
         p('The working prototype captures meeting details, constructs both prompts, parses responses, checks evidence, and exports the final JSON. The model turns run in ChatGPT through a manual handoff. The app also includes a replay mode for the recorded examples.'),
         table(['Module','What it does','Status','Notes'],modules,[116,154,57,W-327]),Spacer(1,14),
         sub('Prompt iteration log'),
         table(['Version','What changed','Why','Observed result'],paired,[68,154,122,W-344]),Spacer(1,10),
         p('All three saved versions were compared on T01 and T06. The paired metric compares output counts and field evidence, accepting the baseline task/text field name. See the full testing criteria in Section 4.'),
         PageBreak(),sub('Full prompt versions')]
for version in ('v1','v2','v3'):
    for f in sorted((root/'prompts'/version).glob('*.txt')):
        body.extend([minor(f'{version} · {f.stem}'),*code_block(f.read_text())])
body += [PageBreak(),heading('4. Demonstration and testing'),
         p('The fictional test set was labelled separately from the response files. ChatGPT responses were captured in one project-building session. Browser checks and the Node evaluator replay the saved JSON. The evaluator compares result counts, owners, deadlines and cited lines/quotes. Item summaries were reviewed by meaning. T12 tests validation before any model step.'),
         table(['Test','Input','Type','Expected output','Actual output','Result'],[[i['id'],d[0],i['type'],d[1],d[2],s['result']] for i,d,s in zip(inputs,case_details,analyses['scored'])],[39,89,48,129,159,W-464]),Spacer(1,10)]
body += [p('Observed: 12/12 passed on replay, including six edge inputs and one invalid input. One direct validator challenge also removed an invented quote and rejected an invalid date and an out-of-roster owner.'),
         PageBreak(),heading('Run evidence')]
for name,caption in [('T01-result','T01. Both pasted responses were processed and rendered. The poster result shows Riya, 16 October, and a verbatim quote.'),('T11-result','T11. The saved verifier response is replayed through the local validator. The repair appears as a flag and the deadline remains unstated.')]:
    body.extend(figure(name+'.jpg',caption,185))
body += [sub('Known limitations and next steps'),table(['Limitation','Next step'],limitations,[174,W-174]),PageBreak(),heading('5. Repository')]
if details['repository_url']: body.append(link('Repository',details['repository_url']))
body += [*figure('folder.jpg','Repository folder evidence. Browser rendering of the actual local project tree during build.',325),
         p('The project now separates v1, v2, v3 and the final prompts.'),
         p('The browser app, checks and scoring script are in code/.'),
         p('The fictional inputs, reference labels and recorded model responses are in test-data/.'),
         p('The dated changelog, diagrams and submission documents show the Milestone 2 additions.'),PageBreak(),heading('6. Supporting document'),*supporting(),PageBreak(),heading('7. Team contribution'),
         p('Record each member’s actual role, work and evidence. All members must agree to the table and percentages must total 100%.'),
         table(['Member name','Enrollment no.','Role','Tasks done in Milestone 2','Evidence','Contribution (%)'],[[m[k] for k in ('name','enrollment','role','task','evidence','contribution')] for m in members] or [['Pending','Pending','Pending','Pending team confirmation','Pending','Pending']],[77,78,67,113,105,W-440])]
write(f"M2_{details['team_id']}_ActionTrace.pdf",body)
write(f"{details['team_name']}_TechnicalReport.pdf",[heading('Supporting document'),*supporting()])
