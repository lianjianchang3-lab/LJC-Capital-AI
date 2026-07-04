import pandas as pd
from core.v105.data.live_hub import LiveHub105
from core.v105.lcri.lcri_engine import LCRIEngine105
from core.v105.sector.sector_engine import SectorEngine105

class CommitteeV5:
    def decide(self):
        df = LiveHub105().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待行情数据","votes":[]}
        lcri_df = pd.DataFrame(LCRIEngine105().calculate().get("items",[]))
        lcri_map = dict(zip(lcri_df["code"], lcri_df["LCRI"])) if not lcri_df.empty and "code" in lcri_df.columns else {}
        sector_df = pd.DataFrame(SectorEngine105().rank().get("items",[]))
        sector_map = dict(zip(sector_df["sector"], sector_df["行业热度"])) if not sector_df.empty and "sector" in sector_df.columns else {}
        rows=[]
        for _, r in df.iterrows():
            code=r.get("code"); sector=r.get("sector","未知")
            lcri=float(lcri_map.get(code,0)); hot=float(sector_map.get(sector,0))
            trend=float(r.get("trend",0)); capital=float(r.get("capital",0)); lia=float(r.get("lia",0)); risk=float(r.get("risk",0)); change=float(r.get("change_pct",0)); price=float(r.get("price",0))
            votes=0; reasons=[]
            if lcri>=70: votes+=1; reasons.append("LCRI资金共振")
            if hot>=70: votes+=1; reasons.append("行业热度高")
            if trend>=70 or change>=3: votes+=1; reasons.append("趋势强")
            if capital>=70: votes+=1; reasons.append("机构评分高")
            if lia>=70: votes+=1; reasons.append("LIA强")
            if risk<=55: votes+=1; reasons.append("风险可控")
            if votes>=5:
                decision="重点买入关注"; pos="10%-18%"; star="★★★★★"
            elif votes==4:
                decision="买入观察"; pos="6%-12%"; star="★★★★"
            elif votes==3:
                decision="小仓观察"; pos="3%-6%"; star="★★★"
            elif risk>=75 or change<=-5:
                decision="风险回避"; pos="0%"; star="★"
            else:
                decision="继续观察"; pos="0%-3%"; star="★★"
            rows.append({"代码":code,"名称":r.get("name"),"行业":sector,"现价":price,"涨跌幅":change,"LCRI":round(lcri,1),"行业热度":round(hot,1),"投票数":votes,"星级":star,"最终决策":decision,"建议仓位":pos,"风险":risk,"理由":"、".join(reasons) if reasons else "信号不足"})
        rows=sorted(rows,key=lambda x:(x["投票数"],x["LCRI"],x["行业热度"]),reverse=True)
        return {"status":"OK","summary":f"投委会V5完成：{len(rows)}只，重点买入关注{sum(1 for x in rows if x['最终决策']=='重点买入关注')}只。","votes":rows}
