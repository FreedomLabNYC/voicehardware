# Agent skills for the voice hardware

Two battle-tested [Hermes Agent](https://hermes-agent.nousresearch.com) skills
covering the devices reviewed in this repo. Each `SKILL.md` is a complete
runbook: bring-up order, verified commands, and the pitfalls that cost real
debugging time (firewall silence, group-drift serial access, Docker DNS,
picker-only video URIs, hidden setup SoftAPs).

- `m5sticks3-relay-debug/` — M5StickS3 (ESP32-S3) voice stick talking to a
  local Hermes dashboard through a WebSocket relay + cloud STT/TTS. Includes
  `scripts/serial_capture.py` and `scripts/reset_stick.py` (pyserial).
- `hermes-gadget-boards/` — flashing/pairing any Hermes Gadget ESP32-S3 board,
  with `references/waveshare-amoled-175.md`: the full chip/pin map, touch
  gesture table and first-flash verification checklist for the Waveshare
  ESP32-S3-Touch-AMOLED-1.75 (SKU 31261) — the board behind
  [docs/PHYSICAL_REVIEW_AMOLED-1.75.md](../docs/PHYSICAL_REVIEW_AMOLED-1.75.md).

## Install

Drop the skill folders into your Hermes profile's skills directory, e.g.:

```bash
git clone https://github.com/FreedomLabNYC/voicehardware
cp -r voicehardware/skills/m5sticks3-relay-debug  ~/.hermes/skills/
cp -r voicehardware/skills/hermes-gadget-boards   ~/.hermes/skills/hardware/
```

Any agent-capable tool can use the same files — they are plain markdown.

## Security note

All device MACs, Wi-Fi names/credentials, LAN addresses and account names have
been replaced with placeholders (`<your-user>`, `<host-ip>`, `<LAN_SUBNET>`).
Keep your real credentials only in a local, gitignored `.env`.

License: MIT (see each SKILL.md frontmatter and the repo LICENSE).
