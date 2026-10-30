# Physical review — Waveshare ESP32-S3-Touch-AMOLED-1.75 (SKU31261)

Reviewed on a real unit on 2026-10-30. This is the first entry in this repository
verified on hardware rather than rendered: a working hold-to-talk voice roundtrip
through a local Hermes Agent, not a concept.

## Subject

- Board: Waveshare **ESP32-S3-Touch-AMOLED-1.75**, SKU 31261 (variants: 31262 -B with case, 31264 -G with LC76G GNSS)
- Product page: https://www.waveshare.com/esp32-s3-touch-amoled-1.75.htm?sku=31261
- Manufacturer docs: https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75
- Dimension drawing: https://docs.waveshare.com/assets/images/ESP32-S3-Touch-AMOLED-1.75-details-size-75dc998071807f62c5915afad69d7e80.webp
- Firmware: [Hermes Gadget SDK](https://github.com/Adolanium/hermes-gadget-sdk) source build, profile `esp32s3-touch-amoled-175`, version 0.4.1 (ESP-IDF 6.1.0 via PlatformIO `espressif32` 8.0.0)

## Manufacturer dimensions (from the drawing above, unit mm)

Round board overall **48.96** wide; PCB circle **φ46.00**; display glass chords 44.16 / 43.76.
Side profile: **10.40** total depth with connectors, 6.90 body section; layer stack 2.05 / 1.10 / 0.60.
Mounting: **2 × M2.00-H3.5** standoffs, holes 2 × φ1.80. Onboard MX1.25 headers labeled **SPK** and **BAT** (3.7 V LiPo, charge/discharge supported).

## Onboard silicon (verified present over I2C/QSPI by the firmware)

| Part | Chip |
|---|---|
| SoC | ESP32-S3R8, 8 MB octal PSRAM, 16 MB flash |
| Display | CO5300 QSPI AMOLED, 466 × 466 round |
| Touch | CST9217 (I2C 0x5A) |
| Microphones | ES7210 dual array (I2C 0x40) |
| Speaker DAC | ES8311 (I2C 0x18) + amplifier enable |
| Power | AXP2101 PMIC (I2C 0x34), battery charger onboard |
| IO expander | TCA9554 (I2C 0x20) |
| IMU / RTC | QMI8658 / PCF85063 |

## What was verified on this unit

1. **Flash:** PlatformIO source build written over the board's native USB-C (USB JTAG/serial debug unit); all four regions reported `Hash of data verified`, hard reset into app.
2. **Console:** the firmware's serial console answers `status` with device JSON (`board: esp32s3-touch-amoled-1.75`, `firmware: 0.4.1`).
3. **Provisioning:** Wi-Fi join and server address set over the console (`wifi add`, `set server ws://<host>:8765/gadget`); device reached the gateway and displayed a pairing code.
4. **Pairing + roundtrip:** device approved against a local Hermes Agent; hold-to-talk conversation completed — speech captured by the dual microphones, reply streamed to the round AMOLED and spoken. Operator verdict (verbatim, 2026-10-30): "perfect everything working like expected".
5. **Controls:** hold screen = talk, tap = yes, swipe down = cancel/interrupt, PWR hold 2 s = new conversation — all as documented by the SDK profile.

## Not verified / limitations

- One unit, one revision (SKU31261 base version); results do not transfer automatically to -B or -G.
- Battery path untested (`battery_present: false`; ran on external USB power). Charging and PMIC shutdown behaviour unobserved.
- TF slot, IMU data and RTC timekeeping not exercised by this review.
- No enclosure study, no acoustic measurement, no fit test — this document reviews the bare board.
- The SDK marks this port experimental upstream until a full verification report is recorded; the checklist above is a first physical data point, not a certification.
- Wi-Fi/USB only. Cellular remains out of current scope per repository rules.

## Reproduce

```bash
git clone https://github.com/Adolanium/hermes-gadget-sdk
cd hermes-gadget-sdk/firmware/esp32
pio run -e esp32s3-touch-amoled-175 -t upload --upload-port /dev/ttyACM1
```

Host side: the Hermes Gadget plugin (`hermes plugins install https://github.com/Adolanium/hermes-gadget-sdk/tree/main/plugin --enable`), gateway listening on ws port 8765 (open in the host firewall for LAN devices), STT/TTS configured, then `hermes gadget pair`.
