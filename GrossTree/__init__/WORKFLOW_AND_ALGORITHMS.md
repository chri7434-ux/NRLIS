# Workflow and Initial Algorithm Design

**Version:** 0.4
**Design principle:** Route by observable capability, combine evidence
probabilistically, abstain when uncertain, and preserve participant authorship.

## 1. Capability representation

Each profile contains a capability vector:

\[
z_i = [L_r,L_e,S,G,M,R,V,H,F,P]
\]

where:

- \(L_r\): receptive-language ability;
- \(L_e\): expressive-language formulation;
- \(S\): residual acoustic speech information;
- \(G\): gaze-control reliability;
- \(M\): other motor-control reliability;
- \(R\): reading and symbol comprehension;
- \(V,H\): visual and auditory access;
- \(F\): fatigue and attention constraints; and
- \(P\): stability or progression over time.

Values are session-sensitive and provenance-tagged. They are not generated as
medical diagnoses by the model.

## 2. Modality routing

The routing policy selects the available modality set \(m\) that minimizes
expected communication cost:

\[
m^* = \arg\min_m
\left[
\alpha\,E(\text{semantic error})
+ \beta\,E(\text{time})
+ \gamma\,E(\text{effort})
+ \eta\,E(\text{unsafe output})
\right]
\]

The initial order of preference is not fixed by technology prestige. Direct
touch may be preferable to gaze; a reliable switch may be preferable to noisy
speech; residual speech may supplement rather than replace an AAC board.

## 3. Core inference stack

For candidate message \(y\), evidence \(x\), context \(c\), and profile \(z_i\):

\[
S(y) =
\alpha \log p_{\text{acoustic}}(y \mid x_a)
+ \beta \log p_{\text{articulatory}}(y \mid x_v)
+ \gamma \log p_{\text{dialect}}(y)
+ \delta \log p_{\text{context}}(y \mid c)
+ \rho \log p_{\text{personal}}(y \mid i)
\]

Not every term is active for every participant. The first implementation should
make every weight inspectable and versioned.

### 3.1 Acoustic model

Initial research approach:

1. start with a frozen multilingual self-supervised or sequence-to-sequence
   speech encoder;
2. train a small task head or adapter on confirmed P001 data;
3. compare CTC-style token decoding and short-phrase classification;
4. avoid full-model fine-tuning until data volume and leakage controls justify
   it; and
5. retain acoustic posterior information instead of only the best transcript.

### 3.2 Population prior plus personal adapter

\[
\theta_i = \theta_{\text{population}} + \Delta\theta_i
\]

The population component represents transferable speech features. The personal
adapter represents speaker-, dialect-, condition-, and session-specific
patterns. Phase 1 may estimate only \(\Delta\theta_{P001}\); it must not claim
that a population prior has been learned from one person.

Candidate adaptation methods to compare later:

- low-rank adapters or LoRA;
- speaker embeddings or learned prompts;
- prototype/nearest-neighbor matching for a constrained phrase bank;
- hierarchical Bayesian personalization;
- parameter-efficient fine-tuning; and
- meta-learning only after a multi-participant cohort exists.

### 3.3 Dialect and personal language layer

Keep the following separable:

- spoken dialect tokens or phonetic representation;
- standard written-Chinese semantic labels, when appropriate;
- personal names and household vocabulary;
- phrase frequency and conversation context; and
- output voice and pronunciation.

Historical healthy-speech audio may support voice identity and language style.
It does not replace paired post-impairment speech and confirmed intent for
recognition training.

### 3.4 Candidate generation

The system returns an \(N\)-best set plus mandatory control options:

- candidate messages;
- "none of these";
- "repeat";
- "cancel"; and
- a non-predictive spelling, symbol, or scanning fallback.

Candidate-set size should be optimized for coverage versus selection burden,
not fixed globally.

### 3.5 Calibration and abstention

Raw neural-network probabilities must not be interpreted as trustworthy
confidence. Candidate methods include:

- temperature scaling on a validation block;
- Brier score and Expected Calibration Error;
- conformal prediction for candidate-set coverage;
- entropy or margin-based abstention; and
- risk-specific thresholds.

The system abstains when evidence is insufficient:

\[
\text{output} =
\begin{cases}
\Gamma(x), & \text{if calibrated risk} \le \tau \\
\text{fallback}, & \text{otherwise}
\end{cases}
\]

No confidence threshold may bypass participant confirmation in Phase 1.

### 3.6 Multimodal fusion

Start with late fusion because it:

- permits missing modalities;
- makes modality contributions inspectable;
- supports participant-specific routing; and
- reduces the data required compared with a fully joint end-to-end model.

Audio-video or audio-gaze joint models may be studied only after separate
baselines and synchronization quality are established.

### 3.7 Confirmed-only active learning

Online adaptation may use:

- accepted candidate;
- explicit rejection;
- corrected label;
- session condition;
- response time; and
- access-method reliability.

An inferred or caregiver-guessed label is not equivalent to participant
confirmation. Every label stores its source and confidence.

### 3.8 Drift monitoring

