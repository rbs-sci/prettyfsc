#!/usr/bin/env python3
# FSC Curve Plotter for RELION postprocess.star files
# (C) Raymond N. Burton Smith, 2026 (ray[at]nips.ac.jp)
#
# Requires:
# Python
# - matplotlib
# - numpy
#
#

import re
import matplotlib.pyplot as plt
import numpy as np


def parse_fsc_data(filepath):
    # Parse FSC data from postprocess.star file.
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    in_fsc_section = False
    data_lines = []
    
    for line in lines:
        if 'data_fsc' in line:
            in_fsc_section = True
            continue
        if in_fsc_section and line.startswith('_rln'):
            continue
        if in_fsc_section and line.strip().startswith('loop_'):
            continue
        if in_fsc_section and line.strip() and not line.startswith('#'):
            if line.strip().startswith('data_'):
                break
            parts = line.strip().split()
            if len(parts) >= 7:
                data_lines.append(parts)
    
    indices = []
    resolutions = []
    angstrom_res = []
    fsc_corrected = []
    fsc_particle_mask = []
    fsc_unmasked = []
    fsc_masked = []
    fsc_randomized = []
    
    for parts in data_lines:
        if len(parts) >= 7:
            indices.append(int(parts[0]))
            resolutions.append(float(parts[1]))
            angstrom_res.append(float(parts[2]))
            fsc_corrected.append(float(parts[3]))
            fsc_particle_mask.append(float(parts[4]))
            fsc_unmasked.append(float(parts[5]))
            fsc_masked.append(float(parts[6]))
            if len(parts) >= 8:
                fsc_randomized.append(float(parts[7]))
            else:
                fsc_randomized.append(np.nan)
    
    return {
        'indices': np.array(indices),
        'resolutions': np.array(resolutions),
        'angstrom_res': np.array(angstrom_res),
        'fsc_corrected': np.array(fsc_corrected),
        'fsc_particle_mask': np.array(fsc_particle_mask),
        'fsc_unmasked': np.array(fsc_unmasked),
        'fsc_masked': np.array(fsc_masked),
        'fsc_randomized': np.array(fsc_randomized)
    }


