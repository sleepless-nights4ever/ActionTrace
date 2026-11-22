const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { groups, validateInput, check, parse } = require('./check');
const data = name => JSON.parse(fs.readFileSync(path.join(__dirname, '../test-data', name + '.json')));
const inputs = data('inputs');
const labels = data('expected');
const runs = data('runs');
const iterations = data('iterations');
// Summaries are paraphrases. Human review checks their meaning; this
// reproducible comparison checks cardinality, owner, deadline and evidence.
function shape(result) {
  return groups.map(group => result[group].map(({ owner, deadline, source_lines, quote }) =>
    JSON.stringify({ owner, deadline, source_lines, quote })).sort());
}
function matches(actual, expected) {
  return JSON.stringify(shape(actual)) === JSON.stringify(shape(expected));
}
const scored = inputs.map(input => {
  const expected = labels.find(row => row.id === input.id).expected;
  const run = runs.find(row => row.id === input.id);
  try {
    validateInput(input);
  } catch (error) {
    return { id: input.id, result: expected === null && error.message === 'Enter a transcript.' ? 'Pass' : 'Fail', validation: error.message };
  }
  const actual = check(input, parse(JSON.stringify(run.verifier), true));
  return { id: input.id, result: matches(actual, expected) ? 'Pass' : 'Fail', actual };
});
const comparison = Object.fromEntries(Object.entries(iterations).map(([version, responses]) =>
  [version, Object.entries(responses).map(([id, output]) => ({
    id, passed: matches(output.verifier || output, labels.find(row => row.id === id).expected)
  }))]));
const adversarial = check(inputs[0], { decisions: [], flags: [], action_items: [
  {item:'Fake quote', owner:'Riya', deadline:'2026-10-16', source_lines:[1], quote:'Never said'},
  {item:'Poster', owner:'Dev', deadline:'2026-02-30', source_lines:[1], quote:"I'll send the draft poster by Friday."}
] });
assert.equal(adversarial.flags.length, 3);
assert.equal(adversarial.action_items.length, 1);
assert.equal(adversarial.action_items[0].owner, 'not stated');
assert.equal(adversarial.action_items[0].deadline, 'not stated');
assert.throws(() => parse('not JSON', true));
console.log(JSON.stringify({scored, comparison, adversarial}, null, 2));
