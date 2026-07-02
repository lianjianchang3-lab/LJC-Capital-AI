class ResearchWatchEngine:
    """
    长期关注股中心。
    当前内置你长期关注股票；后续可从 database/research_watchlist.json 读取。
    """

    def load_watchlist(self):
        return [
            {"code": "300136", "name": "信维通信", "theme": "商业航天/AI基础设施", "base_lcri": 94, "risk": 18},
            {"code": "300762", "name": "上海瀚讯", "theme": "商业航天/军工通信", "base_lcri": 95, "risk": 20},
            {"code": "603308", "name": "应流股份", "theme": "商业航天/高端制造", "base_lcri": 89, "risk": 26},
            {"code": "688008", "name": "澜起科技", "theme": "AI基础设施/半导体", "base_lcri": 91, "risk": 22},
            {"code": "688387", "name": "信科移动", "theme": "卫星通信/通信设备", "base_lcri": 88, "risk": 30},
            {"code": "300342", "name": "天银机电", "theme": "商业航天/军工电子", "base_lcri": 84, "risk": 36},
            {"code": "688568", "name": "中科星图", "theme": "商业航天/卫星应用", "base_lcri": 83, "risk": 34},
            {"code": "600879", "name": "航天电子", "theme": "商业航天/军工", "base_lcri": 82, "risk": 38},
            {"code": "600391", "name": "航发科技", "theme": "航空发动机", "base_lcri": 80, "risk": 40},
            {"code": "301021", "name": "英诺激光", "theme": "激光/高端制造", "base_lcri": 79, "risk": 42},
            {"code": "300058", "name": "蓝色光标", "theme": "AI应用", "base_lcri": 78, "risk": 46},
            {"code": "000426", "name": "兴业银锡", "theme": "资源", "base_lcri": 77, "risk": 44},
            {"code": "600301", "name": "华锡有色", "theme": "资源", "base_lcri": 76, "risk": 45},
        ]
