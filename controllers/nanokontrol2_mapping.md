# 🎛️ Korg nanoKONTROL2 — Default Mapping Reference

This document describes the default MIDI CC layout of the **Korg nanoKONTROL2** and how it will be used in this project to map to the **UAD SSL S3000 Channel Strip** in Logic Pro.

## 🧠 Philosophy

We assume the nanoKONTROL2 is running **factory settings**, with **no customization** applied via the Korg Editor software. This ensures a portable, no-setup-required experience for most users.

---

## 🎚️ Default MIDI CC Layout

| Control Type      | Channel | CC Range     | Notes               |
|-------------------|---------|--------------|---------------------|
| Faders 1–8        | 1       | CC 0–7       | Not used in SSL MVP |
| Knobs 1–8         | 1       | CC 16–23     | Used in SSL MVP     |
| Solo Buttons (S)  | 1       | CC 32–39     | Optional             |
| Mute Buttons (M)  | 1       | CC 48–55     | Optional             |
| Record Buttons (R)| 1       | CC 64–71     | Optional             |
| Transport Buttons | 1       | CC 41, 42... | DAW-specific         |

---

## 🎯 SSL MVP Mapping (Initial Plan)

| nanoKONTROL2 Knob | CC | SSL Parameter        |
|-------------------|----|----------------------|
| Knob 1            | 16 | Input Gain           |
| Knob 2            | 17 | Low EQ Gain          |
| Knob 3            | 18 | Mid EQ Gain          |
| Knob 4            | 19 | High EQ Gain         |
| Knob 5            | 20 | Comp Threshold       |
| Knob 6            | 21 | Comp Ratio           |
| Knob 7            | 22 | Output Gain          |
| Knob 8            | 23 | Bypass Toggle (TBD)  |

This layout matches the default MIDI channel (1) and ensures the most important parameters of the SSL strip are available directly on the top row of knobs.

---

## 🛠️ Notes for Developers

- The Korg Editor can modify this layout, but we will not support altered configs for the MVP.
- If detection of a custom layout becomes necessary, we may explore using MIDI identity requests.
- Mapping files will be stored in the format `ssl_mapping_korg.json` and applied via patching tool.

---

## 🔗 Resources

- [Korg nanoKONTROL2 Product Page](https://www.korg.com/us/products/computergear/nanokontrol2/)
- [Korg Control Editor Download](https://www.korg.com/us/support/download/product/0/159/)
- [MIDI Implementation Chart (PDF)](https://i.korg.com/uploads/Support/nanoKONTROL2_MIDIChart_E_633659281611600000.pdf)