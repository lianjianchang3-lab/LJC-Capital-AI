# V8 Build002 Data Center MVP

## Added

- DataCenter unified API
- CSVProvider
- DataQuality / DataResult schema
- watchlist / quotes / capital / sector / news CSV fallback
- Data Center dashboard in Streamlit

## API

```python
from core.data_center import DataCenter

dc = DataCenter()
dc.get_quotes()
dc.get_capital()
dc.get_sector()
dc.get_news()
```

## Acceptance

- `streamlit run app.py` starts.
- Data Center quality metrics are visible.
- Watchlist / Quotes / Capital / Sector tables are visible.
