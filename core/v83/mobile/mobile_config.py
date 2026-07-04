class MobileConfig:
    def guide(self):
        return {
            "local_mobile": [
                "确保手机和电脑在同一个Wi-Fi",
                "电脑运行：streamlit run apps/v83_build500_ai_decision.py --server.address 0.0.0.0",
                "在电脑终端查看 Network URL",
                "手机浏览器打开 Network URL"
            ],
            "cloud_mobile": [
                "提交代码到 GitHub",
                "Streamlit Cloud 连接仓库",
                "入口文件选择 apps/v83_build500_ai_decision.py",
                "部署后手机直接打开云端网址"
            ]
        }
