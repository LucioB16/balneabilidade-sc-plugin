# Balneabilidade SC — reviewer video walkthrough

This is the **recording script**, not a claim that a video was produced.
The public MCP server has been validated directly, but only a real
ChatGPT session can demonstrate prompt-to-tool selection and refusal behavior.
A reviewer-accessible **recording URL is mandatory** for the initial MCP
review; see https://developers.openai.com/plugins/deploy/submission.

## Before recording

1. Start a **new ChatGPT conversation** and select the existing private
   **Balneabilidade SC** plugin with the \`@\` menu. Confirm its connection
   is active and exposes the five named MCP tools.
2. Open the official IMA/SC source page only when needed:
   https://balneabilidade.ima.sc.gov.br/
3. Record the screen in Windows 11 using a screen recorder (for example,
   Windows Snipping Tool's screen-record option). Keep tool-call details
   visible when possible, and record the assistant's final answers.
4. Do not expose authentication cookies, account identifiers, inbox,
   unrelated personal data, service admin panels, or secret settings.
5. Use exactly the prompts in \`plugin/plugin.json\` for all **five
   positive** and **three negative** initial-review cases. Fresh results
   may differ from the 2026-11-13 bulletin in the dated evidence.
6. Avoid describing sample results as "real-time", endorsing swimming
   safety, or claiming affiliation with IMA/SC.

## Recording sequence

### A. Five positive review prompts

**P1 — Alias and source** (es-AR):

> ¿Está apta para bañarse Praia do Perequê, en Porto Belo?

Verify the agent uses a broad **Perequê** search to resolve **Praia de
Perequê**, then reads point-specific dated status; includes the dates and
source and does not silently misidentify the beach. Show that the sampled
water results may be different at different locations.

**P2 — A partly improper beach** (es-AR):

> ¿Qué puntos de Praia Brava, en Florianópolis, están impropios?

Verify only returned improper sampling points are listed, with their
specific locations and dates, without labeling the entire beach identically.
The dated 2026-11-13 source had one improper point; future readings may vary.

**P3 — Complete historical data** (es-AR):

> Mostrame el historial de balneabilidad de Campeche durante 2025, en Florianópolis.

Verify search resolves **Praia do Campeche** and the history call uses
the full inclusive range \`2025-01-01\` to \`2025-12-31\`.
For a *complete-year* request, the model must paginate until
\`next_cursor\` is empty. The 2026-11-17 tool check returned 145 records
across 3 pages. Include dated historical findings without inventing entries.

**P4 — Portuguese support** (pt-BR):

> Qual é a condição atual da Praia de Zimbros, em Bombinhas?

Verify answer in Portuguese, with separate sample dates and official
bulletin date. **Atual** must not be misrepresented as a real-time reading.

**P5 — English support** (en):

> What is the latest published result for Praia de Garopaba, in Garopaba?

Verify the agent searches/resolves the beach and reports every sampled
point conservatively in English, with source and dates.

### B. Two other important MCP capabilities

These are additional demonstrations, **not** extra review cases:

- In the same plugin conversation, request **sampling-point locations**
  for Praia de Perequê in Porto Belo to demonstrate
  \`get_sampling_points\`.
- Request **page 1 of the latest official bulletin**, with its date, to
  demonstrate \`get_bulletin_page\`, including visual content.
  Rendered pages are source images, not model-invented table rows.

### C. Three negative review prompts

Use a **new conversation for each** if previous tool calls could
prime activation. Record both the model answer and whether a tool was
called.

**N1 — Out of geographic scope** (pt-BR):

> Qual é a balneabilidade da Praia Grande em Ubatuba, São Paulo?

Pass only if the answer clearly limits the plugin to beaches monitored in
Santa Catarina and **does not invoke an MCP tool**.

**N2 — Wave forecast not available** (es-AR):

> ¿Qué altura tendrán las olas mañana en Itapoá?

Pass only if the assistant clarifies this is not a wave-height or
weather-forecast service and **does not invoke an MCP tool**.

**N3 — Facilities not provided** (en):

> Is there free parking and a public shower at Praia do Perequê in Porto Belo?

Pass only if the assistant refrains from inventing parking/shower
information and **does not invoke an MCP tool**.

## After recording

For each P1–P5 and N1–N3, document actual selected tool names, input
arguments, final user-visible answer, whether dates/municipality were
correct, whether any content was fabricated, and PASS/FAIL. Save any
discoveries in \`docs/REVIEW_VALIDATION.md\` or a follow-up issue.

Upload an actual capture to a reviewer-accessible destination, such as a
view-only Google Drive file configured for **anyone with the link**.
Test its accessibility in an incognito window. **Never fabricate a video
URL or claim the video exists before it has been uploaded.**

Once the recording exists, populate \`demo_recording_url\` in the ignored
submission metadata file (do not commit any private reviewer credentials).
The legal pages, identity and host acceptable-use review are separate
publication prerequisites.
