---
name: ask-mfx
description: "MFX beamline operations assistant. Use when working with the MFX hutch-python session, checking XTC data files, running scans, querying device state, or looking up MFX-specific PVs, gotchas, and procedures. Covers IPython bridge setup, set_energy, autorun, undulator pointing, DCCM, beam readiness checks, and accumulated operational gotchas."
---

# Skill: ask-mfx

You are an operations assistant for the MFX instrument at LCLS.
You help with live beamline control via the IPython bridge, data file checks on S3DF,
and accumulated operational knowledge from shift experience.

---

## IPython Bridge — Remote Hutch Python Control

The IPython bridge allows OpenCode (running on S3DF) to execute commands in the live
hutch-python session on `mfx-daq`.

### Connection chain
```
S3DF (OpenCode) :9999 → psdev02 :9998 → mfx-daq :9999 (IPython bridge)
```

### Deploy script
```bash
bash /sdf/data/lcls/ds/mfx/mfx101609126/results/fpoitevi/deploy_bridge.sh
```
> **Gotcha:** Must `kinit` on **psdev02** specifically (not psdev) before running the deploy script.
> The GSSAPI hop to `mfxopr@mfx-daq` only works from psdev02 in this setup.

### Setup steps

**Step 1 — Deploy bridge to mfx-daq** (run deploy script above)

**Step 2 — Start bridge in hutch-python on mfx-daq:**
```python
%run /tmp/ipython_bridge.py
# prints: IPython bridge listening on localhost:9999
```

**Step 3 — SSH tunnel Terminal A (on psdev02):**
```bash
ssh -L 9998:localhost:9999 mfxopr@mfx-daq
```

**Step 4 — SSH tunnel Terminal B (on S3DF):**
```bash
ssh -L 9999:localhost:9998 psdev02
```

**Step 5 — Test connection:**
```bash
echo '{"code": "1+1"}' | nc -w 5 localhost 9999
# → {"status": "ok", "result": "2", ...}
```

### Sending commands via bridge
```bash
echo '{"code": "PYTHON_CODE_HERE"}' | nc -w TIMEOUT localhost 9999
```
- Timeout: 5s for reads, 30s for moves, 60s+ for scans
- Response fields: `status`, `result`, `stdout`, `stderr`, `error`

### Confirmation protocol
- **Read-only commands** (`.wm()`, `get_run()`, `print(...)`, etc.): execute directly
- **Write commands** (moves, scans, DAQ operations): show command to user and wait for go-ahead

---

## Beam Readiness Check

A comprehensive readiness script is bundled at:
```
/sdf/home/j/jb2717/.claude/skills/ask-mfx/references/check_beam_ready.py
```

Load and run it in hutch-python:
```python
%run /sdf/home/j/jb2717/.claude/skills/ask-mfx/references/check_beam_ready.py
check_beam_ready()
```

Or run it via the IPython bridge from S3DF:
```bash
echo '{"code": "exec(open(\"/sdf/home/j/jb2717/.claude/skills/ask-mfx/references/check_beam_ready.py\").read()); check_beam_ready()"}' \
  | nc -w 30 localhost 9999
```

### What it checks

| # | Check | Type | Pass condition |
|---|-------|------|----------------|
| 1 | **Beam destination** | CRITICAL | `mr1l4_homs.pitch` within 10 µrad of −562.035 (MFX) |
| 2 | **Imagers / YAGs** | WARNING | yag0, yag1, yag2, dg1_pim, dg2_pim, dia_pim all `.removed` |
| 3 | **Valves** | INFO | Reports state of dg1×2, dia×2, dvd, mxt valves |
| 4 | **Energy** | CRITICAL | `beam_status` pulse energy > 0.05 mJ; DCCM readback reported |
| 5 | **Undulator pointing** | INFO | X/Y from `BPMS:UNDH:4690:XOFF.D` / `YOFF.D` |
| 6 | **Slits** | INFO | sl1l0, dg1_slits, dg2_upstream_slits x/y widths |
| 7 | **DAQ** | INFO | Current run number from `get_run()` |

Returns `True` if all CRITICAL checks pass.

---

## Key Commands

### Energy control
```python
# Set DCCM only
set_energy(7120, ['d'])

# Set undulator K only (sends to MCC via EPICS)
set_energy(7120, ['k'])

# Set both K and DCCM
set_energy(7120, ['k', 'd'])

# Set K, DCCM, and XRT/FEE spectrometer crystal
set_energy(7120, ['k', 'd', 'x'], crystal_angle_offset=1.3)

# Read current energies
get_energy(['k', 'd'])        # K setpoint + DCCM
print(round(dccm.energy.wm()*1000, 1))  # DCCM readback in eV
```
> **Gotcha:** `crystal_angle_offset` is silently ignored unless `'x'` or `'all'` is in the pv_list.

### Undulator pointing
```python
und_abs_safe((x_um, y_um), wait=True)   # absolute move, max 50 µm/step
und_abs((x_um, y_um), wait=True)        # absolute move, single step
und_del((dx_um, dy_um), wait=True)      # relative (delta) move
```
**Alignment policy (confirmed Matt Seaberg, June 24):**
- Upstream of IM3L0 (z < 746 m): use undulator for both X and Y
- Downstream of IM3L0: use **MR2L0 for X**, undulator for **Y only**

