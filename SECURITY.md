# Security and Privacy Reporting

## Do not disclose sensitive material in issues or pull requests

Do not place any of the following in GitHub issues, pull requests, comments,
attachments, Actions logs, or collaboration prompts:

- participant names or direct identifiers;
- health records or private case details;
- raw audio, video, gaze, biosignal, or session data;
- credentials, API keys, tokens, cookies, or private keys;
- model weights or learned voice artifacts derived from a participant; or
- exact private storage locations that expose a participant.

## Reporting channel

For a software vulnerability, use the repository's private Security Advisory
flow when available. For a privacy, participant-data, or credential event,
contact the repository owner through an already agreed private channel. Share
only the minimum information needed to contain the event.

## Immediate containment

If sensitive content or a credential enters the repository:

1. stop further sharing and automation;
2. revoke or rotate exposed credentials;
3. preserve minimal timestamps and commit identifiers for the audit trail;
4. notify the responsible investigator or privacy/ethics lead;
5. remove the material from current and historical Git objects using an
   approved incident procedure; and
6. append a non-identifying correction to `PROJECT_CHANGE_LOG.md`.

Deleting the latest file alone is not sufficient because Git history and CI
artifacts may retain copies.

## Scope

This policy is repository security guidance. It does not replace institutional
ethics review, clinical governance, informed consent, data-use agreements, or
applicable law.
