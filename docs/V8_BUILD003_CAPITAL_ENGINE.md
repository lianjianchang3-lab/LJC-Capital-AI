# V8 Build003 Capital Engine

## Added

- CapitalEngine
- CapitalSignal schema
- Capital Health
- Institution Score
- Capital Confidence
- Capital Stage
- Trend symbol
- Capital dashboard

## API

```python
from core.capital import CapitalEngine

engine = CapitalEngine()
engine.analyze("300136")
engine.analyze_all()
```

## Acceptance

- `streamlit run app.py` starts.
- Capital Engine table is visible.
- Each watchlist stock has capital health / institution score / stage.
