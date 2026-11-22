# ActionTrace

ActionTrace turns a meeting transcript into decisions and action items, with a supporting quote, cited line numbers, owner, and deadline. Missing fields show `not stated`.

## Open and run

1. Extract the project and open `code/index.html` in Chrome or Edge.
2. Choose T01 and click **Replay saved run** for the course example. Choose T11 for a verifier repair and T12 for input rejection.
3. For a new meeting, enter the date, attendee names, and transcript. Put each speaking turn on its own line.
4. Click **Build extraction prompt**. Copy it to ChatGPT, paste the JSON reply into the app, and build the verification prompt.
5. Send the verification prompt to ChatGPT, preferably in a fresh chat. Paste the response and click **Check and show results**, then **Download JSON**.

The interface runs locally without a key or server. Custom transcripts require two manual ChatGPT turns. Saved runs replay previously generated outputs through live validation and display. Only share synthetic or consented, anonymised transcripts with a model.

## Project structure

- `prompts/` contains three versions and the two final prompt sheets' source text.
- `code/` contains the browser app and evaluator.
- `test-data/` contains inputs, reference labels, project-session responses, and scores.
- `docs/` contains diagrams, run evidence, the report, and the reel.
- `CHANGELOG.md` records progress since Milestone 1.

To reproduce structural scores, run `node code/evaluate.js` from this folder. This reruns checks on recorded JSON. It does not send new requests or calculate semantic similarity.

## Course submission

Team name, members, and contributions await confirmation. Refer to the submission checklist in `docs/` for URLs and form entries.
