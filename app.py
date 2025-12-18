import streamlit as st
import os
import re
from datetime import datetime
import pandas as pd

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_LOG_DIR = os.path.join(BASE_DIR,"log")

st.set_page_config(page_title="Pipeline Monitoring", layout="wide")
#st.title("Pipeline Monitoring Dashboard")

# ----------------------------------------------------
# Utility: Safe directory listing
# ----------------------------------------------------
def safe_list_dirs(path):
    """Return list of directories inside path; never crash."""
    if not os.path.exists(path):
        return []

    try:
        return [ 
            os.path.join(path, d)
            for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d))
        ]
    except:
        return []

# ----------------------------------------------------
# Utility: Safe file list
# ----------------------------------------------------
def list_log_files(pipeline_dir):
    """List all .log files sorted newest → oldest."""
    try:
        logs = [
            f for f in os.listdir(pipeline_dir)
            if f.endswith(".log") and os.path.isfile(os.path.join(pipeline_dir, f))
        ]
        return sorted(logs, reverse=True)
    except:
        return []

# ----------------------------------------------------
# PARSER: Extract detailed metadata from logs
# ----------------------------------------------------
def parse_log_details(log_path):
    """
    Parse a log and extract:
    - status (success/fail/running)
    - etl_name
    - start timestamp
    - rolling window
    - error count
    - traceback chunks
    - end timestamp
    """
    details = {
        "etl": None,
        "status": "unknown",
        "start_time": None,
        "rolling_window": None,
        "error_count": 0,
        "tracebacks": [],
        "end_time": None,
        "runtime": None
    }

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return details

    traceback_buffer = []
    in_traceback = False

    for line in lines:

        # Parse ETL name
        if "INFO Starting" in line:
            m = re.search(r"Starting\s+(\w+)", line)
            if m:
                details["etl"] = m.group(1)

        # Capture start time
        if details["start_time"] is None:
            ts_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            if ts_match:
                details["start_time"] = ts_match.group(1)
        
        # Capture end time
        ts_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
        if ts_match:
            details["end_time"] = ts_match.group(1)

        # Rolling window 
        if "Rolling Window" in line:
            details["rolling_window"] = line.split("Rolling Window:")[-1].strip()

        # ERROR detection
        if "ERROR" in line:
            details["status"] = "fail"
            details["error_count"] += 1
            in_traceback = True
            traceback_buffer = []
            continue

        # Capture traceback
        if in_traceback:
            if line.strip() == "":
                if traceback_buffer:
                    details["tracebacks"].append("".join(traceback_buffer))
                in_traceback = False
            else:
                traceback_buffer.append(line)



    # flush last traceback
    if traceback_buffer:
        details["tracebacks"].append("".join(traceback_buffer))

    #Calcuate runtime (completed_in)
    if details["start_time"] and details["end_time"]:
        start_dt = datetime.strptime(details["start_time"], "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(details["end_time"], "%Y-%m-%d %H:%M:%S")
        #details["runtime"] = (end_dt - start_dt).total_seconds()
        details["runtime"] = round((end_dt - start_dt).total_seconds() / 60.0, 2)

    # No explicit errors → detect success
    if details["status"] != "fail":
        if any("Inserted" in l or "All records inserted" in l for l in lines):
            details["status"] = "success"
        else:
            details["status"] = "running"  # incomplete run

    return details
    

# UI: Load pipeline directories safely
pipeline_dirs = safe_list_dirs(BASE_LOG_DIR)

if not pipeline_dirs:
    st.error(f"No pipeline directories found under: `{BASE_LOG_DIR}`")
    st.stop()

pipeline_names = [os.path.basename(p) for p in pipeline_dirs]

# SECTION 1 — PIPELINE STATUS OVERVIEW
st.subheader("📊 Pipeline Status Overview")
#show summary table in table view
pipeline_rows = []
for pdir in pipeline_dirs:
    logs = list_log_files(pdir)

    if logs:
        latest_log = logs[0]
        log_path = os.path.join(pdir, latest_log)
        meta = parse_log_details(log_path)
        last_run = datetime.fromtimestamp(os.path.getmtime(log_path)).strftime("%Y-%m-%d %H:%M:%S")
        runtime = meta.get("runtime") if meta.get("runtime") else "N/A"
        #rolling window to strip date only
        rollng_window = meta.get("rolling_window") if meta.get("rolling_window") else "N/A"
    else:
        meta = {"status": "No Logs", "etl": None}
        last_run = "N/A"
        # ensure these variables exist when there are no logs
        runtime = None
        rollng_window = "N/A"
    emoji_status = {"success": "🟢", 
                    "fail": "🔴", 
                    "running": "🟠"}.get(meta["status"], "⚪")
    pipeline_rows.append({
        "Pipeline": os.path.basename(pdir),
        "Status": f"{emoji_status} {meta['status']}",
        "Last Run": last_run,
        "Completed In (min)": runtime,
        "Rolling Window": rollng_window
    })
df=pd.DataFrame(pipeline_rows)
df.index=df.index + 1
st.table(df)

# SECTION 2 — LOG EXPLORER
st.subheader("📚 Pipeline Log Explorer")

pipeline_selected = st.selectbox(
    "Select a pipeline",
    options=pipeline_names if pipeline_names else ["(none)"],
)

if not pipeline_selected or pipeline_selected == "(none)":
    st.stop()

selected_pipeline_dir = os.path.join(BASE_LOG_DIR, pipeline_selected)
logs = list_log_files(selected_pipeline_dir)

if not logs:
    st.warning(f"No log files found for `{pipeline_selected}`.")
    st.stop()

log_selected = st.selectbox("Select log file", logs)

file_path = os.path.join(selected_pipeline_dir, log_selected)

# Display Log Metadata (parsed)

meta = parse_log_details(file_path)

st.subheader("📌 Log Metadata")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**ETL:** `{meta['etl']}`")
    st.write(f"**Start Time:** `{meta['start_time']}`")
    st.write(f"**Rolling Window:** `{meta['rolling_window']}`")

with col2: 
    st.write(f"**Status:** `{meta['status']}`")
    st.write(f"**Error Count:** `{meta['error_count']}`")


# Show Tracebacks

if meta["tracebacks"]:
    st.subheader("🔻 Tracebacks")
    for tb in meta["tracebacks"]:
        st.code(tb, language="python")

# Show tail of log

st.subheader("📄 Log Preview")

tail_n = 10

try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        preview = "".join(lines[-tail_n:])
        st.code(preview, language="bash")
except Exception as e:
    st.error(f"Failed to read log: {e}")