def parse_general_data(filepath):
    # Parse general data from postprocess.star file.
    with open(filepath, 'r') as f:
        content = f.read()
    
    data = {}
    patterns = {
        'final_resolution': r'_rlnFinalResolution\s+(\S+)',
        'bfactor': r'_rlnBfactorUsedForSharpening\s+(\S+)',
        'guinier_slope': r'_rlnFittedSlopeGuinierPlot\s+(\S+)',
        'guinier_intercept': r'_rlnFittedInterceptGuinierPlot\s+(\S+)',
        'guinier_correlation': r'_rlnCorrelationFitGuinierPlot\s+(\S+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            data[key] = float(match.group(1))
    
    return data


def plot_fsc(data, general_data, output_file='fsc_plot.svg', output_format='svg', dpi=300, relion_mode=False, cryosparc_mode=False):
    # Create a pretty FSC plot.
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Determine curve visibility
    if cryosparc_mode:
        show_masked = True
        show_unmasked = True
        show_randomized = False
        show_corrected = True
        show_05_threshold = False
        show_0143_threshold = True
        color_corrected = 'red'
        color_masked = 'pink'
        color_unmasked = 'blue'
        color_randomized = 'red'
        linewidth_corrected = 2.5
        linestyle_masked = '--'
        linestyle_unmasked = '-'
        linestyle_randomized = '-'
        linestyle_0143 = '-'
        linestyle_05 = ':'
        color_0143 = 'black'
        color_05 = '#D62828'
    elif relion_mode:
        show_masked = True
        show_unmasked = True
        show_randomized = True
        show_corrected = True
        show_05_threshold = True
        show_0143_threshold = True
        color_corrected = 'black'
        color_masked = 'blue'
        color_unmasked = 'green'
        color_randomized = 'red'
        linewidth_corrected = 2.5
        linestyle_masked = '-'
        linestyle_unmasked = '-'
        linestyle_randomized = '-'
        linestyle_0143 = ':'
        linestyle_05 = ':'
        color_0143 = '#E9C46A'
        color_05 = '#D62828'
    else:
        show_masked = True
        show_unmasked = False
        show_randomized = True
        show_corrected = True
        show_05_threshold = True
        show_0143_threshold = True
        color_corrected = '#2E86AB'
        color_masked = '#A23B72'
        color_unmasked = '#2E86AB'
        color_randomized = '#F18F01'
        linewidth_corrected = 2.5
        linestyle_masked = '--'
        linestyle_unmasked = '-'
        linestyle_randomized = '-.'
        linestyle_0143 = ':'
        linestyle_05 = ':'
        color_0143 = '#E9C46A'
        color_05 = '#D62828'
    
    reciprocal_resolution = 1.0 / data['angstrom_res']
    fsc_corrected = data['fsc_corrected']
    fsc_masked = data['fsc_masked']
    fsc_randomized = data['fsc_randomized']
    
    if show_masked:
        ax.plot(reciprocal_resolution, fsc_masked, 
                label='Masked FSC', color=color_masked, linewidth=2, alpha=0.7, linestyle=linestyle_masked)
    
    if show_randomized and not np.all(np.isnan(fsc_randomized)):
        ax.plot(reciprocal_resolution, fsc_randomized, 
                label='Randomized FSC', color=color_randomized, linewidth=2, alpha=0.7, linestyle=linestyle_randomized)
    
    if show_corrected:
        ax.plot(reciprocal_resolution, fsc_corrected, 
                label='Corrected FSC', color=color_corrected, linewidth=linewidth_corrected, alpha=0.9, zorder=10)
    
    if show_unmasked:
        ax.plot(reciprocal_resolution, data['fsc_unmasked'], 
                label='Unmasked FSC', color=color_unmasked, linewidth=2, alpha=0.7, linestyle=linestyle_unmasked)
    
    if show_05_threshold:
        ax.axhline(y=0.5, color=color_05, linestyle=linestyle_05, linewidth=1.5, alpha=0.7, label='0.5 Threshold')
    if show_0143_threshold:
        ax.axhline(y=0.143, color=color_0143, linestyle=linestyle_0143, linewidth=1.5, alpha=0.7, label='0.143 Threshold')
    
    ax.axhline(y=0.0, color='#000000', linestyle='-', linewidth=0.8, alpha=1)
    
    fsc_corrected = data['fsc_corrected']
    idx_0143 = np.where(fsc_corrected < 0.143)[0]
    if len(idx_0143) > 0:
        cross_idx = idx_0143[0]
        if cross_idx > 0:
            res_low = data['angstrom_res'][cross_idx - 1]
            res_high = data['angstrom_res'][cross_idx]
            fsc_low = fsc_corrected[cross_idx - 1]
            fsc_high = fsc_corrected[cross_idx]
            frac = (0.143 - fsc_low) / (fsc_high - fsc_low)
            exact_res = res_low + frac * (res_high - res_low)
        else:
            exact_res = data['angstrom_res'][cross_idx]
    else:
        exact_res = data['angstrom_res'][-1]
    
    ax.axvline(x=1.0/exact_res, color='#2A9D8F', linestyle='-', linewidth=2, alpha=0.8,
               label=f'Resolution: {exact_res:.3f} Å')
    
    ax.set_xlabel('Reciprocal Resolution (1/Å)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fourier Shell Correlation', fontsize=12, fontweight='bold')
    
    ax.set_xlim(left=0, right=1.0/(exact_res * 0.9))
    ax.set_ylim(bottom=-0.1, top=1.1)
    
    pass
    
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.legend(loc='lower left', fontsize=10, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    title_text = (f'GS-FSC: {exact_res:.1f} Å | '
                  f'B-factor: {general_data.get("bfactor", "N/A"):.1f} Å² | '
                  f'Guinier corr: {general_data.get("guinier_correlation", "N/A"):.4f}')
    
    ax.set_title(title_text, fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if output_format == 'png':
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight', facecolor='white')
    else:
        plt.savefig(output_file, bbox_inches='tight', facecolor='white')
    
    plt.close()
    
    return fig


def print_summary(data, general_data):
    # Print summary statistics.
    print("\n" + "="*60)
    print("FSC ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\nResolution metrics:")
    print(f"  Final resolution (0.143): {general_data.get('final_resolution', 'N/A')} Å")
    print(f"  B-factor used for sharpening: {general_data.get('bfactor', 'N/A')} Å²")
    
    print(f"\nGuinier plot fit:")
    print(f"  Fitted slope: {general_data.get('guinier_slope', 'N/A')}")
    print(f"  Fitted intercept: {general_data.get('guinier_intercept', 'N/A')}")
    print(f"  Correlation: {general_data.get('guinier_correlation', 'N/A')}")
    
    print("\nFSC statistics:")
    indices = data['indices']
    fsc_corrected = data['fsc_corrected']
    
    idx_0143 = np.where(fsc_corrected < 0.143)[0]
    if len(idx_0143) > 0:
        res_0143 = data['angstrom_res'][idx_0143[0]]
        print(f"  Resolution at FSC=0.143: {res_0143:.3f} Å")
    
    idx_05 = np.where(fsc_corrected < 0.5)[0]
    if len(idx_05) > 0:
        res_05 = data['angstrom_res'][idx_05[0]]
        print(f"  Resolution at FSC=0.5: {res_05:.3f} Å")
    
    fsc_at_half = fsc_corrected[len(fsc_corrected)//2]
    print(f"  FSC at half resolution: {fsc_at_half:.4f}")
    
    print("="*60 + "\n")


def main():
    import sys
    
    # Default values
    filepath = 'postprocess.star'
    output_format = 'svg'
    output_dpi = 300
    output_file = None
    relion_mode = False
    cryosparc_mode = False
    
    show_masked = True
    show_unmasked = False
    show_randomized = True
    show_corrected = True
    
    show_05_threshold = True
    show_0143_threshold = True
    
    def show_help():
        print("Usage: prettyfsc.py [OPTIONS] [OUTPUT_FILE]")
        print("")
        print("FSC Curve Plotter for RELION postprocess.star files")
        print("Praise or complaints to ray[at]nips.ac.jp if you want")
        print("")
        print("Options:")
        print("  -i, --input FILE    Input postprocess.star file (default: postprocess.star)")
        print("  -o, --output FILE   Output plot file (default: fsc_plot.svg or .png)")
        print("  -p, --png           Output as PNG format (default: SVG)")
        print("  -dpi, --dpi NUM     DPI for PNG output (default: 300)")
        print("  -rel, --relion      Use RELION-style color scheme")
        print("  -cs, --cryosparc    Use CryoSPARC-style (Corrected, Masked, Unmasked, FSC 0.143)")
        print("  --no-masked         Do not plot masked FSC")
        print("  --no-unmasked       Do not plot unmasked FSC")
        print("  --no-randomized     Do not plot randomized FSC")
        print("  --no-corrected      Do not plot corrected FSC")
        print("  --no-05-threshold   Do not plot 0.5 threshold line")
        print("  --no-0143-threshold Do not plot 0.143 threshold line")
        print("  -h, --help          Show this help message")
        print("")
        print("Examples:")
        print("  python prettyfsc.py -i apoferritin/job033/postprocess.star -o plots/apoferritin_fsc.svg")
        print("  python prettyfsc.py -rel -p -dpi 600 -o output.png")
        print("  python prettyfsc.py -cs -o cs_style_plot.svg")
        print("  python prettyfsc.py --no-randomized --no-unmasked")
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--help' or args[i] == '-h':
            show_help()
            return
        elif args[i] == '--png' or args[i] == '-p':
            output_format = 'png'
            i += 1
        elif args[i] == '--dpi' or args[i] == '-dpi':
            if i + 1 < len(args):
                output_dpi = int(args[i + 1])
                i += 2
            else:
                i += 1
        elif args[i] == '--input' or args[i] == '-i':
            if i + 1 < len(args):
                filepath = args[i + 1]
                i += 2
            else:
                i += 1
        elif args[i] == '--output' or args[i] == '-o':
            if i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
            else:
                i += 1
        elif args[i] == '--no-masked':
            show_masked = False
            i += 1
        elif args[i] == '--no-unmasked':
            show_unmasked = False
            i += 1
        elif args[i] == '--no-randomized':
            show_randomized = False
            i += 1
        elif args[i] == '--no-corrected':
            show_corrected = False
            i += 1
        elif args[i] == '--no-05-threshold':
            show_05_threshold = False
            i += 1
        elif args[i] == '--no-0143-threshold':
            show_0143_threshold = False
            i += 1
        elif args[i] == '--relion' or args[i] == '-rel':
            relion_mode = True
            i += 1
        elif args[i] == '--cryosparc' or args[i] == '-cs':
            cryosparc_mode = True
            i += 1
        elif output_file is None:
            output_file = args[i]
            i += 1
        else:
            i += 1
    
    if output_file is None:
        if output_format == 'svg':
            output_file = 'fsc_plot.svg'
        else:
            output_file = 'fsc_plot.png'
    
    print(f"Parsing FSC data from: {filepath}")
    
    try:
        data = parse_fsc_data(filepath)
        general_data = parse_general_data(filepath)
    except FileNotFoundError:
        show_help()
        return
    
    print_summary(data, general_data)
    
    fig = plot_fsc(data, general_data, output_file, output_format, output_dpi, relion_mode, cryosparc_mode)
    
    print(f"Plot saved to: {output_file}")


if __name__ == '__main__':
    main()
