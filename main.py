import random
from pathlib import Path

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter, MessageEventResult
from astrbot.api.star import Context, Star, register

# ===================== 核心配置（扩展触发词） =====================
CONFIG = {
    # 扩展触发词列表（支持自然语言，不用/前缀）
    "trigger_keywords": [
        "我要当皇帝", "抽皇帝", "随机皇帝", "来个皇帝",
        "朕要登基", "选个皇帝", "随机抽皇帝", "来一位皇帝"
    ],
    
    # 回复格式
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

# ===================== 插件核心类（支持自然语言触发） =====================
@register("randomEmperor", "郭圣通", "随机抽取中国历史皇帝", "1.1.0")
class RandomEmperorPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.plugin_dir = Path(__file__).parent
        self.emperor_list = CONFIG["emperor_list"]
        self.trigger_keywords = CONFIG["trigger_keywords"]
        
        logger.info("🎲 随机抽皇帝插件 v1.1.0 初始化完成")
        logger.info(f"✅ 加载 {len(self.emperor_list)} 位皇帝数据")
        logger.info(f"✅ 支持触发词：{', '.join(self.trigger_keywords)}")

    def get_random_emperor(self):
        """随机抽取一位皇帝"""
        if not self.emperor_list:
            logger.error("皇帝数据为空！")
            return None
        return random.choice(self.emperor_list)

    def format_reply(self, emperor_data):
        """格式化回复内容"""
        if not emperor_data:
            return "❌ 皇帝数据加载失败，请联系管理员！"
        
        data = {
            "dynasty": emperor_data.get("dynasty", "未知朝代"),
            "emperor": emperor_data.get("emperor", "未知皇帝"),
            "birthDeath": emperor_data.get("birthDeath", "无记录"),
            "templeName": emperor_data.get("templeName", "无记录"),
            "posthumousTitle": emperor_data.get("posthumousTitle", "无记录"),
            "experience": emperor_data.get("experience", "无详细记录")
        }
        return CONFIG["reply_format"].format(**data)

    def is_trigger(self, message: str):
        """判断消息是否包含触发词（忽略大小写/空格）"""
        if not message:
            return False
        msg = message.strip().lower()
        # 匹配任意触发词（忽略大小写）
        return any(keyword.lower() in msg for keyword in self.trigger_keywords)

    # ========== 核心：监听所有消息，支持自然语言触发 ==========
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        监听所有消息（自然语言触发核心）
        返回 MessageEventResult(True) 阻止AI后续处理，彻底去掉多余回复
        """
        # 只处理群/私聊消息，忽略机器人自己发的
        if event.is_self():
            return MessageEventResult(False)
        
        # 获取用户消息（纯文本）
        msg_text = event.message_str.strip()
        
        # 匹配触发词 → 回复并阻止AI抢话
        if self.is_trigger(msg_text):
            emperor = self.get_random_emperor()
            reply_text = self.format_reply(emperor)
            # 发送回复
            await event.send(event.plain_result(reply_text))
            # 返回 True 阻止AI继续处理这条消息（关键！去掉多余回复）
            return MessageEventResult(True)
        
        # 不匹配触发词 → 交给其他插件/AI处理
        return MessageEventResult(False)

    # ========== 保留/指令触发（兼容旧习惯） ==========
    @filter.command("我要当皇帝", alias={"抽皇帝", "随机皇帝", "来个皇帝"})
    async def draw_emperor(self, event: AstrMessageEvent):
        """随机抽取一位历史皇帝（/指令触发）"""
        emperor = self.get_random_emperor()
        reply_text = self.format_reply(emperor)
        await event.send(event.plain_result(reply_text))

    @filter.command("皇帝抽奖状态")
    async def emperor_status(self, event: AstrMessageEvent):
        """查看插件状态"""
        status_text = (
            "📋 随机抽皇帝插件状态（v1.1.0）：\n"
            f"├─ 皇帝数据量：{len(self.emperor_list)} 条\n"
            f"├─ 自然语言触发词：{', '.join(self.trigger_keywords)}\n"
            f"├─ /指令触发：/{'、/'.join(self.trigger_keywords[:4])}\n"
            "└─ 状态：✅ 正常运行"
        )
        await event.send(event.plain_result(status_text))

    async def terminate(self):
        logger.info("🎲 随机抽皇帝插件已卸载")

# 启动日志
logger.info("""
🎉 AstrBot-随机抽皇帝插件 v1.1.0 加载成功！
✅ 自然语言触发：直接发「我要当皇帝」「来个皇帝」等
✅ /指令触发：/我要当皇帝、/抽皇帝
✅ 状态查询：/皇帝抽奖状态
✅ 已开启防AI抢话，无多余回复！
""")
