from mpi4py import MPI
import pandas as pd
import time
import json

# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()   # which process am i? (0,1,2,3)
size = comm.Get_size()   # total how many processes?

DATA_PATH = '/home/cc/weather-mpi/data/weather_clean.csv'

# ── SEQUENTIAL (only root, for comparison) ──────────────────
if rank == 0:
    print(f"\n{'='*50}")
    print(f"Running with {size} MPI processes")
    print(f"{'='*50}")

    # Sequential timing
    seq_start = time.time()
    df_full = pd.read_csv(DATA_PATH)
    seq_stats = {
        'avg_temp'     : df_full['temperature'].mean(),
        'max_temp'     : df_full['temperature'].max(),
        'min_temp'     : df_full['temperature'].min(),
        'avg_humidity' : df_full['humidity'].mean(),
        'avg_wind'     : df_full['wind_speed'].mean(),
        'max_wind'     : df_full['wind_speed'].max(),
    }
    seq_time = time.time() - seq_start
    print(f"\nSequential time : {seq_time:.4f} seconds")

# ── PARALLEL ────────────────────────────────────────────────
comm.Barrier()   # all processes wait here together
par_start = time.time()

chunks = None
if rank == 0:
    df = pd.read_csv(DATA_PATH)
    # split into equal chunks for each process
    chunks = [df[i::size] for i in range(size)]

# scatter: root sends each process its chunk
local_chunk = comm.scatter(chunks, root=0)

# each process computes its own local stats
local_stats = {
    'avg_temp'     : local_chunk['temperature'].mean(),
    'max_temp'     : local_chunk['temperature'].max(),
    'min_temp'     : local_chunk['temperature'].min(),
    'avg_humidity' : local_chunk['humidity'].mean(),
    'avg_wind'     : local_chunk['wind_speed'].mean(),
    'max_wind'     : local_chunk['wind_speed'].max(),
    'count'        : len(local_chunk),
}

print(f"  Process {rank} → processed {local_stats['count']:,} rows")

# gather: all processes send results back to root
all_stats = comm.gather(local_stats, root=0)

# root combines everything
if rank == 0:
    par_time = time.time() - par_start

    # combine results from all processes
    final = {
        'avg_temp'     : sum(s['avg_temp'] * s['count'] for s in all_stats) / sum(s['count'] for s in all_stats),
        'max_temp'     : max(s['max_temp'] for s in all_stats),
        'min_temp'     : min(s['min_temp'] for s in all_stats),
        'avg_humidity' : sum(s['avg_humidity'] * s['count'] for s in all_stats) / sum(s['count'] for s in all_stats),
        'avg_wind'     : sum(s['avg_wind'] * s['count'] for s in all_stats) / sum(s['count'] for s in all_stats),
        'max_wind'     : max(s['max_wind'] for s in all_stats),
    }

    print(f"\nParallel time   : {par_time:.4f} seconds")
    print(f"Speedup         : {seq_time/par_time:.2f}x faster")

    print(f"\n{'='*50}")
    print("FINAL RESULTS")
    print(f"{'='*50}")
    print(f"Average Temperature : {final['avg_temp']:.2f} °C")
    print(f"Max Temperature     : {final['max_temp']:.2f} °C")
    print(f"Min Temperature     : {final['min_temp']:.2f} °C")
    print(f"Average Humidity    : {final['avg_humidity']:.2f} %")
    print(f"Average Wind Speed  : {final['avg_wind']:.2f} m/s")
    print(f"Max Wind Speed      : {final['max_wind']:.2f} m/s")

    # save results for visualize.py
    results = {
        'final_stats' : final,
        'seq_time'    : seq_time,
        'par_time'    : par_time,
        'speedup'     : seq_time / par_time,
        'num_processes': size,
    }
    with open('/home/cc/weather-mpi/output/results.json', 'w') as f:
        json.dump(results, f)
    print(f"\nResults saved to output/results.json")
