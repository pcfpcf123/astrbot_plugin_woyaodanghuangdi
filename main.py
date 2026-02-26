import random
from pathlib import Path

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain  # 参考插件导入方式

# ===================== 核心配置 + 内嵌皇帝数据 =====================
CONFIG = {
    # 触发指令（作为@filter.command的别名）
    "trigger_commands": ["我要当皇帝", "抽皇帝", "随机皇帝", "来个皇帝"],
    
    # 回复格式（对齐参考插件的排版风格）
    "reply_format": (
        "🎊 恭喜你抽到【{dynasty}】的皇帝：{emperor}\n"
        "📅 生卒年份：{birthDeath}\n"
        "🏛️ 庙号：{templeName}\n"
        "📜 谥号：{posthumousTitle}\n"
        "📖 核心经历：{experience}"
    ),
    
    # 内嵌皇帝数据
    "emperor_list": [
        {
            "dynasty": "秦朝",
            "emperor": "嬴政（秦始皇）",
            "birthDeath": "前259-前210年",
            "templeName": "无",
            "posthumousTitle": "始皇帝（无正式谥号，后世尊称为秦始皇）",
            "experience": "统一六国，建立中国历史上第一个中央集权大一统封建王朝，首创皇帝制度，推行郡县制，统一文字、货币、度量衡，修筑万里长城与灵渠"
        },
        {
            "dynasty": "秦朝",
            "emperor": "胡亥（秦二世）",
            "birthDeath": "前230-前207年",
            "templeName": "无",
            "posthumousTitle": "无（史称秦二世）",
            "experience": "依靠赵高、李斯篡改遗诏即位，在位期间荒淫无道，横征暴敛，引发秦末农民起义，最终被赵高心腹所杀，秦朝迅速灭亡"
        },
    ]
}

# ===================== 插件核心类（完全对齐参考插件规范） =====================
@register("randomEmperor", "郭圣通", "随机抽取中国历史皇帝", "1.1.0")
class RandomEmperorPlugin(Star):
    def __init__(self, context: Context):
        """初始化插件（对照参考插件的__init__写法）"""
        super().__init__(context)
        self.plugin_dir = Path(__file__).parent  # 插件目录（参考插件的路径规范）
        self.emperor_list = CONFIG["emperor_list"]
        
        # 初始化日志（参考插件的日志风格）
        logger.info("🎲 随机抽皇帝插件 v1.1.0 初始化完成")
        logger.info(f"✅ 加载 {len(self.emperor_list)} 位皇帝数据")

    def get_random_emperor(self):
        """随机抽取一位皇帝（同步工具方法，参考插件的工具方法写法）"""
        if not self.emperor_list:
            logger.error("皇帝数据为空！")
            return None
        return random.choice(self.emperor_list)

    def format_reply(self, emperor_data):
        """格式化回复内容（处理字段默认值）"""
        if not emperor_data:
            return "❌ 皇帝数据加载失败，请联系管理员！"
        
        # 字段默认值（参考插件的容错风格）
        data = {
            "dynasty": emperor_data.get("dynasty", "未知朝代"),
            "emperor": emperor_data.get("emperor", "未知皇帝"),
            "birthDeath": emperor_data.get("birthDeath", "无记录"),
            "templeName": emperor_data.get("templeName", "无记录"),
            "posthumousTitle": emperor_data.get("posthumousTitle", "无记录"),
            "experience": emperor_data.get("experience", "无详细记录")
        }
        return CONFIG["reply_format"].format(**data)

    # ========== 核心指令：抽皇帝（对照参考插件的@filter.command写法） ==========
    @filter.command("我要当皇帝", alias={"抽皇帝", "随机皇帝", "来个皇帝"})
    async def draw_emperor(self, event: AstrMessageEvent):
        """
        随机抽取一位历史皇帝
        触发方式：/我要当皇帝、/抽皇帝、/随机皇帝、/来个皇帝
        """
        # 随机获取皇帝数据
        emperor = self.get_random_emperor()
        reply_text = self.format_reply(emperor)
        
        # 发送回复（参考插件的标准发送方式）
        await event.send(event.plain_result(reply_text))

    # ========== 状态查询指令（对照参考插件的指令写法） ==========
    @filter.command("皇帝抽奖状态", alias={"抽皇帝状态"})
    async def emperor_status(self, event: AstrMessageEvent):
        """查看插件状态和使用说明"""
        status_text = (
            "📋 随机抽皇帝插件状态（v1.1.0）：\n"
            f"├─ 皇帝数据量：{len(self.emperor_list)} 条\n"
            f"├─ 触发指令：/{'、/'.join(CONFIG['trigger_commands'])}\n"
            "├─ 支持朝代：秦朝（可自行扩展）\n"
            "└─ 状态：✅ 正常运行"
        )
        await event.send(event.plain_result(status_text))

    async def terminate(self):
        """插件卸载清理（对照参考插件的terminate写法）"""
        logger.info("🎲 随机抽皇帝插件已卸载/停用")

# 插件启动日志（参考插件的日志风格）
logger.info("""
🎉 AstrBot-随机抽皇帝插件 v1.1.0 加载成功！
✅ 触发指令：/我要当皇帝、/抽皇帝、/随机皇帝、/来个皇帝
✅ 状态查询：/皇帝抽奖状态
✅ 适配版本：AstrBot v4.12.0
""")
