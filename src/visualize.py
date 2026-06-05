import json
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#0f3460',
    'axes.labelcolor': '#e2e2e2',
    'axes.titlecolor': '#e2e2e2',
    'xtick.color': '#a8a8b3',
    'ytick.color': '#a8a8b3',
    'text.color': '#e2e2e2',
    'grid.color': '#0f3460',
    'grid.linewidth': 0.8,
    'font.family': 'DejaVu Sans',
})

with open('/home/cc/weather-mpi/output/results.json', 'r') as f:
    data = json.load(f)

stats = data['final_stats']
seq_time = data['seq_time']
par_time = data['par_time']
speedup = data['speedup']

print("Generating charts...")

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.patch.set_facecolor('#1a1a2e')
fig.suptitle('Jena Climate Analysis  |  MPI Parallel Computing',
             fontsize=16, fontweight='bold', color='#e94560', y=0.98)

# Chart 1 — Temperature
ax1 = axes[0, 0]
labels = ['Avg Temp', 'Max Temp', 'Min Temp']
values = [stats['avg_temp'], stats['max_temp'], stats['min_temp']]
colors = ['#4cc9f0', '#f72585', '#7209b7']
x = np.arange(len(labels))
bars = ax1.bar(x, values, color=colors, width=0.5, edgecolor='#1a1a2e', linewidth=1.2, zorder=3)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=10)
ax1.set_title('Temperature Statistics', fontsize=12, fontweight='bold', pad=12, color='#4cc9f0')
ax1.set_ylabel('°C', fontsize=10)
ax1.axhline(y=0, color='#e94560', linewidth=1, linestyle='--', zorder=2)
ax1.grid(axis='y', zorder=0)
ax1.set_axisbelow(True)
for bar, val in zip(bars, values):
    ypos = bar.get_height() + (0.8 if val >= 0 else -2.0)
    ax1.text(bar.get_x() + bar.get_width()/2, ypos,
             f'{val:.2f}C', ha='center', fontsize=10, fontweight='bold', color='#ffffff')

# Chart 2 — Humidity & Wind
ax2 = axes[0, 1]
labels2 = ['Avg Humidity', 'Avg Wind', 'Max Wind']
vals2 = [stats['avg_humidity'], stats['avg_wind'], stats['max_wind']]
units = ['%', 'm/s', 'm/s']
colors2 = ['#4361ee', '#4cc9f0', '#f72585']
x2 = np.arange(len(labels2))
bars2 = ax2.bar(x2, vals2, color=colors2, width=0.5, edgecolor='#1a1a2e', linewidth=1.2, zorder=3)
ax2.set_xticks(x2)
ax2.set_xticklabels(labels2, fontsize=10)
ax2.set_title('Humidity & Wind Statistics', fontsize=12, fontweight='bold', pad=12, color='#4cc9f0')
ax2.grid(axis='y', zorder=0)
ax2.set_axisbelow(True)
for bar, val, unit in zip(bars2, vals2, units):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
             f'{val:.2f} {unit}', ha='center', fontsize=10, fontweight='bold', color='#ffffff')

# Chart 3 — Execution Time
ax3 = axes[1, 0]
time_labels = ['Sequential\n(1 Process)', 'Parallel\n(4 Processes)']
times = [seq_time, par_time]
colors3 = ['#e94560', '#4cc9f0']
x3 = np.arange(len(time_labels))
bars3 = ax3.bar(x3, times, color=colors3, width=0.4, edgecolor='#1a1a2e', linewidth=1.2, zorder=3)
ax3.set_xticks(x3)
ax3.set_xticklabels(time_labels, fontsize=10)
ax3.set_title('Execution Time Comparison', fontsize=12, fontweight='bold', pad=12, color='#4cc9f0')
ax3.set_ylabel('Seconds', fontsize=10)
ax3.grid(axis='y', zorder=0)
ax3.set_axisbelow(True)
for bar, val in zip(bars3, times):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{val:.4f}s', ha='center', fontsize=10, fontweight='bold', color='#ffffff')
ax3.text(0.5, 0.15, f'MPI overhead > benefit at this scale\nSpeedup: {speedup:.2f}x',
         transform=ax3.transAxes, fontsize=9, ha='center', color='#a8a8b3',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#0f3460', edgecolor='#4cc9f0', alpha=0.9))

# Chart 4 — Workload Distribution
ax4 = axes[1, 1]
procs = ['Process 0', 'Process 1', 'Process 2', 'Process 3']
rows = [105138, 105138, 105138, 105137]
colors4 = ['#4cc9f0', '#4361ee', '#7209b7', '#f72585']
x4 = np.arange(len(procs))
bars4 = ax4.bar(x4, rows, color=colors4, width=0.5, edgecolor='#1a1a2e', linewidth=1.2, zorder=3)
ax4.set_xticks(x4)
ax4.set_xticklabels(procs, fontsize=10)
ax4.set_title('Workload Distribution per Process', fontsize=12, fontweight='bold', pad=12, color='#4cc9f0')
ax4.set_ylabel('Rows Processed', fontsize=10)
ax4.set_ylim([105130, 105145])
ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax4.grid(axis='y', zorder=0)
ax4.set_axisbelow(True)
for bar, val in zip(bars4, rows):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:,}', ha='center', fontsize=9, fontweight='bold', color='#ffffff')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/cc/weather-mpi/output/weather_analysis.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print("Chart 1 saved!")

# Speedup Chart
fig2, ax = plt.subplots(figsize=(8, 5))
fig2.patch.set_facecolor('#1a1a2e')
categories = ['Sequential\n(1 Process)', 'Parallel\n(4 Processes)']
times2 = [seq_time, par_time]
colors5 = ['#e94560', '#4cc9f0']
x5 = np.arange(len(categories))
bars5 = ax.bar(x5, times2, color=colors5, width=0.35, edgecolor='#1a1a2e', linewidth=1.2, zorder=3)
ax.set_xticks(x5)
ax.set_xticklabels(categories, fontsize=11)
ax.set_title(f'MPI Speedup Analysis\n420,551 Rows  |  4 Processes  |  Speedup: {speedup:.2f}x',
             fontsize=13, fontweight='bold', color='#e94560', pad=15)
ax.set_ylabel('Execution Time (seconds)', fontsize=11)
ax.grid(axis='y', zorder=0)
ax.set_axisbelow(True)
for bar, val in zip(bars5, times2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{val:.4f}s', ha='center', fontsize=11, fontweight='bold', color='#ffffff')
ax.text(0.5, 0.18,
        'Note: For small datasets, MPI communication overhead\nexceeds computation gain.',
        transform=ax.transAxes, fontsize=9, ha='center', color='#a8a8b3',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f3460', edgecolor='#4cc9f0', alpha=0.9))

plt.tight_layout()
plt.savefig('/home/cc/weather-mpi/output/speedup_analysis.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print("Chart 2 saved!")
print("Done!")
