from dataclasses import dataclass, field
from typing import List


@dataclass
class StockAnalysisResult:
    """
    LJC Capital AI
    股票统一分析结果
    """

    # 基本信息
    code: str
    name: str

    # 综合评分
    ai_score: float = 0

    # 五大核心指数（后续逐步实现）
    bei: float = 0      # 爆发指数
    cri: float = 0      # 资金共振指数
    ici: float = 0      # 机构信心指数
    smi: float = 0      # 聪明资金指数
    rri: float = 0      # 风险收益指数

    # 综合结论
    recommendation: str = "观察"

    # 价格建议
    target_price: float = 0
    stop_loss: float = 0

    # 证据链
    evidence: List[str] = field(default_factory=list)