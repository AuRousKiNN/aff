# Arcaea File Format (AFF) Project

## Project Overview
This repository serves as a documentation and reference source for the **Arcaea File Format (AFF)**. AFF is the proprietary file format used for beatmaps (charts) in the mobile rhythm game *Arcaea*.

The project currently consists of detailed specifications regarding the syntax, objects, and control commands used within `.aff` files.

## Key Files

*   **`FORMAT_REF.md`**
    *   **Description:** The core documentation file (in Chinese). It provides a comprehensive specification of the AFF structure.
    *   **Contents:**
        *   **Header Information:** `AudioOffset`, `TimingPointDensityFactor`.
        *   **Timing:** BPM and beat definitions.
        *   **Objects:** Notes (Tap), Holds, Arcs (Sky Notes/Arcs), and Arctaps.
        *   **Advanced Features:** Camera manipulation, Scene control (hiding tracks, red lines), and Timing Groups (for simultaneous different speeds).
        *   **Syntax:** Detailed parameters for each object type (coordinates, timing, easing, etc.).

## Usage
This repository is intended for:
1.  **Chart Designers:** To understand the specific syntax and commands for creating complex Arcaea charts.
2.  **Tool Developers:** As a reference for building AFF parsers, editors, or visualization tools.

### Common Syntax Example
An AFF file typically looks like this:
```text
AudioOffset:0
-
timing(0,180.00,4.00);
(1000,1);
hold(2000,3000,2);
arc(4000,5000,0.00,1.00,s,1.00,1.00,0,none,true)[arctap(4500)];
```

## Note on Language
The primary documentation (`FORMAT_REF.md`) is written in **Chinese**. Users may need to translate specific sections if they are not fluent.
