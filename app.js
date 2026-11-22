const byId = id => document.getElementById(id);
const { groups, validateInput, renderPrompt, parse, check } = ActionTrace;
const { inputs, runs, prompts } = actionTraceData;
let snapshot, finalResult;
const pretty = value => JSON.stringify(value, null, 2);
const notice = message => { byId('message').textContent = message; };
const show = (element, visible) => { byId(element).hidden = !visible; };

function currentInput() {
  return {
    meeting_date: byId('date').value,
    attendees: [...new Set(byId('attendees').value.split(',').map(name => name.trim()).filter(Boolean))],
    transcript: byId('transcript').value
  };
}

function add(parent, tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  parent.append(node);
  return node;
}

function display(result, origin) {
  finalResult = result;
  byId('download').disabled = !result;
  byId('origin').textContent = origin;
  const container = byId('results');
  container.replaceChildren();
  if (!result) return;
  for (const group of groups) {
    const label = group === 'decisions' ? 'Decisions' : 'Action items';
    add(container, 'h3', `${label} · ${result[group].length}`, 'tag');
    if (!result[group].length) add(container, 'p', 'None found.', 'hint');
    for (const row of result[group]) {
      const entry = add(container, 'article', '');
      add(entry, 'strong', row.item);
      add(entry, 'p', `Owner: ${row.owner} · Deadline: ${row.deadline} · Lines: ${row.source_lines.join(', ')}`);
      add(entry, 'blockquote', row.quote);
    }
  }
  add(container, 'h3', `Verification flags · ${result.flags.length}`, 'tag');
  for (const flag of result.flags) add(container, 'p', `${flag.item}: ${flag.reason}`, 'flag');
}

function reset() {
  snapshot = undefined;
  show('workflow', false);
  notice('');
  display(null, 'Run both prompts or replay a saved test case.');
}

function sample() {
  const input = inputs.find(item => item.id === byId('sample').value);
  byId('date').value = input.meeting_date;
  byId('attendees').value = input.attendees.join(', ');
  byId('transcript').value = input.transcript;
  reset();
  return input;
}

function handle(action) {
  return event => {
    event.preventDefault();
    notice('');
    try { action(); } catch (error) { notice(error.message); }
  };
}

for (const input of inputs) {
  const option = add(byId('sample'), 'option', `${input.id} · ${input.label}`);
  option.value = input.id;
}
byId('load').onclick = handle(sample);
byId('replay').onclick = handle(() => {
  const input = validateInput(sample());
  const run = runs.find(entry => entry.id === input.id);
  display(check(input, run.verifier), `${input.id} · Saved ChatGPT responses replayed through local checks`);
});
byId('meeting').addEventListener('input', reset);
byId('meeting').onsubmit = handle(() => {
  reset();
  snapshot = validateInput(currentInput());
  byId('p1').value = renderPrompt(prompts.P1, snapshot);
  byId('draft').value = '';
  byId('audit').value = '';
  show('audit-step', false);
  show('workflow', true);
  byId('workflow').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
byId('draft').addEventListener('input', () => { show('audit-step', false); byId('audit').value = ''; display(null, 'Rebuild the verification prompt after editing the extraction JSON.'); });
byId('audit').addEventListener('input', () => display(null, 'Check the verification response to refresh results.'));
byId('verify').onclick = handle(() => {
  const draft = parse(byId('draft').value, false);
  byId('p2').value = renderPrompt(prompts.P2, snapshot, draft);
  show('audit-step', true);
  byId('p2').focus();
});
byId('apply').onclick = handle(() => {
  display(check(snapshot, parse(byId('audit').value, true)), 'Pasted verification response checked against the transcript');
  byId('review-title').scrollIntoView({behavior:'smooth',block:'center'});
});
document.querySelectorAll('[data-copy]').forEach(button => {
  button.onclick = async () => {
    const field = byId(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(field.value);
      const label = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = label; }, 800);
    } catch {
      field.focus();
      field.select();
    }
  };
});
byId('download').onclick = () => {
  const link = document.createElement('a');
  const url = URL.createObjectURL(new Blob([pretty(finalResult)], { type: 'application/json' }));
  link.href = url;
  link.download = 'actiontrace-results.json';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
