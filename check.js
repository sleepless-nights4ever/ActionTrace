(function (root) {
  const groups = ['decisions', 'action_items'];
  const missing = 'not stated';
  function validDate(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const date = new Date(value);
    return Number.isFinite(+date) && date.toISOString().slice(0, 10) === value;
  }
  function linesOf(value) {
    return value.split(/\r?\n/).map(line => line.trim()).filter(Boolean)
      .map(line => line.replace(/^\[\d+\]\s*/, ''));
  }
  function validateInput(input) {
    if (!validDate(input.meeting_date)) throw Error('Enter a valid meeting date.');
    if (!input.attendees.length) throw Error('Enter at least one attendee.');
    if (!linesOf(input.transcript).length) throw Error('Enter a transcript.');
    return input;
  }
  function renderPrompt(template, input, draft) {
    const values = {
      meeting_date: input.meeting_date,
      attendees: input.attendees.join(', '),
      transcript: linesOf(input.transcript).map((line, i) => `[${i+1}] ${line}`).join('\n'),
      draft_json: JSON.stringify(draft, null, 2)
    };
    return template.replace(/\{(meeting_date|attendees|transcript|draft_json)\}/g, (_, key) => values[key]);
  }
  function parse(value, verified) {
    const normalized = value.trim().replace(/^```(?:json)?\s*([\s\S]*?)\s*```$/i, '$1');
    const result = JSON.parse(normalized);
    if (!result || groups.some(group => !Array.isArray(result[group]))) {
      throw Error('JSON must contain decisions and action_items arrays.');
    }
    if (verified && (!Array.isArray(result.flags) || result.flags.some(flag =>
      !flag || typeof flag.item !== 'string' || typeof flag.reason !== 'string'))) {
      throw Error('Verifier JSON must contain a flags array with item and reason fields.');
    }
    return result;
  }
  function check(input, result) {
    const lines = linesOf(input.transcript);
    const checked = { decisions: [], action_items: [], flags: [...result.flags] };
    for (const group of groups) {
      for (const row of result[group]) {
        const item = typeof row?.item === 'string' ? row.item : 'Unnamed row';
        const validLines = Array.isArray(row?.source_lines) && row.source_lines.length &&
          row.source_lines.every(n => Number.isInteger(n) && n >= 1 && n <= lines.length);
        if (!item.trim() || typeof row?.item !== 'string' || !validLines ||
          typeof row.quote !== 'string' || !row.quote.trim() ||
          !row.source_lines.some(n => lines[n - 1].includes(row.quote))) {
          checked.flags.push({ item, reason: 'Removed because its evidence fields or verbatim quote failed validation.' });
          continue;
        }
        let { owner, deadline } = row;
        if (owner !== missing && !input.attendees.includes(owner)) {
          checked.flags.push({ item, reason: 'Owner replaced because it did not exactly match an attendee.' });
          owner = missing;
        }
        if (deadline !== missing && !validDate(deadline)) {
          checked.flags.push({ item, reason: 'Deadline replaced because it was not a valid ISO date.' });
          deadline = missing;
        }
        checked[group].push({ item, owner, deadline, source_lines: [...new Set(row.source_lines)], quote: row.quote });
      }
    }
    return checked;
  }
  const api = { groups, validateInput, renderPrompt, parse, check };
  if (typeof module === 'object') module.exports = api;
  else root.ActionTrace = api;
})(globalThis);
