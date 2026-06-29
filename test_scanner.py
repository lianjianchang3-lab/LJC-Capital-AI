from src.data.datasource import DataSource
from analysis.scanner_engine import ScannerEngine

ds = DataSource()

stock_list = ds.get_stock_list()

scanner = ScannerEngine(stock_list)

top20 = scanner.scan_top20()

print("=" * 60)
print("LJC Capital AI 今日爆发榜 TOP20")
print("=" * 60)

print(top20)