# prettyfsc
FSC plotter: various output options including RELION and CryoSPARC styles

Requires:
- Python
  - matplotlib
  - numpy

```
Usage: prettyfsc.py [OPTIONS] [OUTPUT_FILE]

FSC Curve Plotter for RELION postprocess.star files
Praise or complaints to ray[at]nips.ac.jp if you want

Options:
  -i, --input FILE    Input postprocess.star file (default: postprocess.star)
  -o, --output FILE   Output plot file (default: fsc_plot.svg or .png)
  -p, --png           Output as PNG format (default: SVG)
  -dpi, --dpi NUM     DPI for PNG output (default: 300)
  -rel, --relion      Use RELION-style color scheme
  -cs, --cryosparc    Use CryoSPARC-style (Corrected, Masked, Unmasked, FSC 0.143)
  --no-masked         Do not plot masked FSC
  --no-unmasked       Do not plot unmasked FSC
  --no-randomized     Do not plot randomized FSC
  --no-corrected      Do not plot corrected FSC
  --no-05-threshold   Do not plot 0.5 threshold line
  --no-0143-threshold Do not plot 0.143 threshold line
  -h, --help          Show this help message

Examples:
  python prettyfsc.py -i apoferritin/job033/postprocess.star -o plots/apoferritin_fsc.svg
  python prettyfsc.py -rel -p -dpi 600 -o output.png
  python prettyfsc.py -cs -o cs_style_plot.svg
  python prettyfsc.py --no-randomized --no-unmasked
```
Examples of plot output:
--
Default output:

<img width="632" height="441" alt="zz_default_demo" src="https://github.com/user-attachments/assets/187f6d1e-d853-4372-8a73-0085b1ea01bb" />

- Does not display unmasked FSC


RELION-style output:

<img width="632" height="441" alt="zz_rel_demo" src="https://github.com/user-attachments/assets/c4a2ca5f-002d-4186-89fb-ab01604c1897" />

- Displays all FSC curves


CryoSPARC-style output:

<img width="632" height="441" alt="zz_cs_demo" src="https://github.com/user-attachments/assets/d61493bf-d92f-47b5-a8d1-0d9d7fc2fcb9" />

- Does not display phase-randomised FSC curve
- Does not display FSC = 0.5
