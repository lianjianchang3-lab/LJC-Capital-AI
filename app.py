import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from apps.cockpit import render_cockpit

st.set_page_config(page_title="LJC Capital AI Pro V8.5 Final", page_icon="🛫", layout="wide")
render_cockpit()