### Data acquisition
```python
# Short test run (dry run, no recording)
autorun(sample='test', run_length=10, record=False, runs=1, daq_num=2, picker=None)

# Real recording run
autorun(sample='Fe_foil', run_length=60, record=True, runs=1, daq_num=2, picker=None)

# Check current run number
get_run()
```

### EXAFS scans
```python
from mfx.exafs import EXAFSEnergyRangeBuilder
builder = EXAFSEnergyRangeBuilder()
energies, _, _, _ = builder.build_energy_range(min_K_value=2.0, max_K_value=16.0, K_spacing=0.5)

summary = exafs.k_xas_scan(
    k_positions=energies,
    dccm_offsets=[0.0],
    dwell_time=3.0,
    k_move_mode='concurrent_settled',
    track_feespec=True,
    track_feespec_blocking=False,
    record=True,
    sample='Fe_foil'
)
```

---

## Key PVs

### Energy / undulator K
| PV | Purpose |
|----|---------|
| `MFX:USER:MCC:EPHOT:SET2` | K energy setpoint (eV) → MCC tunes undulator gaps |
| `MFX:USER:MCC:EPHOT:SET1` | Vernier setpoint (eV) |
| `MFX:USER:MCC:EPHOT:REF1` | Vernier reference |
| `MFX:USER:MCC:EPHOT:REF2` | K reference |

### Undulator pointing
| PV | Purpose |
|----|---------|
| `MFX:USER:MCC:UND:DELTA_X` | X delta setpoint (µm, polarity-flipped internally) |
| `MFX:USER:MCC:UND:DELTA_Y` | Y delta setpoint (µm) |
| `MFX:USER:MCC:UND:GO` | Pulse to 1 to execute move |
| `SIOC:SYS0:ML07:AO216` | Done PV — goes to 0 when move completes |
| `BPMS:UNDH:4690:XOFF.D` | X position readback (mm) |
| `BPMS:UNDH:4690:YOFF.D` | Y position readback (mm) |

---

## Data Files on S3DF

### XTC files
```
/sdf/data/lcls/ds/mfx/mfx101609126/xtc/mfx101609126-r<RRRR>-s<SS>-c000.xtc2
```
> **Gotcha:** XTC files may not appear on S3DF immediately after a run ends.
> There is a transfer delay between the instrument DAQ nodes and S3DF.
> Wait 1–2 minutes after `get_run()` returns before expecting files to be visible.
> The most recently visible files on S3DF may be 1–2 runs behind the current run number.

### Count events in a completed run (from S3DF)
```bash
source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh
python -c "
import psana
ds = psana.DataSource(exp='mfx101609126', run=<RUN>)
run = next(ds.runs())
print(sum(1 for _ in run.events()))
"
```

### Results directory
```
/sdf/data/lcls/ds/mfx/mfx101609126/results/fpoitevi/
```
Key files:
- `beam_notes.md` — shift log
- `deploy_bridge.sh` — bridge deploy script
- `ipython_bridge.py` — copy of bridge script

---

## MFX↔MEC Beam Switching

> **Do not use the Beam Destination pyDM GUI** — it resets MR2L0 pointing.
> MR2L0 (−7.401 µrad) and MR1L0 (4.150 µrad) must remain untouched.

### MFX → MEC
```python
mr1l4.pitch.move(819.2)
und_abs_safe((0, -450), wait=True)
# Check beam on xrt_yag1b — expect crosshair (594, 171)
```

### MEC → MFX
```python
mr1l4.pitch.move(-562.035)
und_abs_safe((0, -410), wait=True)
# Check beam on MFX DG1 YAG
```

---

## Known Bugs & TODOs (accumulated from shifts)

### PPM_screen
1. **Undulator used for X** — should delegate horizontal corrections to MR2L0 downstream of IM3L0
2. **YAG insert/retract not automated** — currently manual at each imager step
3. **MFX DG2 not supported** — not yet added as an imager
4. **Fixed 20 µm tolerance too tight downstream** — should scale with z-position (available from happi)
5. **Calibration not reloaded after save** — requires PPM_screen restart to pick up new `imager_info.json`

### Notch scan / DAQ
6. **`SerialDataSource` FileNotFoundError freezes DAQ** — file transfer error not caught; needs try/except with graceful abort
7. **`getState()` timeouts** — non-fatal; ZMQ/IPC hiccup, monitor for recurrence
8. **DCCM notch scan causes pointing drift on `xrt_yag1`** — needs live pointing correction (undulator Y + MR2L0 X) interleaved with DCCM steps

### EXAFS / k_xas_scan
9. **`crystal_angle_offset` silently ignored** unless `'x'` or `'all'` in pv_list of `set_energy()`
10. **FEE camera PV updated**: `CAMR:FEE1:441:Acquire` → `XRT:ZYLA:CAM:01:Acquire` (Zyla replacement, as of June 26)

---

## Branch
Hutch python is on branch: `dot-commissioning`
Repo: https://github.com/pcdshub/mfx/tree/dot-commissioning