Monitor by session rather than averaging all history:

- acoustic embedding shift;
- rising abstention;
- calibration drift;
- increasing correction or cancellation;
- gaze/switch reliability;
- fatigue-associated latency; and
- changes in vocabulary or context.

Detected drift triggers recalibration or fallback, not silent model updating.

## 4. Required baselines

Every AI method must be compared with:

1. unaided current communication;
2. a low-tech fixed phrase or symbol board;
3. the participant's best direct access method;
4. generic ASR without personalization, if residual speech is used;
5. personalized acoustic modeling without an LLM;
6. contextual reranking with a fixed candidate bank; and
7. the complete calibrated workflow.

This separates the benefit of deep learning from the benefit of a better
interface or a smaller phrase set.

## 5. Initial deep-learning experiment order

1. Constrained short-phrase classification.
2. Frozen multilingual encoder plus personal classifier.
3. Personal adapter for phoneme/token recognition.
4. Dialect-aware lexical and personal-vocabulary reranking.
5. Calibrated Top-k candidate sets.
6. Optional audio-visual late fusion.
7. Open-vocabulary decoding only after prospective constrained-task success.
8. sEMG, EEG, and BCI remain Extension-track research.

### 5.1 Current executable milestone

The first participant-free neural baseline is implemented in
`../Basic/Training/Implementation/participant_free_neural.py`. It trains a
small two-layer multilayer perceptron on generated synthetic embedding vectors,
fits a temperature on a separate calibration split, applies probability and
margin abstention rules, and evaluates only a held-out synthetic test split.

This milestone verifies neural training, split isolation, calibration,
abstention, deterministic artifacts, and disabled output. Its inputs are not
speech features. It establishes neither ASR performance nor any claim about
P001, dysarthria, dialect, clinical effectiveness, or cross-person
generalization. The next participant-free model milestone is a licensed public
speech corpus adapter with the same interface and claim boundary.

### 5.2 WP2.1 recording and Care-mode interfaces

The recording-intake framework precedes every future audio pipeline. Its v0.1
schema records only participant-neutral categories and deny-only states: source
context, speaker multiplicity, separate permission scopes, reference status,
chronological split status, and disposition. It intentionally excludes audio,
paths, original filenames, transcripts, precise time/location, identifying
facts, and participant-level hashes. The executable accepts only its synthetic
fixture and opens no ingest or model-use path.

The Care-mode synthetic MVP separately demonstrates the candidate-to-
confirmation interaction contract. A person first chooses a generic context,
then selects one of four bounded phrases or a mandatory safety action. A
selected phrase remains pending until a separate confirmation control is
activated. The app provides touch, keyboard, switch-style scanning, and a
bounded event adapter for future gaze software; it implements neither gaze
estimation nor AI inference. It performs no recording, persistence, analytics,
speech synthesis, external connection, or research measurement.

This separation permits interface and accessibility work to mature before a
model or participant dataset exists. Later signal models must target the same
bounded candidate and abstention contract instead of bypassing confirmation.

### 5.3 WP2.2 semantic vocabulary and interaction architecture

WP2.2 makes `concept_id`, rather than rendered phrase text, the boundary between
a future inference module and the user interface. Each concept has a stable
semantic domain, speech-act type, versioned canonical/compact renderings,
low-risk classification, mandatory confirmation, and synthetic provenance.
Contexts constrain navigation; four-item panels control visual and scanning
burden. Neither a context nor a panel is a training label.

The current synthetic vocabulary contains 40 concepts across five contexts and
ten fixed panels. It performs no ranking: panel composition and order are
versioned lookup data. Compact text is a second rendering of the same concept,
not a new label. Dialect variants, personal names, household terms, learned
frequency, and historical-voice style are absent; a future private overlay must
be separately versioned, permission-scoped, reversible, and collision-checked.

The DOM-independent transition core exposes the following safe state machine:

`context -> panel -> concept pending -> confirm or reject -> visual output`

Navigation, surface switching, repeat, none, and rejection cannot create an
output. Confirmation is the only output-producing transition. Cancel clears
the complete transient message state, while fallback clears user-message state
and exits the candidate flow. External pointer, keyboard, switch, or future gaze
adapters can only focus or activate controls already represented by this state
machine.

Seven declarative synthetic scenarios execute the direct-confirmation,
rejection/correction, panel-navigation, compact-surface, none/fallback, repeat,
cancel, and hidden-concept rejection paths. These scenarios are software test
vectors, not human interaction records. They contain no timing, score,
identifier, audio, transcript, model result, or participant observation.

## 6. Why this ordering is rational

The local disordered-speech study reports strong personalized-ASR performance
on short phrases while explicitly identifying longer spontaneous speech,
noise, severity, and limited training data as unresolved challenges. The
project therefore begins with a falsifiable constrained task, then expands the
message space only after future-session evidence supports doing so.

The local fMRI semantic-decoding paper is treated as evidence of scientific
possibility, not near-term product readiness. Its person-specific training,
scanner dependence, and requirement for cooperation keep direct semantic brain
decoding outside the Phase 1 core.
