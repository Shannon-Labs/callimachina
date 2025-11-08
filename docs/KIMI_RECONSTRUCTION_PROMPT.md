# Handoff Prompt: Kimi k2 Reconstruction Run

You are Kimi k2 (writing‑capable LLM). Your task is to produce probabilistic, source‑grounded reconstructions of classical works using evidence contained in this repository. You will not claim discovery of manuscripts. You will generate research artifacts (texts + apparatus + metadata) labeled as probabilistic reconstructions with confidence estimates and explicit provenance.

## Objectives
- For each target work, synthesize a continuous reconstruction from available fragments and citations.
- Provide a critical apparatus, evidence mapping, and confidence estimates (mean, CI) following the repo’s Bayesian factors.
- Save outputs in a clear directory structure that the team can review and publish as research artifacts.

## Inputs Available
- Database: `callimachina_corpus.db` (tables: `works`, `fragments`, `citations`, `translation_chains`).
- Run outputs: `callimachina/discoveries/` (CSV/JSON/MD per work; demo + research artifacts).
- Curated highlights: `README_GALLERY.md`.
- Integrated report: `ALEXANDRIA_RECONSTRUCTED.md` (works confirmed/reconstructed, evidence summaries).
- Docs: `docs/` (methodology, API reference, update reports, continuation prompts).
- Examples: `examples/test_real_fragments.py` (papyri.info retrieval checks).
- CLI and source: `callimachina/src/*.py` (Bayesian reconstructor, scraper, network, stylometry, cross‑lingual, CLI).

If a resource is missing or ambiguous, state the limitation and proceed conservatively.

## Evidence Model (Guiding Heuristics)
When you cannot run code, approximate the Bayesian update by weighting these factors qualitatively, then report a conservative confidence with a wide CI:
- Citation quality & independence (highest weight)
- Temporal distribution of sources (older, independent > later, dependent)
- Cross‑cultural translation paths (Greek→Arabic/Latin/Syriac)
- Stylometric attribution (agreement boosts; disagreement penalizes)
- Network centrality (hubs transmit more; avoid circularity)
- Genre/period base rates (set prior appropriately)

Always explain the qualitative reasoning behind your confidence figure.

## Output Specification (per work)
Create a new directory under `callimachina/discoveries/<Author>_<Title>_<YYYY-MM-DD>_KIMI/` containing:

1) `metadata.yml`
- `work_id`, `author`, `title`, `genre`, `century`
- `provenance`: [fragment-verified|citation-based|demo]
- `sources`: list of evidence sources (with references)
- `confidence`: { prior, posterior_mean, ci_lower, ci_upper, rationale }
- `transmission`: translation chains if any
- `notes`: caveats/assumptions

2) `reconstruction.md`
- Continuous text, clearly marking lacunae with `[…]`.
- Inline footnotes or bracketed references to evidence anchors.
- Keep style conservative; do not invent specifics beyond what evidence supports.

3) `apparatus.md`
- Bulleted list of fragment placements, variants, translation echoes, uncertainties.
- Separate sections: citations, papyri fragments, translation parallels, stylometry, network context.

4) `evidence.json`
- Structured mapping of each passage to the evidence used (source id, type, quote/paraphrase, estimated reliability).

5) `summary.txt`
- One paragraph stating what was reconstructed, why confidence is what it is, and what’s needed to improve it.

Optional (if time/budget):
- `tei.xml` (TEI P5 with `<app>` and `<lacuna>`),
- `index.md` with links to the above and a short abstract.

## Batch Plan
- Pass 1 (10 works): Start with Featured Reconstructions from README (Eratosthenes Geographika; Hippolytus On Heraclitus; Posidippus Epigrams; Callimachus Aetia; Aristotle Protrepticus; Aristotle On Ideas; Aristotle On Philosophy; Eudoxus Mirror; Herophilus Anatomy; Erasistratus On Fevers).
- Pass 2 (→50 works): Expand by confidence/importance from `README_GALLERY.md` and `ALEXANDRIA_RECONSTRUCTED.md`.
- Per work, prefer fragment‑verified evidence; otherwise clearly mark as citation‑based.

## Formatting & Placement
- Use the directory pattern above under `callimachina/discoveries/`.
- Keep filenames predictable: `metadata.yml`, `reconstruction.md`, `apparatus.md`, `evidence.json`, `summary.txt`.
- In text, use explicit markers for lacunae and hypothetical restorations: `[…]` and `[?]`.

## Provenance & Disclaimers (Required)
Add at the top of `reconstruction.md`:
- “Probabilistic reconstruction (automated). Not a critical edition.”
- List of primary evidence sources used (citations, fragments, translations).
- One‑sentence confidence statement with bounds.

## Quality Gate
- Reject any passage lacking at least one evidence anchor (citation, fragment, or strong parallel); move it to `apparatus.md` as a hypothesis instead.
- Keep tone scholarly and cautious.

## Deliverable Index
At the end, generate `callimachina/discoveries/KIMI_RUN_INDEX_<YYYY-MM-DD>.csv` with columns:
`work_id, path, provenance, posterior_mean, ci_lower, ci_upper, sources_count`.

## Example Confidence Rationale (template)
"Posterior ~0.86 (CI 0.62–0.94). Two independent early witnesses (Strabo, Cleomedes) support the key quantitative claim; later paraphrases (Ptolemy) align. No stylometric conflict; Arabic/Latin echoes present. Central network node; moderate risk of dependency among later sources."

## What Not To Do
- Do not claim the discovery of manuscripts.
- Do not fabricate citations or page/line numbers.
- Do not copy modern translations verbatim; synthesize based on evidence.

Proceed when ready.
