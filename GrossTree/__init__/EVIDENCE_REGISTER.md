# Evidence Register

**Version:** 0.3

**Purpose:** Tie design decisions to evidence while stating what each source
cannot establish.

## E001 - Personalized ASR for disordered speech

**Source**

Green, J. R., et al. (2021). *Automatic Speech Recognition of Disordered
Speech: Personalized models outperforming human listeners on short phrases*.
INTERSPEECH 2021. DOI:
[10.21437/Interspeech.2021-1384](https://doi.org/10.21437/Interspeech.2021-1384)

**Local evidence**

Full text not redistributed in the public repository; see the DOI above.

**Supports**

- speaker personalization can substantially improve short-phrase recognition;
- training-set size and signal-to-noise ratio matter;
- severity, intelligibility, articulation, phonation, and prosody affect
  performance; and
- evaluation should include the participants most likely to benefit.

**Does not support**

- equivalent performance in spontaneous conversation;
- Chinese dialect transfer;
- zero-shot recognition for a new participant;
- semantic or aphasia recovery; or
- replacing participant confirmation.

The paper reports results from prompted short phrases and explicitly calls for
further work in longer, spontaneous, and demanding conditions. This limitation
drives the Phase 1 constrained-task ordering and prospective session split.

## E002 - Non-invasive semantic language decoding

**Source**

Tang, J., LeBel, A., Jain, S., & Huth, A. G. (2023). *Semantic reconstruction of
continuous language from non-invasive brain recordings*. Nature Neuroscience,
26, 858-866. DOI:
[10.1038/s41593-023-01304-9](https://doi.org/10.1038/s41593-023-01304-9)

**Local evidence**

Full text not redistributed in the public repository; see the DOI above.

**Supports**

- semantic reconstruction from person-specific fMRI is scientifically
  possible;
- reconstruction can address perceived and imagined language under controlled
  conditions; and
- subject cooperation is relevant to both training and application.

**Does not support**

- consumer or home deployment;
- wearable EEG equivalence;
- decoding without individual training;
- cross-person generalization; or
- involuntary reading of arbitrary thought.

This evidence keeps direct semantic brain decoding in the Extension track.

## E003 - AAC capability and access assessment

**Source**

American Speech-Language-Hearing Association. *Augmentative and Alternative
Communication (AAC) Practice Portal*:
[ASHA AAC](https://www.asha.org/practice-portal/professional-issues/augmentative-and-alternative-communication/)

**Supports**

- comprehensive and culturally/linguistically relevant assessment;
- multimodal access;
- eye gaze, touch, switch, and scanning as selection methods;
- participation- and person-centered planning; and
- collaboration among SLP, rehabilitation, vision, and technical roles.

**Design consequence**

Diagnosis does not determine the route by itself. Capability profiling and
non-AI fallbacks are mandatory.

## E004 - Early live evaluation of clinical AI

**Source**

Vasey, B., et al. (2022). *DECIDE-AI*. Nature Medicine, 28, 924-933:
[10.1038/s41591-022-01772-9](https://doi.org/10.1038/s41591-022-01772-9)

**Supports**

- explicit intended use and workflow placement;
- early small-scale clinical evaluation before large trials;
- human-factors and human-AI interaction reporting;
- documentation of errors and adaptations; and
- transparent reporting of live clinical evaluation.

**Does not replace**

- an ethics protocol;
- a study-design-specific statistical plan; or
- regulatory review.

## E005 - Good Machine Learning Practice

**Source**

U.S. FDA / IMDRF. *Good Machine Learning Practice for Medical Device
Development: Guiding Principles*:
[FDA GMLP](https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles)

**Supports**

- total-product-lifecycle thinking;
- representative data and independent testing;
- human-AI team performance;
- clear intended use;
- monitoring of deployed performance; and
- controlled model changes.

**Design consequence**

NRLIS versions data, models, thresholds, and workflow decisions before a
medical-device claim exists.

## E006 - Adults who may lack consent capacity

**Source**

NIH IRB. *Adults Who Lack Capacity to Consent to Research*:
[NIH guidance](https://irbo.nih.gov/research-with-vulnerable-populations/adults-who-lack-capacity-to-consent-to-research/)

**Supports**

- communication impairment and consent capacity require careful, accessible
  assessment;
- inclusion of adults lacking capacity requires an approved protection
  pathway; and
- representative permission does not eliminate participant protections.

**Jurisdiction note**

NIH policy is not assumed to be the governing local rule. The relevant
institution and jurisdiction must make the actual determination.

## E007 - Human-participant determination and informed consent

**Sources**

- HHS OHRP, [Federal Policy for the Protection of Human Subjects](https://www.hhs.gov/ohrp/regulations-and-policy/regulations/common-rule/index.html)
- HHS OHRP, [Informed Consent FAQs](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/informed-consent/index.html)
- HHS OHRP, [Exempt Research Determination FAQs](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/exempt-research-determination/index.html)
- eCFR, [45 CFR 46.102(i)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.102)
- eCFR, [21 CFR 50.3(l)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-A/section-50.3)

**Supports**

- IRB approval before covered non-exempt human-participant research;
- OHRP recommendation, rather than a universal Common Rule mandate, that
  investigators not independently determine exemption; stricter local or
  project rules may require an external determination;
- prospective, legally effective informed consent unless an authorized waiver
  applies;
- consent as disclosure, understanding, and voluntariness rather than a
  signature alone;
- LAR authority under the definition governing the activity: applicable law,
  plus the 45 CFR 46.102(i) institutional-policy fallback when that rule
  applies and no law addresses the issue, while 21 CFR 50.3(l) states the
  applicable-law route; and
- additional safeguards when coercion, undue influence, or impaired
  decision-making may be relevant.

**Design consequence**

As a stricter project rule, NRLIS does not self-exempt, infer incapacity from
communication impairment, or treat family status as LAR authority. Cornell's
local rule requires IRB-staff exemption determination if Cornell governs. The
external scope, issuing authority, conditions, review date, and revocation
state remain machine-blocking.

## E008 - Cornell human-research, consent, and data process

**Sources**

- Cornell Research Services, [Research with Human Participants](https://researchservices.cornell.edu/compliance/human-research)
- Cornell Research Services, [IRB FAQs](https://researchservices.cornell.edu/resources/irb-faqs)
- Cornell Research Services, [IRB Informed Consent](https://researchservices.cornell.edu/resources/irb-informed-consent)
- Cornell Research Services, [Human-participant data considerations](https://researchservices.cornell.edu/resources/human-participant-data)

**Supports**

- IRB/HRPP determination for human-participant work conducted under Cornell
  auspices;
- investigator inability to self-determine an exemption;
- multiple institutions may require separate review unless a documented
  reliance/authorization agreement designates one reviewing IRB;
- training and accountable-investigator requirements;
- accessible, understandable consent materials; and
- protocol-level privacy, confidentiality, storage, and breach controls.

**Applicability limit**

Cornell is not assumed to govern merely because the project owner is a student.
The auspices, campus, faculty/PI, and IRB-of-record questions require a written
institutional answer.

## E009 - HIPAA and de-identification boundaries

**Sources**

- HHS OCR, [The HIPAA Privacy Rule](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
- HHS OCR, [De-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)
- eCFR, [45 CFR 164.514](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514)

**Supports**

- HIPAA applicability depends on covered-entity, business-associate, and data
  flow roles;
- Expert Determination and Safe Harbor are distinct de-identification routes;
- coded or pseudonymous data are not automatically de-identified; and
- voiceprints, full-face/comparable images, and other unique characteristics
  are explicit identifier concerns under the HIPAA pathway; and
- re-identification risk depends on data and recipient context.

**Design consequence**

NRLIS does not claim that an N-of-1 profile, voice, gaze/video, embedding, or
rare message is anonymous merely because names are removed. Project privacy
controls apply even when HIPAA is authoritatively found not applicable.
Repository/reporting eligibility is therefore recorded as
`disclosure-reviewed and release-approved`; `HIPAA-de-identified` is used only
when a documented 45 CFR 164.514 route applies.

## E010 - Device software and investigational-device boundary

**Sources**

- FDA, [How to Determine if Your Product is a Medical Device](https://www.fda.gov/medical-devices/classify-your-medical-device/how-determine-if-your-product-medical-device)
- FDA, [Investigational Device Exemption](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/investigational-device-exemption-ide)

**Supports**

- intended use and indications are central to device status;
- software functions can be device functions;
- investigational device studies may require IRB, informed consent, and,
  depending on risk and exemption status, FDA action; and
- a formal or qualified determination is available when classification is
  uncertain.

**Design consequence**

The terms prototype, family case, shadow, and N-of-1 do not themselves settle
device or IDE applicability. NRLIS makes no device classification, clinical
claim, or investigational-device authorization in WP1.

## E011 - Voluntary AI lifecycle governance

**Source**

NIST, [AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)

**Supports**

- explicit roles and accountability;
- lifecycle risk mapping, measurement, management, and monitoring;
- documentation of affected people and contexts;
- human oversight, incident response, and change control; and
- privacy, transparency, validity, reliability, safety, and security as
  interacting trustworthiness properties.

**Does not replace**

- IRB or ethics review;
- informed consent;
- privacy-law determination;
- medical-device determination; or
- clinical evidence.

## E012 - Accessible communication during consent

**Sources**

- U.S. Department of Justice, [ADA Requirements: Effective Communication](https://www.ada.gov/resources/effective-communication/)
- HHS OHRP, [Consent for non-English speakers](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/obtaining-and-documenting-infomed-consent-non-english-speakers/index.html)

**Supports**

- communication methods matched to the person's usual access and the
  complexity of the interaction;
- qualified communication assistance rather than relying on an interested
  family companion by default;
- understandable language and translated/short-form consent routes when
  approved; and
- participant access as a condition of meaningful choice.

**Applicability limit**

ADA and OHRP requirements depend on setting and governing authority. NRLIS uses
them as a stricter accessibility design baseline while awaiting the actual
determination.

## Evidence-status labels

- `local_primary`: full local paper or faithful page images available
- `external_primary`: authoritative paper or official source linked
- `hypothesis`: design proposal not yet empirically supported in NRLIS
- `project_evidence`: evidence generated under a frozen NRLIS protocol

Every future claim should cite at least one evidence-status label and state its
generalization level.
