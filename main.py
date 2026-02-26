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
        { 
            "dynasty": "西汉", 
            "emperor": "刘邦（汉高祖）",
            "birthDeath": "前256-前195年",
            "templeName": "太祖",
            "posthumousTitle": "高皇帝",
            "experience": "西汉开国皇帝，秦末起兵反秦，后与项羽展开楚汉争霸并获胜，建立西汉王朝，推行休养生息政策，减轻百姓负担，奠定西汉百年基业"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘盈（汉惠帝）",
            "birthDeath": "前210-前188年",
            "templeName": "惠宗（后被废）",
            "posthumousTitle": "孝惠皇帝",
            "experience": "西汉第二位皇帝，性格仁弱，在位期间由吕后临朝称制，继续推行休养生息政策，萧规曹随，维持西汉稳定发展"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘恒（汉文帝）",
            "birthDeath": "前203-前157年",
            "templeName": "太宗",
            "posthumousTitle": "孝文皇帝",
            "experience": "西汉第五位皇帝，平定诸吕之乱后即位，厉行节俭，轻徭薄赋，与民休息，开创“文景之治”，为汉武帝盛世奠定物质基础"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘启（汉景帝）",
            "birthDeath": "前188-前141年",
            "templeName": "孝景皇帝（无庙号，后世尊称为汉景帝）",
            "posthumousTitle": "孝景皇帝",
            "experience": "西汉第六位皇帝，延续汉文帝休养生息政策，平定“七国之乱”，巩固中央集权，与汉文帝共同开创“文景之治”"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘彻（汉武帝）",
            "birthDeath": "前156-前87年",
            "templeName": "世宗",
            "posthumousTitle": "孝武皇帝",
            "experience": "西汉第七位皇帝，雄才大略，罢黜百家、独尊儒术，开疆拓土，北击匈奴、西通西域、南征百越，开创西汉鼎盛时代，晚年发布《轮台罪己诏》反思施政"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘弗陵（汉昭帝）",
            "birthDeath": "前94-前74年",
            "templeName": "昭宗（后被废）",
            "posthumousTitle": "孝昭皇帝",
            "experience": "西汉第八位皇帝，幼年即位，由霍光辅政，轻徭薄赋，与民休息，平定上官桀叛乱，维持西汉稳定，为“昭宣中兴”奠定基础"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘询（汉宣帝）",
            "birthDeath": "前91-前49年",
            "templeName": "中宗",
            "posthumousTitle": "孝宣皇帝",
            "experience": "西汉第十位皇帝，幼时流落民间，即位后清除霍氏势力，励精图治，轻徭薄赋，大破匈奴，设立西域都护府，开创“昭宣中兴”"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘奭（汉元帝）",
            "birthDeath": "前74-前33年",
            "templeName": "高宗（后被废）",
            "posthumousTitle": "孝元皇帝",
            "experience": "西汉第十一位皇帝，性格柔弱，重用宦官，朝政日益腐败，西汉由盛转衰，期间昭君出塞，维持与匈奴的和平关系"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘骜（汉成帝）",
            "birthDeath": "前51-前7年",
            "templeName": "统宗（后被废）",
            "posthumousTitle": "孝成皇帝",
            "experience": "西汉第十二位皇帝，荒淫无道，沉迷酒色，重用外戚王氏，王氏势力日益膨胀，为王莽篡汉埋下隐患"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘欣（汉哀帝）",
            "birthDeath": "前25-前1年",
            "templeName": "哀宗（后被废）",
            "posthumousTitle": "孝哀皇帝",
            "experience": "西汉第十三位皇帝，在位期间试图限制外戚与宦官势力，未果，沉迷男色，朝政混乱，西汉统治进一步衰落"
        },
        { 
            "dynasty": "西汉", 
            "emperor": "刘衎（汉平帝）",
            "birthDeath": "前9-5年",
            "templeName": "元宗（后被废）",
            "posthumousTitle": "孝平皇帝",
            "experience": "西汉第十四位皇帝，幼年即位，由王莽辅政，实为傀儡皇帝，最终被王莽毒杀，西汉名存实亡"
        },
        { 
            "dynasty": "新朝", 
            "emperor": "王莽",
            "birthDeath": "前45-23年",
            "templeName": "无",
            "posthumousTitle": "无（史称新莽）",
            "experience": "篡汉建立新朝，推行“王莽改制”，试图解决西汉末年社会矛盾，因政策脱离实际引发天下大乱，最终被绿林军所杀，新朝灭亡"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘秀（汉光武帝）",
            "birthDeath": "前6-57年",
            "templeName": "世祖",
            "posthumousTitle": "光武皇帝",
            "experience": "东汉开国皇帝，参加绿林军推翻新莽，后平定各路割据势力，统一全国，开创“光武中兴”，整顿吏治，轻徭薄赋，恢复社会生产"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘庄（汉明帝）",
            "birthDeath": "28-75年",
            "templeName": "显宗",
            "posthumousTitle": "孝明皇帝",
            "experience": "东汉第二位皇帝，励精图治，严明吏治，派班超出使西域，恢复汉朝对西域的控制，修建白马寺，促进佛教传播"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘炟（汉章帝）",
            "birthDeath": "57-88年",
            "templeName": "肃宗",
            "posthumousTitle": "孝章皇帝",
            "experience": "东汉第三位皇帝，延续明章之治，轻徭薄赋，重视儒学，与汉明帝共同开创“明章之治”，后期外戚势力开始抬头"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘肇（汉和帝）",
            "birthDeath": "79-105年",
            "templeName": "穆宗（后被废）",
            "posthumousTitle": "孝和皇帝",
            "experience": "东汉第四位皇帝，幼年即位，由窦太后临朝，后诛杀窦氏势力亲政，励精图治，东汉国力达到鼎盛，史称“永元之隆”"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘隆（汉殇帝）",
            "birthDeath": "105-106年",
            "templeName": "无",
            "posthumousTitle": "孝殇皇帝",
            "experience": "中国历史上年龄最小的皇帝，即位时仅百天，在位仅8个月便夭折，是东汉最短命的皇帝"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘祜（汉安帝）",
            "birthDeath": "94-125年",
            "templeName": "恭宗（后被废）",
            "posthumousTitle": "孝安皇帝",
            "experience": "东汉第六位皇帝，依赖外戚与宦官掌权，朝政混乱，西域控制权丧失，东汉国力开始衰退"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘保（汉顺帝）",
            "birthDeath": "115-144年",
            "templeName": "敬宗（后被废）",
            "posthumousTitle": "孝顺皇帝",
            "experience": "东汉第七位皇帝，由宦官拥立即位，宦官势力自此崛起，朝政日益腐败，东汉统治进一步衰落"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘炳（汉冲帝）",
            "birthDeath": "143-145年",
            "templeName": "无",
            "posthumousTitle": "孝冲皇帝",
            "experience": "东汉第八位皇帝，3岁即位，在位仅半年便病逝，由外戚梁氏掌控朝政"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘缵（汉质帝）",
            "birthDeath": "138-146年",
            "templeName": "无",
            "posthumousTitle": "孝质皇帝",
            "experience": "东汉第九位皇帝，因直言斥责权臣梁冀“跋扈”，被梁冀毒杀，年仅9岁"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘志（汉桓帝）",
            "birthDeath": "132-167年",
            "templeName": "威宗（后被废）",
            "posthumousTitle": "孝桓皇帝",
            "experience": "东汉第十位皇帝，依靠宦官诛灭梁冀势力，后纵容宦官乱政，引发“党锢之祸”，东汉统治岌岌可危"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘宏（汉灵帝）",
            "birthDeath": "156-189年",
            "templeName": "无",
            "posthumousTitle": "孝灵皇帝",
            "experience": "东汉第十一位皇帝，卖官鬻爵，荒淫无道，横征暴敛，引发黄巾起义，东汉名存实亡"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘辩（汉少帝）",
            "birthDeath": "176-190年",
            "templeName": "无",
            "posthumousTitle": "无（史称汉少帝）",
            "experience": "东汉第十二位皇帝，由何太后与何进掌控，后被董卓废黜并毒杀，东汉皇权彻底旁落"
        },
        { 
            "dynasty": "东汉", 
            "emperor": "刘协（汉献帝）",
            "birthDeath": "181-234年",
            "templeName": "无",
            "posthumousTitle": "孝献皇帝",
            "experience": "东汉末代皇帝，一生受制于董卓、曹操等权臣，220年禅位于曹丕，东汉灭亡，后被封为山阳公，善终"
        },
        { 
            "dynasty": "曹魏", 
            "emperor": "曹丕（魏文帝）",
            "birthDeath": "187-226年",
            "templeName": "世祖",
            "posthumousTitle": "文皇帝",
            "experience": "曹魏开国皇帝，曹操次子，篡汉建魏，推行九品中正制，奠定曹魏政治基础，擅长文学，与曹操、曹植并称“三曹”"
        },
        { 
            "dynasty": "曹魏", 
            "emperor": "曹叡（魏明帝）",
            "birthDeath": "204-239年",
            "templeName": "烈祖",
            "posthumousTitle": "明皇帝",
            "experience": "曹魏第二位皇帝，前期励精图治，稳固曹魏统治，后期沉迷享乐，托孤不当，导致司马懿势力崛起"
        },
        { 
            "dynasty": "曹魏", 
            "emperor": "曹芳（魏少帝）",
            "birthDeath": "232-274年",
            "templeName": "无",
            "posthumousTitle": "邵陵厉公",
            "experience": "曹魏第三位皇帝，幼年即位，由曹爽与司马懿辅政，后司马懿发动“高平陵之变”掌控朝政，曹芳被废黜"
        },
        { 
            "dynasty": "曹魏", 
            "emperor": "曹髦（魏高贵乡公）",
            "birthDeath": "241-260年",
            "templeName": "无",
            "posthumousTitle": "无（史称高贵乡公）",
            "experience": "曹魏第四位皇帝，不甘沦为司马氏傀儡，率宫人讨伐司马昭，最终被司马昭心腹所杀，曹魏名存实亡"
        },
        { 
            "dynasty": "曹魏", 
            "emperor": "曹奂（魏元帝）",
            "birthDeath": "246-302年",
            "templeName": "元皇帝",
            "posthumousTitle": "孝元皇帝",
            "experience": "曹魏末代皇帝，司马氏傀儡，265年禅位于司马炎，西晋建立，后被封为陈留王，善终"
        },
        { 
            "dynasty": "蜀汉", 
            "emperor": "刘备（汉昭烈帝）",
            "birthDeath": "161-223年",
            "templeName": "烈祖",
            "posthumousTitle": "昭烈皇帝",
            "experience": "蜀汉开国皇帝，自称中山靖王之后，颠沛流离半生，后联合孙权在赤壁之战击败曹操，占据益州建立蜀汉，夷陵之战兵败后病逝白帝城"
        },
        { 
            "dynasty": "蜀汉", 
            "emperor": "刘禅（汉怀帝）",
            "birthDeath": "207-271年",
            "templeName": "无",
            "posthumousTitle": "孝怀皇帝",
            "experience": "蜀汉末代皇帝，小名阿斗，诸葛亮辅政期间维持蜀汉稳定，诸葛亮去世后宠信宦官，263年蜀汉被曹魏所灭，被俘后“乐不思蜀”，善终"
        },
        { 
            "dynasty": "东吴", 
            "emperor": "孙权（吴大帝）",
            "birthDeath": "182-252年",
            "templeName": "太祖",
            "posthumousTitle": "大皇帝",
            "experience": "东吴开国皇帝，继承父兄基业，占据江东，与刘备联合在赤壁之战击败曹操，后偷袭荆州杀死关羽，与曹魏对峙，晚年猜忌滥杀，东吴国力衰退"
        },
        { 
            "dynasty": "东吴", 
            "emperor": "孙亮（吴少帝）",
            "birthDeath": "243-260年",
            "templeName": "无",
            "posthumousTitle": "会稽王",
            "experience": "东吴第二位皇帝，幼年即位，由诸葛恪辅政，后试图诛杀权臣孙綝，被孙綝废黜，后自杀身亡"
        },
        { 
            "dynasty": "东吴", 
            "emperor": "孙休（吴景帝）",
            "birthDeath": "235-264年",
            "templeName": "太宗",
            "posthumousTitle": "景皇帝",
            "experience": "东吴第三位皇帝，联合丁奉诛杀孙綝，整顿朝政，试图恢复东吴国力，可惜英年早逝"
        },
        { 
            "dynasty": "东吴", 
            "emperor": "孙皓（吴末帝）",
            "birthDeath": "242-284年",
            "templeName": "无",
            "posthumousTitle": "无（史称吴末帝）",
            "experience": "东吴末代皇帝，残暴嗜杀，荒淫无道，横征暴敛，280年西晋灭吴，孙皓被俘，东吴灭亡"
        },
        { 
            "dynasty": "西晋", 
            "emperor": "司马炎（晋武帝）",
            "birthDeath": "236-290年",
            "templeName": "世祖",
            "posthumousTitle": "武皇帝",
            "experience": "西晋开国皇帝，司马懿之孙，篡魏建晋，280年灭吴统一全国，推行“占田制”，后期沉迷享乐，分封诸王，为“八王之乱”埋下隐患"
        },
        { 
            "dynasty": "西晋", 
            "emperor": "司马衷（晋惠帝）",
            "birthDeath": "259-307年",
            "templeName": "无",
            "posthumousTitle": "惠皇帝",
            "experience": "西晋第二位皇帝，智力低下，“何不食肉糜”出自其口，在位期间爆发“八王之乱”，西晋统治崩溃，后被毒杀"
        },
        { 
            "dynasty": "西晋", 
            "emperor": "司马炽（晋怀帝）",
            "birthDeath": "284-313年",
            "templeName": "无",
            "posthumousTitle": "怀皇帝",
            "experience": "西晋第三位皇帝，在位期间西晋已名存实亡，匈奴刘聪攻破洛阳，司马炽被俘，后被毒杀"
        },
        { 
            "dynasty": "西晋", 
            "emperor": "司马邺（晋愍帝）",
            "birthDeath": "300-317年",
            "templeName": "无",
            "posthumousTitle": "愍皇帝",
            "experience": "西晋末代皇帝，在长安即位，后匈奴刘曜攻破长安，司马邺被俘，西晋灭亡，后被杀害"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马睿（晋元帝）",
            "birthDeath": "276-323年",
            "templeName": "中宗",
            "posthumousTitle": "元皇帝",
            "experience": "东晋开国皇帝，依赖王导等门阀士族在江南建立政权，史称“王与马共天下”，后期受制于王敦，忧郁而死"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马绍（晋明帝）",
            "birthDeath": "299-325年",
            "templeName": "肃宗",
            "posthumousTitle": "明皇帝",
            "experience": "东晋第二位皇帝，聪慧果决，平定王敦之乱，稳固东晋根基，可惜英年早逝"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马衍（晋成帝）",
            "birthDeath": "321-342年",
            "templeName": "显宗",
            "posthumousTitle": "成皇帝",
            "experience": "东晋第三位皇帝，幼年即位，由庾太后临朝，门阀争斗持续，在位期间维持东晋偏安局面"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马岳（晋康帝）",
            "birthDeath": "322-344年",
            "templeName": "无",
            "posthumousTitle": "康皇帝",
            "experience": "东晋第四位皇帝，在位仅2年，无显著作为，传位于弟弟司马聃"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马聃（晋穆帝）",
            "birthDeath": "343-361年",
            "templeName": "孝宗",
            "posthumousTitle": "穆皇帝",
            "experience": "东晋第五位皇帝，幼年即位，由褚太后临朝，桓温渐掌实权，在位期间桓温北伐，收复部分失地"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马丕（晋哀帝）",
            "birthDeath": "341-365年",
            "templeName": "无",
            "posthumousTitle": "哀皇帝",
            "experience": "东晋第六位皇帝，沉迷炼丹求仙，不理朝政，早逝，在位期间东晋国力继续衰退"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马奕（晋废帝）",
            "birthDeath": "342-386年",
            "templeName": "无",
            "posthumousTitle": "海西公",
            "experience": "东晋第七位皇帝，被桓温废黜，后善终，东晋皇权进一步弱化"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马昱（晋简文帝）",
            "birthDeath": "320-372年",
            "templeName": "太宗",
            "posthumousTitle": "简文皇帝",
            "experience": "东晋第八位皇帝，桓温拥立的傀儡皇帝，在位仅8个月，忧郁病逝"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马曜（晋孝武帝）",
            "birthDeath": "362-396年",
            "templeName": "烈宗",
            "posthumousTitle": "孝武皇帝",
            "experience": "东晋第九位皇帝，前期倚重谢安，取得淝水之战胜利，后期沉迷酒色，被妃嫔所杀，东晋统治日益混乱"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马德宗（晋安帝）",
            "birthDeath": "382-419年",
            "templeName": "无",
            "posthumousTitle": "安皇帝",
            "experience": "东晋第十位皇帝，智力低下，朝政被桓玄、刘裕先后掌控，在位期间桓玄篡晋，后刘裕平定桓玄，掌控东晋大权"
        },
        { 
            "dynasty": "东晋", 
            "emperor": "司马德文（晋恭帝）",
            "birthDeath": "386-421年",
            "templeName": "无",
            "posthumousTitle": "恭皇帝",
            "experience": "东晋末代皇帝，220年禅位于刘裕，南朝宋建立，后被刘裕弑杀，东晋灭亡"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘裕（宋武帝）",
            "birthDeath": "363-422年",
            "templeName": "高祖",
            "posthumousTitle": "武皇帝",
            "experience": "南朝宋开国皇帝，寒门出身，平定东晋内乱，北伐收复洛阳、长安，篡晋建宋，推行改革，抑制门阀，奠定南朝宋基础"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘义符（宋少帝）",
            "birthDeath": "406-424年",
            "templeName": "无",
            "posthumousTitle": "少帝",
            "experience": "南朝宋第二位皇帝，荒淫无道，不理朝政，被辅政大臣徐羡之等人废杀"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘义隆（宋文帝）",
            "birthDeath": "407-453年",
            "templeName": "太祖",
            "posthumousTitle": "文皇帝",
            "experience": "南朝宋第三位皇帝，励精图治，开创“元嘉之治”，多次北伐均失败，后被儿子刘劭弑杀"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘劭（宋元凶）",
            "birthDeath": "426-453年",
            "templeName": "无",
            "posthumousTitle": "无（史称元凶）",
            "experience": "南朝宋第四位皇帝，弑父篡位，在位仅3个月，被弟弟刘骏击败斩杀"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘骏（宋孝武帝）",
            "birthDeath": "430-464年",
            "templeName": "世祖",
            "posthumousTitle": "孝武皇帝",
            "experience": "南朝宋第五位皇帝，平定刘劭之乱后即位，前期励精图治，后期荒淫无道，朝政混乱"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘子业（宋前废帝）",
            "birthDeath": "449-466年",
            "templeName": "无",
            "posthumousTitle": "前废帝",
            "experience": "南朝宋第六位皇帝，残暴嗜杀，荒淫无道，被宗室刘彧等人诛杀"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘彧（宋明帝）",
            "birthDeath": "439-472年",
            "templeName": "太宗",
            "posthumousTitle": "明皇帝",
            "experience": "南朝宋第七位皇帝，平定刘子业之乱后即位，在位期间猜忌嗜杀，南朝宋国力大幅衰退"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘昱（宋后废帝）",
            "birthDeath": "463-477年",
            "templeName": "无",
            "posthumousTitle": "后废帝",
            "experience": "南朝宋第八位皇帝，残暴荒诞，滥杀大臣，被萧道成等人诛杀"
        },
        { 
            "dynasty": "南朝宋", 
            "emperor": "刘准（宋顺帝）",
            "birthDeath": "467-479年",
            "templeName": "无",
            "posthumousTitle": "顺皇帝",
            "experience": "南朝宋末代皇帝，萧道成掌控下的傀儡皇帝，479年禅位于萧道成，南朝宋灭亡，后被萧道成弑杀"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧道成（齐高帝）",
            "birthDeath": "427-482年",
            "templeName": "太祖",
            "posthumousTitle": "高皇帝",
            "experience": "南朝齐开国皇帝，篡宋建齐，节俭治国，整顿吏治，奠定南朝齐基础"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧赜（齐武帝）",
            "birthDeath": "440-493年",
            "templeName": "世祖",
            "posthumousTitle": "武皇帝",
            "experience": "南朝齐第二位皇帝，励精图治，开创“永明之治”，南朝齐国力达到顶峰"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧昭业（齐郁林王）",
            "birthDeath": "473-494年",
            "templeName": "无",
            "posthumousTitle": "郁林王",
            "experience": "南朝齐第三位皇帝，荒淫无道，不理朝政，被萧鸾废杀"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧昭文（齐海陵王）",
            "birthDeath": "480-494年",
            "templeName": "无",
            "posthumousTitle": "海陵王",
            "experience": "南朝齐第四位皇帝，萧鸾拥立的傀儡皇帝，在位仅3个月，被萧鸾废黜后毒杀"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧鸾（齐明帝）",
            "birthDeath": "452-498年",
            "templeName": "高宗",
            "posthumousTitle": "明皇帝",
            "experience": "南朝齐第五位皇帝，弑侄篡位，猜忌嗜杀，南朝齐国力迅速衰退"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧宝卷（齐东昏侯）",
            "birthDeath": "483-501年",
            "templeName": "无",
            "posthumousTitle": "东昏侯",
            "experience": "南朝齐第六位皇帝，残暴荒诞，滥杀大臣，被萧衍推翻，后被杀"
        },
        { 
            "dynasty": "南朝齐", 
            "emperor": "萧宝融（齐和帝）",
            "birthDeath": "488-502年",
            "templeName": "无",
            "posthumousTitle": "和皇帝",
            "experience": "南朝齐末代皇帝，萧衍掌控下的傀儡皇帝，502年禅位于萧衍，南朝齐灭亡，后被萧衍弑杀"
        },
        { 
            "dynasty": "南朝梁", 
            "emperor": "萧衍（梁武帝）",
            "birthDeath": "464-549年",
            "templeName": "高祖",
            "posthumousTitle": "武皇帝",
            "experience": "南朝梁开国皇帝，篡齐建梁，在位48年，前期勤政爱民，后期沉迷佛教，多次舍身同泰寺，引发侯景之乱，被俘后饿死"
        },
        { 
            "dynasty": "南朝梁", 
            "emperor": "萧纲（梁简文帝）",
            "birthDeath": "503-551年",
            "templeName": "太宗",
            "posthumousTitle": "简文皇帝",
            "experience": "南朝梁第二位皇帝，侯景傀儡，在位期间受尽屈辱，后被侯景弑杀"
        },
        { 
            "dynasty": "南朝梁", 
            "emperor": "萧绎（梁元帝）",
            "birthDeath": "508-555年",
            "templeName": "世祖",
            "posthumousTitle": "元皇帝",
            "experience": "南朝梁第三位皇帝，平定侯景之乱，后与西魏交恶，西魏攻破江陵，萧绎被杀"
        },
        { 
            "dynasty": "南朝梁", 
            "emperor": "萧方智（梁敬帝）",
            "birthDeath": "543-557年",
            "templeName": "无",
            "posthumousTitle": "敬皇帝",
            "experience": "南朝梁末代皇帝，陈霸先掌控下的傀儡皇帝，557年禅位于陈霸先，南朝梁灭亡，后被陈霸先弑杀"
        },
        { 
            "dynasty": "南朝陈", 
            "emperor": "陈霸先（陈武帝）",
            "birthDeath": "503-559年",
            "templeName": "高祖",
            "posthumousTitle": "武皇帝",
            "experience": "南朝陈开国皇帝，平定侯景之乱后掌控南朝梁大权，篡梁建陈，稳定江南局势，奠定南朝陈基础"
        },
        { 
            "dynasty": "南朝陈", 
            "emperor": "陈蒨（陈文帝）",
            "birthDeath": "522-566年",
            "templeName": "世祖",
            "posthumousTitle": "文皇帝",
            "experience": "南朝陈第二位皇帝，励精图治，开创“天嘉之治”，南朝陈国力达到鼎盛"
        },
        { 
            "dynasty": "南朝陈", 
            "emperor": "陈伯宗（陈废帝）",
            "birthDeath": "554-570年",
            "templeName": "无",
            "posthumousTitle": "废帝",
            "experience": "南朝陈第三位皇帝，懦弱无能，被叔父陈顼废黜，后病逝"
        },
        { 
            "dynasty": "南朝陈", 
            "emperor": "陈顼（陈宣帝）",
            "birthDeath": "530-582年",
            "templeName": "高宗",
            "posthumousTitle": "孝宣皇帝",
            "experience": "南朝陈第四位皇帝，夺权即位，北伐失败，南朝陈国力由盛转衰"
        },
        { 
            "dynasty": "南朝陈", 
            "emperor": "陈叔宝（陈后主）",
            "birthDeath": "553-604年",
            "templeName": "无",
            "posthumousTitle": "炀皇帝（隋赠）",
            "experience": "南朝陈末代皇帝，荒淫无道，沉迷酒色与诗文，589年隋朝灭陈，陈叔宝被俘，南朝陈灭亡，后善终"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋珪（道武帝）",
            "birthDeath": "371-409年",
            "templeName": "太祖",
            "posthumousTitle": "道武皇帝",
            "experience": "北魏开国皇帝，重建代国，后改国号为魏，统一北方草原，奠定北魏根基，晚年猜忌嗜杀，被儿子拓跋绍弑杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋嗣（明元帝）",
            "birthDeath": "392-423年",
            "templeName": "太宗",
            "posthumousTitle": "明元皇帝",
            "experience": "北魏第二位皇帝，平定拓跋绍之乱后即位，勤政爱民，延续拓跋珪政策，国力稳步提升，为拓跋焘统一北方奠定基础"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋焘（太武帝）",
            "birthDeath": "408-452年",
            "templeName": "世祖",
            "posthumousTitle": "太武皇帝",
            "experience": "北魏第三位皇帝，雄才大略，统一北方，击败柔然、大夏等政权，晚年嗜杀，被宦官宗爱弑杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋余（南安王）",
            "birthDeath": "？-452年",
            "templeName": "无",
            "posthumousTitle": "南安王",
            "experience": "北魏第四位皇帝，被宗爱拥立，在位仅数月，后被宗爱弑杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋濬（文成帝）",
            "birthDeath": "440-465年",
            "templeName": "高宗",
            "posthumousTitle": "文成皇帝",
            "experience": "北魏第五位皇帝，平定宗爱之乱后即位，休养生息，北魏国力复苏，推行汉化政策的开端"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "拓跋弘（献文帝）",
            "birthDeath": "454-476年",
            "templeName": "显祖",
            "posthumousTitle": "献文皇帝",
            "experience": "北魏第六位皇帝，禅位于儿子元宏，后被冯太后毒死，在位期间推行改革，促进北魏发展"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元宏（孝文帝）",
            "birthDeath": "467-499年",
            "templeName": "高祖",
            "posthumousTitle": "孝文皇帝",
            "experience": "北魏第七位皇帝，推行全面汉化改革，迁都洛阳，改汉姓、穿汉服、说汉语，促进民族融合，北魏达到鼎盛"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元恪（宣武帝）",
            "birthDeath": "483-515年",
            "templeName": "世宗",
            "posthumousTitle": "宣武皇帝",
            "experience": "北魏第八位皇帝，后期朝政混乱，外戚专权，北魏由盛转衰，丢失部分南方领土"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元诩（孝明帝）",
            "birthDeath": "510-528年",
            "templeName": "肃宗",
            "posthumousTitle": "孝明皇帝",
            "experience": "北魏第九位皇帝，与胡太后争权，被胡太后毒杀，引发“河阴之变”，北魏统治崩溃"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元子攸（孝庄帝）",
            "birthDeath": "507-530年",
            "templeName": "敬宗",
            "posthumousTitle": "孝庄皇帝",
            "experience": "北魏第十位皇帝，杀尔朱荣，后被尔朱兆弑杀，北魏陷入分裂边缘"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元晔（长广王）",
            "birthDeath": "509-532年",
            "templeName": "无",
            "posthumousTitle": "长广王",
            "experience": "北魏第十一位皇帝，尔朱氏拥立的傀儡皇帝，被废后被杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元恭（节闵帝）",
            "birthDeath": "498-532年",
            "templeName": "无",
            "posthumousTitle": "节闵帝",
            "experience": "北魏第十二位皇帝，尔朱氏拥立的傀儡皇帝，被高欢废杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元朗（安定王）",
            "birthDeath": "513-532年",
            "templeName": "无",
            "posthumousTitle": "安定王",
            "experience": "北魏第十三位皇帝，高欢拥立的傀儡皇帝，被废后被杀"
        },
        { 
            "dynasty": "北魏", 
            "emperor": "元修（孝武帝）",
            "birthDeath": "510-534年",
            "templeName": "无",
            "posthumousTitle": "孝武皇帝",
            "experience": "北魏末代皇帝，与高欢争权失败，逃奔宇文泰，北魏分裂为东魏和西魏，后被宇文泰弑杀"
        },
        { 
            "dynasty": "东魏", 
            "emperor": "元善见（孝静帝）",
            "birthDeath": "524-551年",
            "templeName": "无",
            "posthumousTitle": "孝静皇帝",
            "experience": "东魏唯一皇帝，高欢父子傀儡，550年禅位于高洋，东魏灭亡，后被高洋弑杀"
        },
        { 
            "dynasty": "西魏", 
            "emperor": "元宝炬（文帝）",
            "birthDeath": "507-551年",
            "templeName": "无",
            "posthumousTitle": "文皇帝",
            "experience": "西魏开国皇帝，宇文泰傀儡，隐忍求存，在位期间维持西魏偏安局面"
        },
        { 
            "dynasty": "西魏", 
            "emperor": "元钦（废帝）",
            "birthDeath": "525-554年",
            "templeName": "无",
            "posthumousTitle": "废帝",
            "experience": "西魏第二位皇帝，试图诛杀宇文泰，失败后被废杀"
        },
        { 
            "dynasty": "西魏", 
            "emperor": "元廓（恭帝）",
            "birthDeath": "537-557年",
            "templeName": "无",
            "posthumousTitle": "恭皇帝",
            "experience": "西魏末代皇帝，宇文泰傀儡，557年禅位于宇文觉，西魏灭亡，后被宇文觉弑杀"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高洋（文宣帝）",
            "birthDeath": "526-559年",
            "templeName": "无",
            "posthumousTitle": "文宣皇帝",
            "experience": "北齐开国皇帝，篡东魏建齐，前期英武，统一北方东部，后期残暴嗜杀，荒淫无道"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高殷（废帝）",
            "birthDeath": "545-561年",
            "templeName": "无",
            "posthumousTitle": "废帝",
            "experience": "北齐第二位皇帝，宽厚仁孝，被叔叔高演废杀"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高演（孝昭帝）",
            "birthDeath": "535-561年",
            "templeName": "无",
            "posthumousTitle": "孝昭皇帝",
            "experience": "北齐第三位皇帝，弑侄篡位，勤政爱民，英年早逝"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高湛（武成帝）",
            "birthDeath": "537-569年",
            "templeName": "无",
            "posthumousTitle": "武成皇帝",
            "experience": "北齐第四位皇帝，荒淫残暴，宠信奸佞，北齐国力迅速衰退"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高纬（后主）",
            "birthDeath": "556-577年",
            "templeName": "无",
            "posthumousTitle": "后主",
            "experience": "北齐第五位皇帝，昏庸无道，滥杀功臣，577年北周灭齐，高纬被俘后被杀"
        },
        { 
            "dynasty": "北齐", 
            "emperor": "高恒（幼主）",
            "birthDeath": "570-577年",
            "templeName": "无",
            "posthumousTitle": "幼主",
            "experience": "北齐末代皇帝，在位仅25天，被俘后被杀，北齐灭亡"
        },
        { 
            "dynasty": "北周", 
            "emperor": "宇文觉（孝闵帝）",
            "birthDeath": "542-557年",
            "templeName": "无",
            "posthumousTitle": "孝闵皇帝",
            "experience": "北周开国皇帝，宇文泰之子，被宇文护拥立，后试图诛杀宇文护，失败被废杀"
        },
        { 
            "dynasty": "北周", 
            "emperor": "宇文毓（明帝）",
            "birthDeath": "534-560年",
            "templeName": "世宗",
            "posthumousTitle": "明皇帝",
            "experience": "北周第二位皇帝，有才干，被宇文护毒杀"
        },
        { 
            "dynasty": "北周", 
            "emperor": "宇文邕（武帝）",
            "birthDeath": "543-578年",
            "templeName": "高祖",
            "posthumousTitle": "武皇帝",
            "experience": "北周第三位皇帝，诛杀宇文护亲政，励精图治，灭北齐统一北方，北周达到鼎盛，英年早逝"
        },
        { 
            "dynasty": "北周", 
            "emperor": "宇文赟（宣帝）",
            "birthDeath": "559-580年",
            "templeName": "无",
            "posthumousTitle": "宣皇帝",
            "experience": "北周第四位皇帝，荒淫无道，传位于儿子宇文阐后，沉迷酒色，早逝"
        },
        { 
            "dynasty": "北周", 
            "emperor": "宇文阐（静帝）",
            "birthDeath": "573-581年",
            "templeName": "无",
            "posthumousTitle": "静皇帝",
            "experience": "北周末代皇帝，杨坚傀儡，581年禅位于杨坚，北周灭亡，后被杨坚弑杀"
        },
        { 
            "dynasty": "隋朝", 
            "emperor": "杨坚（隋文帝）",
            "birthDeath": "541-604年",
            "templeName": "高祖",
            "posthumousTitle": "文皇帝",
            "experience": "隋朝开国皇帝，篡周建隋，589年灭陈统一全国，推行“开皇之治”，创立三省六部制、科举制，奠定隋唐盛世基础"
        },
        { 
            "dynasty": "隋朝", 
            "emperor": "杨广（隋炀帝）",
            "birthDeath": "569-618年",
            "templeName": "无",
            "posthumousTitle": "炀皇帝",
            "experience": "隋朝第二位皇帝，在位期间开凿大运河，修建东都洛阳，三征高句丽，横征暴敛，引发隋末农民起义，后被宇文化及弑杀，隋朝灭亡"
        },
        { 
            "dynasty": "隋朝", 
            "emperor": "杨侑（隋恭帝）",
            "birthDeath": "605-619年",
            "templeName": "无",
            "posthumousTitle": "恭皇帝",
            "experience": "隋朝末代皇帝，李渊拥立的傀儡皇帝，618年禅位于李渊，唐朝建立，后被李渊弑杀"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李渊（唐高祖）",
            "birthDeath": "566-635年",
            "templeName": "高祖",
            "posthumousTitle": "神尧大圣大光孝皇帝",
            "experience": "唐朝开国皇帝，晋阳起兵反隋，618年建唐，统一全国，后在“玄武门之变”后禅位于李世民，善终"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李世民（唐太宗）",
            "birthDeath": "598-649年",
            "templeName": "太宗",
            "posthumousTitle": "文武大圣大广孝皇帝",
            "experience": "唐朝第二位皇帝，通过“玄武门之变”即位，励精图治，开创“贞观之治”，虚心纳谏，重用贤才，开疆拓土，被尊为“天可汗”"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李治（唐高宗）",
            "birthDeath": "628-683年",
            "templeName": "高宗",
            "posthumousTitle": "天皇大圣大弘孝皇帝",
            "experience": "唐朝第三位皇帝，在位期间延续贞观之治，开创“永徽之治”，灭高句丽、西突厥，扩大唐朝疆域，后期体弱，武则天逐渐掌控朝政"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "武则天（武周圣神皇帝）",
            "birthDeath": "624-705年",
            "templeName": "无",
            "posthumousTitle": "则天大圣皇帝",
            "experience": "中国历史上唯一女皇帝，废唐建周，在位期间重视人才，推行科举制，整顿吏治，国力稳步提升，晚年病重，被张柬之等人发动“神龙政变”推翻，复唐国号"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李显（唐中宗）",
            "birthDeath": "656-710年",
            "templeName": "中宗",
            "posthumousTitle": "大和大圣大昭孝皇帝",
            "experience": "唐朝第四位皇帝，两度在位，懦弱无能，受制于韦皇后与安乐公主，后被韦皇后与安乐公主毒杀"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李旦（唐睿宗）",
            "birthDeath": "662-716年",
            "templeName": "睿宗",
            "posthumousTitle": "玄真大圣大兴孝皇帝",
            "experience": "唐朝第五位皇帝，两度在位，前期受制于武则天，后期受制于太平公主与李隆基，后禅位于李隆基，善终"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李隆基（唐玄宗）",
            "birthDeath": "685-762年",
            "templeName": "玄宗",
            "posthumousTitle": "至道大圣大明孝皇帝",
            "experience": "唐朝第六位皇帝，发动“唐隆政变”诛杀韦后，即位后开创“开元盛世”，唐朝达到鼎盛，后期沉迷酒色，宠信杨贵妃与杨国忠，引发“安史之乱”，唐朝由盛转衰"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李亨（唐肃宗）",
            "birthDeath": "711-762年",
            "templeName": "肃宗",
            "posthumousTitle": "文明武德大圣大宣孝皇帝",
            "experience": "唐朝第七位皇帝，安史之乱中即位，领导平叛，后期受制于宦官李辅国，忧郁而死"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李豫（唐代宗）",
            "birthDeath": "726-779年",
            "templeName": "代宗",
            "posthumousTitle": "睿文孝武皇帝",
            "experience": "唐朝第八位皇帝，平定安史之乱余孽，后纵容藩镇割据，宦官势力日益膨胀，唐朝统治进一步衰退"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李适（唐德宗）",
            "birthDeath": "742-805年",
            "templeName": "德宗",
            "posthumousTitle": "神武孝文皇帝",
            "experience": "唐朝第九位皇帝，前期锐意改革，试图削弱藩镇与宦官势力，后期猜忌功臣，重用宦官，藩镇割据愈演愈烈"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李诵（唐顺宗）",
            "birthDeath": "761-806年",
            "templeName": "顺宗",
            "posthumousTitle": "至德大圣大安孝皇帝",
            "experience": "唐朝第十位皇帝，在位仅8个月，推行“永贞革新”失败，被迫禅位于李纯，后病逝"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李纯（唐宪宗）",
            "birthDeath": "778-820年",
            "templeName": "宪宗",
            "posthumousTitle": "昭文章武大圣至神孝皇帝",
            "experience": "唐朝第十一位皇帝，开创“元和中兴”，暂时平定藩镇割据，后期宠信宦官，被宦官弑杀"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李恒（唐穆宗）",
            "birthDeath": "795-824年",
            "templeName": "穆宗",
            "posthumousTitle": "睿圣文惠孝皇帝",
            "experience": "唐朝第十二位皇帝，耽于享乐，不理朝政，藩镇割据复燃，唐朝国力继续衰退"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李湛（唐敬宗）",
            "birthDeath": "809-826年",
            "templeName": "敬宗",
            "posthumousTitle": "睿武昭愍孝皇帝",
            "experience": "唐朝第十三位皇帝，年少即位，沉迷游乐，被宦官弑杀，年仅18岁"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李昂（唐文宗）",
            "birthDeath": "809-840年",
            "templeName": "文宗",
            "posthumousTitle": "元圣昭献孝皇帝",
            "experience": "唐朝第十四位皇帝，试图通过“甘露之变”诛杀宦官，失败后被软禁，忧郁而死"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李炎（唐武宗）",
            "birthDeath": "814-846年",
            "templeName": "武宗",
            "posthumousTitle": "至道昭肃孝皇帝",
            "experience": "唐朝第十五位皇帝，推行“会昌中兴”，打压宦官与佛教，整顿吏治，唐朝国力短暂复苏"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李忱（唐宣宗）",
            "birthDeath": "810-859年",
            "templeName": "宣宗",
            "posthumousTitle": "圣武献文孝皇帝",
            "experience": "唐朝第十六位皇帝，人称“小太宗”，开创“大中之治”，唐朝回光返照，后期沉迷丹药，中毒而死"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李漼（唐懿宗）",
            "birthDeath": "833-873年",
            "templeName": "懿宗",
            "posthumousTitle": "昭圣恭惠孝皇帝",
            "experience": "唐朝第十七位皇帝，荒淫无道，不理朝政，唐朝由盛转衰的关键推手，在位期间爆发裘甫起义"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李儇（唐僖宗）",
            "birthDeath": "862-888年",
            "templeName": "僖宗",
            "posthumousTitle": "惠圣恭定孝皇帝",
            "experience": "唐朝第十八位皇帝，在位期间爆发黄巢起义，被迫两次出逃长安，唐朝统治摇摇欲坠"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李晔（唐昭宗）",
            "birthDeath": "867-904年",
            "templeName": "昭宗",
            "posthumousTitle": "圣穆景文孝皇帝",
            "experience": "唐朝第十九位皇帝，力图复兴唐朝，却受制于藩镇，最终被朱温弑杀，唐朝名存实亡"
        },
        { 
            "dynasty": "唐朝", 
            "emperor": "李柷（唐哀帝）",
            "birthDeath": "892-908年",
            "templeName": "无",
            "posthumousTitle": "昭宣光烈孝皇帝",
            "experience": "唐朝末代皇帝，朱温傀儡，907年禅位于朱温，唐朝灭亡，后被朱温毒杀"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵匡胤（宋太祖）",
            "birthDeath": "927-976年",
            "templeName": "太祖",
            "posthumousTitle": "启运立极英武睿文神德圣功至明大孝皇帝",
            "experience": "北宋开国皇帝，通过“陈桥兵变”篡周建宋，统一南方大部分地区，推行“重文轻武”政策，加强中央集权，“烛影斧声”中离奇去世"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵光义（宋太宗）",
            "birthDeath": "939-997年",
            "templeName": "太宗",
            "posthumousTitle": "神功圣德文武皇帝",
            "experience": "北宋第二位皇帝，赵匡胤之弟，即位后统一全国，两次北伐辽国均失败，确立“重文轻武”国策，加强中央集权"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵恒（宋真宗）",
            "birthDeath": "968-1022年",
            "templeName": "真宗",
            "posthumousTitle": "膺符稽古神功让德文明武定章圣元孝皇帝",
            "experience": "北宋第三位皇帝，与辽国签订“澶渊之盟”，维持宋辽百年和平，后期沉迷封禅，朝政日益腐败"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵祯（宋仁宗）",
            "birthDeath": "1010-1063年",
            "templeName": "仁宗",
            "posthumousTitle": "体天法道极功全德神文圣武睿哲明孝皇帝",
            "experience": "北宋第四位皇帝，在位42年，以仁政闻名，开创“庆历新政”，虽未成功，但推动北宋发展，北宋国力达到鼎盛"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵曙（宋英宗）",
            "birthDeath": "1032-1067年",
            "templeName": "英宗",
            "posthumousTitle": "体乾应历隆功盛德宪文肃武睿圣宣孝皇帝",
            "experience": "北宋第五位皇帝，在位仅4年，体弱多病，由曹太后临朝，在位期间命司马光编撰《资治通鉴》"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵顼（宋神宗）",
            "birthDeath": "1048-1085年",
            "templeName": "神宗",
            "posthumousTitle": "绍天法古运德建功英文烈武钦仁圣孝皇帝",
            "experience": "北宋第六位皇帝，支持王安石变法，试图改变北宋积贫积弱局面，变法失败，两次伐夏均失利，忧郁而死"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵煦（宋哲宗）",
            "birthDeath": "1077-1100年",
            "templeName": "哲宗",
            "posthumousTitle": "宪元继道显德定功钦文睿武齐圣昭孝皇帝",
            "experience": "北宋第七位皇帝，幼年即位，由高太后临朝，废除王安石变法，亲政后恢复变法，击败西夏，扩大北宋疆域，英年早逝"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵佶（宋徽宗）",
            "birthDeath": "1082-1135年",
            "templeName": "徽宗",
            "posthumousTitle": "体神合道骏烈逊功圣文仁德宪慈显孝皇帝",
            "experience": "北宋第八位皇帝，擅长书画，创立“瘦金体”，荒淫无道，重用奸佞，爆发方腊起义，1127年“靖康之变”中被俘，死于金国"
        },
        { 
            "dynasty": "北宋", 
            "emperor": "赵桓（宋钦宗）",
            "birthDeath": "1100-1156年",
            "templeName": "钦宗",
            "posthumousTitle": "恭文顺德仁孝皇帝",
            "experience": "北宋末代皇帝，1127年“靖康之变”中与宋徽宗一同被俘，死于金国，北宋灭亡"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵构（宋高宗）",
            "birthDeath": "1107-1187年",
            "templeName": "高宗",
            "posthumousTitle": "受命中兴全功至德圣神武文昭仁宪孝皇帝",
            "experience": "南宋开国皇帝，宋徽宗之子，“靖康之变”后在临安建立南宋，重用秦桧，杀害岳飞，与金国签订“绍兴和议”，偏安江南"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵昚（宋孝宗）",
            "birthDeath": "1127-1194年",
            "templeName": "孝宗",
            "posthumousTitle": "绍统同道冠德昭功哲文神武明圣成孝皇帝",
            "experience": "南宋第二位皇帝，赵构养子，即位后为岳飞平反，发动“隆兴北伐”，失败后与金国签订“隆兴和议”，励精图治，开创“乾淳之治”"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵惇（宋光宗）",
            "birthDeath": "1147-1200年",
            "templeName": "光宗",
            "posthumousTitle": "循道宪仁明功茂德温文顺武圣哲慈孝皇帝",
            "experience": "南宋第三位皇帝，体弱多病，惧内，与父亲赵昚不和，朝政混乱，被大臣废黜"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵扩（宋宁宗）",
            "birthDeath": "1168-1224年",
            "templeName": "宁宗",
            "posthumousTitle": "法天备道纯德茂功仁文哲武圣睿恭孝皇帝",
            "experience": "南宋第四位皇帝，在位期间发动“开禧北伐”，失败后与金国签订“嘉定和议”，朝政被史弥远掌控"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵昀（宋理宗）",
            "birthDeath": "1205-1264年",
            "templeName": "理宗",
            "posthumousTitle": "建道备德大功复兴烈文仁武圣明安孝皇帝",
            "experience": "南宋第五位皇帝，史弥远拥立，前期受制于史弥远，亲政后整顿吏治，后期沉迷酒色，重用贾似道，南宋国力迅速衰退"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵禥（宋度宗）",
            "birthDeath": "1240-1274年",
            "templeName": "度宗",
            "posthumousTitle": "端文明武景孝皇帝",
            "experience": "南宋第六位皇帝，懦弱无能，重用贾似道，不理朝政，蒙古大军南下，南宋危在旦夕"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵显（宋恭帝）",
            "birthDeath": "1271-1323年",
            "templeName": "无",
            "posthumousTitle": "恭皇帝",
            "experience": "南宋第七位皇帝，幼年即位，1276年元军攻破临安，赵显被俘，后出家为僧，被元英宗赐死"
        },
        { 
            "dynasty": "南宋", 
            "emperor": "赵昰（宋端宗）",
            "birthDeath": "1269-1278年",
            "templeName": "端宗",
            "posthumousTitle": "裕文昭武愍孝皇帝",
            "experience": "南宋第八位皇帝，赵显之弟，在福州即位，后被元军追击，病逝于碙洲"
        },
        { 
    "dynasty": "成汉", 
    "emperor": "李雄（成汉武帝）",
    "birthDeath": "274-334年",
    "templeName": "太宗",
    "posthumousTitle": "武皇帝",
    "experience": "成汉开国皇帝，建大成国（后改汉），治蜀宽和，轻徭薄赋，国力渐强，奠定成汉基业"
},
{ 
    "dynasty": "成汉", 
    "emperor": "李班（成汉哀帝）",
    "birthDeath": "288-334年",
    "templeName": "哀帝",
    "posthumousTitle": "哀皇帝",
    "experience": "仁厚无威权，即位后不久被李越、李期联手弑杀，在位仅数月"
},
{ 
    "dynasty": "成汉", 
    "emperor": "李期（成汉幽公）",
    "birthDeath": "314-338年",
    "templeName": "无",
    "posthumousTitle": "幽公",
    "experience": "弑叔篡位，残暴多疑，滥杀宗室大臣，被李寿推翻后自杀身亡"
},
{ 
    "dynasty": "成汉", 
    "emperor": "李寿（成汉中宗）",
    "birthDeath": "300-343年",
    "templeName": "中宗",
    "posthumousTitle": "昭文皇帝",
    "experience": "夺位后改国号为汉，前期勤政兴利，后期奢侈残暴，加重赋税导致国力衰退"
},
{ 
    "dynasty": "成汉", 
    "emperor": "李势（成汉末主）",
    "birthDeath": "？-361年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "成汉末代皇帝，荒淫无道，不理朝政，347年被东晋桓温所灭，被俘后善终"
},
{ 
    "dynasty": "汉赵", 
    "emperor": "刘渊（汉赵光文帝）",
    "birthDeath": "？-310年",
    "templeName": "高祖",
    "posthumousTitle": "光文皇帝",
    "experience": "汉赵开国皇帝，趁西晋内乱起兵，建立汉国，开启五胡十六国乱世，推动匈奴汉化"
},
{ 
    "dynasty": "汉赵", 
    "emperor": "刘和（汉赵废帝）",
    "birthDeath": "？-310年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "即位后猜忌兄弟，欲诛杀刘聪等，反被刘聪发动政变弑杀，在位仅7天"
},
{ 
    "dynasty": "汉赵", 
    "emperor": "刘聪（汉赵昭武帝）",
    "birthDeath": "？-318年",
    "templeName": "烈宗",
    "posthumousTitle": "昭武皇帝",
    "experience": "灭西晋，俘晋怀、愍二帝，统一北方部分地区，前期英明后期荒淫暴虐，朝政混乱"
},
{ 
    "dynasty": "汉赵", 
    "emperor": "刘粲（汉赵隐帝）",
    "birthDeath": "？-318年",
    "templeName": "隐帝",
    "posthumousTitle": "无",
    "experience": "荒淫无道，重用奸佞，在位仅2个月被靳准弑杀，汉赵陷入内乱"
},
{ 
    "dynasty": "汉赵", 
    "emperor": "刘曜（汉赵末帝）",
    "birthDeath": "？-329年",
    "templeName": "高祖",
    "posthumousTitle": "昭文皇帝",
    "experience": "平定靳准之乱，改国号为赵（前赵），与后赵石勒对峙，战败被俘后被杀，汉赵灭亡"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石勒（后赵明帝）",
    "birthDeath": "274-333年",
    "templeName": "高祖",
    "posthumousTitle": "明皇帝",
    "experience": "后赵开国皇帝，统一北方大部，重用汉人推行汉化，建立完善制度，国力强盛"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石弘（后赵海阳王）",
    "birthDeath": "314-335年",
    "templeName": "无",
    "posthumousTitle": "海阳王",
    "experience": "傀儡皇帝，受制于石虎，在位2年被废杀，后赵政权落入石虎手中"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石虎（后赵武帝）",
    "birthDeath": "295-349年",
    "templeName": "太祖",
    "posthumousTitle": "武皇帝",
    "experience": "残暴嗜杀，荒淫无度，大兴土木加重民赋，虽扩张领土但国力由盛转衰"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石世（后赵少帝）",
    "birthDeath": "339-349年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "幼年即位，在位仅33天被石遵废杀，后赵陷入皇族内乱"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石遵（后赵废帝）",
    "birthDeath": "？-349年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "弑侄篡位，在位仅183天，被石鉴与冉闵联手诛杀"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石鉴（后赵末帝）",
    "birthDeath": "？-350年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "冉闵掌控下的傀儡皇帝，后被冉闵弑杀，后赵灭亡"
},
{ 
    "dynasty": "后赵", 
    "emperor": "石祗（后赵兴武帝）",
    "birthDeath": "？-351年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "在后赵残余势力拥立，与冉魏对抗，兵败被杀，后赵彻底覆灭"
},
{ 
    "dynasty": "冉魏", 
    "emperor": "冉闵（冉魏武悼天王）",
    "birthDeath": "？-352年",
    "templeName": "无",
    "posthumousTitle": "武悼天王",
    "experience": "建冉魏，颁布“杀胡令”引发民族冲突，虽短暂统一北方局部，后与前燕交战兵败被杀"
},
{ 
    "dynasty": "前凉", 
    "emperor": "张祚（前凉威王）",
    "birthDeath": "？-355年",
    "templeName": "无",
    "posthumousTitle": "威王",
    "experience": "前凉唯一称帝者，荒淫残暴，篡位自立，在位2年被宗室张瓘发动兵变诛杀"
},
{ 
    "dynasty": "前燕", 
    "emperor": "慕容儁（前燕景昭帝）",
    "birthDeath": "319-360年",
    "templeName": "烈祖",
    "posthumousTitle": "景昭皇帝",
    "experience": "前燕开国皇帝，352年称帝，统一华北东部，与前秦对峙，奠定前燕鼎盛局面"
},
{ 
    "dynasty": "前燕", 
    "emperor": "慕容暐（前燕幽帝）",
    "birthDeath": "350-384年",
    "templeName": "无",
    "posthumousTitle": "幽帝",
    "experience": "前燕末代皇帝，朝政被慕容评掌控，腐败混乱，370年被前秦苻坚所灭，被俘后善终"
},
{ 
    "dynasty": "前秦", 
    "emperor": "苻健（前秦明帝）",
    "birthDeath": "317-355年",
    "templeName": "太祖",
    "posthumousTitle": "明皇帝",
    "experience": "前秦开国皇帝，351年建秦，稳定关陇地区，与东晋对峙，推行汉化促进发展"
},
{ 
    "dynasty": "前秦", 
    "emperor": "苻生（前秦厉王）",
    "birthDeath": "335-357年",
    "templeName": "无",
    "posthumousTitle": "厉王",
    "experience": "残暴至极，滥杀大臣宗室，荒淫无道，被苻坚发动政变弑杀"
},
{ 
    "dynasty": "前秦", 
    "emperor": "苻丕（前秦哀平帝）",
    "birthDeath": "？-386年",
    "templeName": "无",
    "posthumousTitle": "哀平皇帝",
    "experience": "苻坚死后即位，与后秦、西燕混战，兵败被杀，前秦政权分裂"
},
{ 
    "dynasty": "前秦", 
    "emperor": "苻登（前秦高皇帝）",
    "birthDeath": "343-394年",
    "templeName": "太宗",
    "posthumousTitle": "高皇帝",
    "experience": "坚持对抗后秦姚氏，虽作战勇猛但国力衰弱，最终兵败被杀"
},
{ 
    "dynasty": "前秦", 
    "emperor": "苻崇（前秦末主）",
    "birthDeath": "？-394年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "前秦末代皇帝，苻登之子，即位后不久被西秦所杀，前秦灭亡"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容垂（后燕成武帝）",
    "birthDeath": "326-396年",
    "templeName": "世祖",
    "posthumousTitle": "成武皇帝",
    "experience": "后燕开国皇帝，淝水之战后复国，重创前秦，统一北方东部，晚年兵败于北魏"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容宝（后燕惠愍帝）",
    "birthDeath": "355-398年",
    "templeName": "烈宗",
    "posthumousTitle": "惠愍皇帝",
    "experience": "懦弱无能，参合陂之战惨败于北魏，后被兰汗发动兵变弑杀"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容详（后燕废帝）",
    "birthDeath": "？-397年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "自立为帝，嗜杀无度，在位仅2个月被慕容麟诛杀"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容麟（后燕废帝）",
    "birthDeath": "？-398年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "弑兄篡位，与北魏交战兵败，后被慕容德击败身死"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容盛（后燕昭武帝）",
    "birthDeath": "373-401年",
    "templeName": "中宗",
    "posthumousTitle": "昭武皇帝",
    "experience": "平定兰汗之乱即位，猜忌嗜杀，加强集权，后被刺杀身亡"
},
{ 
    "dynasty": "后燕", 
    "emperor": "慕容熙（后燕昭文帝）",
    "birthDeath": "385-407年",
    "templeName": "无",
    "posthumousTitle": "昭文帝",
    "experience": "荒淫无道，为宠妃大兴土木，滥杀无辜，被冯跋发动政变弑杀，后燕灭亡"
},
{ 
    "dynasty": "南燕", 
    "emperor": "慕容德（南燕献武帝）",
    "birthDeath": "336-405年",
    "templeName": "世宗",
    "posthumousTitle": "献武皇帝",
    "experience": "南燕开国皇帝，据山东半岛建国，治国尚算清明，奠定南燕根基"
},
{ 
    "dynasty": "南燕", 
    "emperor": "慕容超（南燕末主）",
    "birthDeath": "384-410年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "南燕末代皇帝，荒于政事，猜忌大臣，410年被东晋刘裕所灭，被俘后处死"
},
{ 
    "dynasty": "西燕", 
    "emperor": "慕容冲（西燕威帝）",
    "birthDeath": "359-386年",
    "templeName": "无",
    "posthumousTitle": "威帝",
    "experience": "建西燕，与慕容垂争夺慕容氏正统，定都长安，后被部下韩延所杀"
},
{ 
    "dynasty": "西燕", 
    "emperor": "慕容瑶（西燕废帝）",
    "birthDeath": "？-386年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "被部下拥立为帝，在位仅10天被慕容忠取代，后被杀"
},
{ 
    "dynasty": "西燕", 
    "emperor": "慕容忠（西燕末主）",
    "birthDeath": "？-386年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "西燕末代皇帝，被慕容永发动政变弑杀，西燕政权落入慕容永手中"
},
{ 
    "dynasty": "后秦", 
    "emperor": "姚苌（后秦武昭帝）",
    "birthDeath": "330-393年",
    "templeName": "太祖",
    "posthumousTitle": "武昭皇帝",
    "experience": "后秦开国皇帝，杀苻坚建后秦，据关中地区，与前秦、西燕长期混战"
},
{ 
    "dynasty": "后秦", 
    "emperor": "姚兴（后秦文桓帝）",
    "birthDeath": "366-416年",
    "templeName": "高祖",
    "posthumousTitle": "文桓皇帝",
    "experience": "治后秦达鼎盛，重用鸠摩罗什译经，推行汉化，后期国力衰退，遭刘裕北伐"
},
{ 
    "dynasty": "后秦", 
    "emperor": "姚泓（后秦末主）",
    "birthDeath": "388-417年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "后秦末代皇帝，懦弱无能，面对刘裕北伐兵败投降，后被处死，后秦灭亡"
},
{ 
    "dynasty": "夏", 
    "emperor": "赫连勃勃（夏武烈帝）",
    "birthDeath": "381-425年",
    "templeName": "世祖",
    "posthumousTitle": "武烈皇帝",
    "experience": "夏开国皇帝，建统万城，残暴嗜杀，善用兵，扩张领土，国力强盛"
},
{ 
    "dynasty": "夏", 
    "emperor": "赫连昌（夏废帝）",
    "birthDeath": "？-434年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "即位后与北魏交战，兵败被俘，夏国领土大幅丧失"
},
{ 
    "dynasty": "夏", 
    "emperor": "赫连定（夏末主）",
    "birthDeath": "？-432年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "夏末代皇帝，赫连昌被俘后即位，试图复国兵败，被吐谷浑所俘后处死，夏灭亡"
},
{ 
    "dynasty": "后梁", 
    "emperor": "朱晃（后梁太祖）",
    "birthDeath": "852-912年",
    "templeName": "太祖",
    "posthumousTitle": "神武元圣孝皇帝",
    "experience": "后梁开国皇帝，原名朱温，篡唐称帝建立后梁，结束唐朝统治，前期割据中原，后期残暴嗜杀，被其子朱友珪弑杀"
},
{ 
    "dynasty": "后梁", 
    "emperor": "朱友珪（后梁废帝）",
    "birthDeath": "？-913年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "弑父篡位登基，在位期间荒淫无道，朝政混乱，仅在位数月便被朱瑱（朱友贞）联合大臣推翻，兵败被杀"
},
{ 
    "dynasty": "后梁", 
    "emperor": "朱瑱（后梁末帝）",
    "birthDeath": "888-923年",
    "templeName": "无",
    "posthumousTitle": "末帝",
    "experience": "后梁末代皇帝，原名朱友贞，推翻朱友珪即位，与后唐李存勖长期对峙，最终兵败自杀，后梁灭亡"
},
{ 
    "dynasty": "后唐", 
    "emperor": "李存勖（后唐庄宗）",
    "birthDeath": "885-926年",
    "templeName": "庄宗",
    "posthumousTitle": "光圣神闵孝皇帝",
    "experience": "后唐开国皇帝，骁勇善战，灭后梁统一北方，前期英明有为，后期沉迷享乐、重用伶人，引发兴教门之变被杀"
},
{ 
    "dynasty": "后唐", 
    "emperor": "李亶（后唐明宗）",
    "birthDeath": "867-933年",
    "templeName": "明宗",
    "posthumousTitle": "圣德和武钦孝皇帝",
    "experience": "原名李嗣源，兵变即位，在位期间整顿朝政、休养生息，吏治清明，史称“天成之治”，晚年朝政逐渐混乱"
},
{ 
    "dynasty": "后唐", 
    "emperor": "李从厚（后唐闵帝）",
    "birthDeath": "914-934年",
    "templeName": "无",
    "posthumousTitle": "闵皇帝",
    "experience": "年少即位，懦弱无能，受制于权臣，在位仅数月便被李从珂发动兵变推翻，逃亡途中被杀"
},
{ 
    "dynasty": "后唐", 
    "emperor": "李从珂（后唐末帝）",
    "birthDeath": "885-936年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "后唐末代皇帝，靠兵变登基，与石敬瑭矛盾激化，石敬瑭借契丹兵力来攻，李从珂自焚而死，后唐灭亡"
},
{ 
    "dynasty": "后晋", 
    "emperor": "石敬瑭（后晋高祖）",
    "birthDeath": "892-942年",
    "templeName": "高祖",
    "posthumousTitle": "圣文章武明德孝皇帝",
    "experience": "后晋开国皇帝，以割让燕云十六州为代价，借契丹兵力灭后唐称帝，尊称契丹君主为“父皇帝”，自称“儿皇帝”，留下千古骂名"
},
{ 
    "dynasty": "后晋", 
    "emperor": "石重贵（后晋出帝）",
    "birthDeath": "914-974年",
    "templeName": "无",
    "posthumousTitle": "出帝（负义侯）",
    "experience": "后晋末代皇帝，即位后拒绝向契丹称臣，与契丹爆发战争，最终兵败被俘，后晋灭亡，被俘后病死异乡"
},
{ 
    "dynasty": "后汉", 
    "emperor": "刘暠（后汉高祖）",
    "birthDeath": "895-948年",
    "templeName": "高祖",
    "posthumousTitle": "睿文圣武昭肃孝皇帝",
    "experience": "原名刘知远，后汉开国皇帝，趁契丹北撤之机在太原称帝，建立后汉，迅速统一北方，在位仅一年便病逝"
},
{ 
    "dynasty": "后汉", 
    "emperor": "刘承祐（后汉隐帝）",
    "birthDeath": "930-950年",
    "templeName": "无",
    "posthumousTitle": "隐皇帝",
    "experience": "后汉末代皇帝，年少即位，猜忌权臣，诛杀郭威家族，引发郭威兵变，最终在逃亡中被部下所杀，后汉灭亡"
},
{ 
    "dynasty": "北汉", 
    "emperor": "刘旻（北汉世祖）",
    "birthDeath": "895-954年",
    "templeName": "世祖",
    "posthumousTitle": "神武皇帝",
    "birthDeath": "895-954年",
    "experience": "原名刘崇，北汉开国皇帝，刘暠之弟，后汉灭亡后在太原建立北汉，依附契丹对抗后周，最终兵败忧愤而死"
},
{ 
    "dynasty": "北汉", 
    "emperor": "刘钧（北汉睿宗）",
    "birthDeath": "926-968年",
    "templeName": "睿宗",
    "posthumousTitle": "孝和皇帝",
    "experience": "刘旻之子，即位后继续依附契丹，自称“儿皇帝”，励精图治维持北汉统治，与后周、北宋长期对峙，病逝于位"
},
{ 
    "dynasty": "北汉", 
    "emperor": "刘继恩（北汉废帝）",
    "birthDeath": "935-968年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "刘钧养子，即位后受制于权臣郭无为，在位仅两个月便被郭无为派人弑杀，政权短暂动荡"
},
{ 
    "dynasty": "北汉", 
    "emperor": "刘继元（北汉末帝）",
    "birthDeath": "？-992年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "北汉末代皇帝，即位后继续依附契丹，抵抗北宋进攻，最终被宋太宗赵光义所灭，被俘后降封彭城郡公，善终"
},
{ 
    "dynasty": "后周", 
    "emperor": "郭威（后周太祖）",
    "birthDeath": "904-954年",
    "templeName": "太祖",
    "posthumousTitle": "圣神恭肃文武孝皇帝",
    "experience": "后周开国皇帝，发动兵变取代后汉，在位期间改革弊政、减轻赋税、整顿军纪，休养生息，奠定后周强盛基础"
},
{ 
    "dynasty": "后周", 
    "emperor": "郭荣（后周世宗）",
    "birthDeath": "921-959年",
    "templeName": "世宗",
    "posthumousTitle": "睿武孝文皇帝",
    "experience": "原名柴荣，郭威养子，在位期间励精图治、南征北战，改革军政、发展生产，为北宋统一全国奠定坚实基础，英年早逝"
},
{ 
    "dynasty": "后周", 
    "emperor": "柴宗训（后周恭帝）",
    "birthDeath": "953-973年",
    "templeName": "无",
    "posthumousTitle": "恭皇帝",
    "experience": "后周末代皇帝，幼年即位，赵匡胤发动陈桥兵变，被黄袍加身取代帝位，后周灭亡，降封郑王，善终"
},
{ 
    "dynasty": "南吴", 
    "emperor": "杨溥（南吴睿帝）",
    "birthDeath": "900-938年",
    "templeName": "睿宗",
    "posthumousTitle": "睿皇帝",
    "experience": "南吴末代君主，先称吴王，后正式称帝，在位期间为权臣所制，最终禅位于李昪，南吴灭亡，不久后病逝"
},
{ 
    "dynasty": "前蜀", 
    "emperor": "王建（前蜀高祖）",
    "birthDeath": "847-918年",
    "templeName": "高祖",
    "posthumousTitle": "神武圣文孝德明惠皇帝",
    "experience": "前蜀开国皇帝，在蜀地割据称帝，在位期间保境安民、发展生产、整顿吏治，使蜀地成为乱世中的安定之地"
},
{ 
    "dynasty": "前蜀", 
    "emperor": "王衍（前蜀后主）",
    "birthDeath": "899-926年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "前蜀末代皇帝，荒淫无道、不理朝政，沉迷酒色与游乐，最终被后唐李存勖所灭，被俘后处死"
},
{ 
    "dynasty": "闽", 
    "emperor": "王鏻（闽惠宗）",
    "birthDeath": "889-935年",
    "templeName": "惠宗",
    "posthumousTitle": "齐肃明孝皇帝",
    "experience": "闽国第二位君主，即位后正式称帝，前期尚能理政，后期荒淫残暴、重用奸佞，最终被其子王昶（王继鹏）弑杀"
},
{ 
    "dynasty": "闽", 
    "emperor": "王昶（闽康宗）",
    "birthDeath": "？-939年",
    "templeName": "康宗",
    "posthumousTitle": "圣神英睿文明广武应道大弘孝皇帝",
    "experience": "原名王继鹏，弑父篡位登基，在位期间昏庸无道、横征暴敛，引发军民不满，最终被部下发动兵变弑杀"
},
{ 
    "dynasty": "闽", 
    "emperor": "王曦（闽景宗）",
    "birthDeath": "？-944年",
    "templeName": "景宗",
    "posthumousTitle": "睿文广武明圣元德隆道大孝皇帝",
    "experience": "在位期间嗜酒嗜杀、残暴不仁，与弟弟王延政常年内战，导致闽国国力衰败，最终被部下联合王延政弑杀"
},
{ 
    "dynasty": "南汉", 
    "emperor": "刘䶮（南汉高祖）",
    "birthDeath": "889-942年",
    "templeName": "高祖",
    "posthumousTitle": "天皇大帝",
    "experience": "南汉开国皇帝，在岭南割据称帝，在位期间建立官制、发展经济，后期奢侈残暴，大肆兴建宫殿，加重百姓负担"
},
{ 
    "dynasty": "南汉", 
    "emperor": "刘玢（南汉殇帝）",
    "birthDeath": "920-943年",
    "templeName": "无",
    "posthumousTitle": "殇皇帝",
    "experience": "南汉第二位君主，荒淫无道、沉迷游乐，不理朝政，在位仅一年便被其弟刘晟发动兵变弑杀"
},
{ 
    "dynasty": "南汉", 
    "emperor": "刘晟（南汉中宗）",
    "birthDeath": "920-958年",
    "templeName": "中宗",
    "posthumousTitle": "文武光圣明孝皇帝",
    "experience": "弑兄篡位登基，在位期间大肆诛杀宗室与大臣，消除异己，后期沉迷酒色，朝政日益腐败，南汉国力渐衰"
},
{ 
    "dynasty": "南汉", 
    "emperor": "刘鋹（南汉后主）",
    "birthDeath": "942-980年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "南汉末代皇帝，荒淫无道、重用宦官，荒废朝政，北宋大军南下时无力抵抗，被俘后降封恩赦侯，善终"
},
{ 
    "dynasty": "后蜀", 
    "emperor": "孟知祥（后蜀高祖）",
    "birthDeath": "874-934年",
    "templeName": "高祖",
    "posthumousTitle": "文武圣德英烈明孝皇帝",
    "experience": "后蜀开国皇帝，趁后唐内乱之机，在蜀地割据称帝，建立后蜀，在位仅数月便病逝，传位给其子孟昶"
},
{ 
    "dynasty": "后蜀", 
    "emperor": "孟昶（后蜀后主）",
    "birthDeath": "919-965年",
    "templeName": "无",
    "posthumousTitle": "恭孝王",
    "experience": "后蜀末代皇帝，在位前期励精图治、休养生息，蜀地富庶安定，后期沉迷享乐、荒废朝政，最终被北宋所灭，被俘后善终"
},
{ 
    "dynasty": "南唐", 
    "emperor": "李昪（南唐烈祖）",
    "birthDeath": "888-943年",
    "templeName": "烈祖",
    "posthumousTitle": "光文肃武孝高皇帝",
    "experience": "南唐开国皇帝，原名徐知诰，篡南吴称帝后恢复李姓，改国号为唐（南唐），在位期间休养生息、发展生产，南唐国力日渐强盛"
},
{ 
    "dynasty": "南唐", 
    "emperor": "李璟（南唐元宗）",
    "birthDeath": "916-961年",
    "templeName": "元宗",
    "posthumousTitle": "明道崇德文宣孝皇帝",
    "experience": "又称南唐中主，在位前期扩张领土，后期被后周击败，被迫割地称臣，去帝号，晚年传位给其子李煜，郁郁而终"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律亿（辽太祖）",
    "birthDeath": "872-926年",
    "templeName": "太祖",
    "posthumousTitle": "大圣大明神烈天皇帝",
    "experience": "原名耶律阿保机，辽朝开国皇帝，统一契丹各部，称帝建辽，创制契丹文字，奠定辽朝百年基业，东征渤海国时病逝"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律德光（辽太宗）",
    "birthDeath": "902-947年",
    "templeName": "太宗",
    "posthumousTitle": "孝武惠文皇帝",
    "experience": "耶律亿次子，在位期间南下灭后晋，改国号为“大辽”，北撤途中病逝于栾城，被制成“帝羓”运回契丹"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律阮（辽世宗）",
    "birthDeath": "917-951年",
    "templeName": "世宗",
    "posthumousTitle": "孝和庄宪皇帝",
    "experience": "耶律亿之孙，即位后稳定辽朝内部统治，尝试汉化改革，后期率军南下攻打后周，在兵变中被杀"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律璟（辽穆宗）",
    "birthDeath": "931-969年",
    "templeName": "穆宗",
    "posthumousTitle": "孝安敬正皇帝",
    "experience": "在位期间残暴嗜杀、沉迷饮酒与睡眠，不理朝政，被称为“睡王”，最终被身边侍从弑杀"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律贤（辽景宗）",
    "birthDeath": "948-982年",
    "templeName": "景宗",
    "posthumousTitle": "孝成康靖皇帝",
    "experience": "即位后整顿朝政、重用汉臣、改革弊政，与北宋对峙，后期体弱多病，由皇后萧绰（萧燕燕）辅政，为辽朝鼎盛奠基"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律隆绪（辽圣宗）",
    "birthDeath": "972-1031年",
    "templeName": "圣宗",
    "posthumousTitle": "文武大孝宣皇帝",
    "experience": "年少即位，由萧绰辅政，开创“澶渊之盟”，与北宋维持百年和平，亲政后继续改革，辽朝达到鼎盛时期"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律宗真（辽兴宗）",
    "birthDeath": "1016-1055年",
    "templeName": "兴宗",
    "posthumousTitle": "神圣孝章皇帝",
    "experience": "在位期间与北宋、西夏多次交战，国力消耗巨大，后期朝政日益腐败，辽朝开始由盛转衰"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律洪基（辽道宗）",
    "birthDeath": "1032-1101年",
    "templeName": "道宗",
    "posthumousTitle": "仁圣大孝文皇帝",
    "experience": "在位期间重用奸佞耶律乙辛，引发“重元之乱”，诛杀太子耶律浚，朝政腐败不堪，辽朝衰落加剧"
},
{ 
    "dynasty": "辽", 
    "emperor": "耶律延禧（辽天祚帝）",
    "birthDeath": "1075-1128年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "辽朝末代皇帝，昏庸无道、不理朝政，沉迷游猎，面对金国进攻节节败退，最终被俘，辽朝灭亡，后惨死异乡"
},
{ 
    "dynasty": "明", 
    "emperor": "朱元璋（明太祖）",
    "birthDeath": "1328-1398年",
    "templeName": "太祖",
    "posthumousTitle": "开天行道肇纪立极大圣至神仁文义武俊德成功高皇帝",
    "experience": "明朝开国皇帝，出身布衣，推翻元朝统治，统一全国，开创“洪武之治”，废除丞相制加强集权，整顿吏治严惩贪腐"
},
{ 
    "dynasty": "明", 
    "emperor": "朱允炆（明惠宗）",
    "birthDeath": "1377-？年",
    "templeName": "无",
    "posthumousTitle": "嗣天章道诚懿渊功观文扬武克仁笃孝让皇帝（南明追尊）",
    "experience": "明朝第二位皇帝，推行“建文新政”，试图削藩引发“靖难之役”，兵败后下落不明，成为历史谜团"
},
{ 
    "dynasty": "明", 
    "emperor": "朱棣（明成祖）",
    "birthDeath": "1360-1424年",
    "templeName": "成祖",
    "posthumousTitle": "启天弘道高明肇运圣武神功纯仁至孝文皇帝",
    "experience": "发动“靖难之役”夺取帝位，迁都北京，派郑和七下西洋，编纂《永乐大典》，开创“永乐盛世”，奠定明朝强盛基础"
},
{ 
    "dynasty": "明", 
    "emperor": "朱高炽（明仁宗）",
    "birthDeath": "1378-1425年",
    "templeName": "仁宗",
    "posthumousTitle": "敬天体道纯诚至德弘文钦武章圣达孝昭皇帝",
    "experience": "在位仅10个月，推行仁政，平反冤案，减轻赋税，与民休息，为“仁宣之治”奠定坚实基础"
},
{ 
    "dynasty": "明", 
    "emperor": "朱瞻基（明宣宗）",
    "birthDeath": "1398-1435年",
    "templeName": "宣宗",
    "posthumousTitle": "宪天崇道英明神圣钦文昭武宽仁纯孝章皇帝",
    "experience": "延续仁政，平定汉王朱高煦叛乱，整顿吏治发展生产，“仁宣之治”达鼎盛，明朝国力空前强盛"
},
{ 
    "dynasty": "明", 
    "emperor": "朱祁镇（明英宗）",
    "birthDeath": "1427-1464年",
    "templeName": "英宗",
    "posthumousTitle": "法天立道仁明诚敬昭文宪武至德广孝睿皇帝",
    "experience": "两度在位，前期宠信王振引发“土木堡之变”被俘，复辟后诛杀于谦，晚年幡然醒悟，废除殉葬制"
},
{ 
    "dynasty": "明", 
    "emperor": "朱祁钰（明代宗）",
    "birthDeath": "1428-1457年",
    "templeName": "代宗",
    "posthumousTitle": "恭仁康定景皇帝",
    "experience": "临危受命登基，重用于谦取得“北京保卫战”胜利，稳定朝局，后被夺门之变推翻，贬为郕王，离奇病逝"
},
{ 
    "dynasty": "明", 
    "emperor": "朱见深（明宪宗）",
    "birthDeath": "1447-1487年",
    "templeName": "宪宗",
    "posthumousTitle": "继天凝道诚明仁敬崇文肃武宏德圣孝纯皇帝",
    "experience": "平反于谦冤案，设立西厂加强特务统治，宠信万贵妃，后期朝政日益腐败，明朝开始走向衰退"
},
{ 
    "dynasty": "明", 
    "emperor": "朱祐樘（明孝宗）",
    "birthDeath": "1470-1505年",
    "templeName": "孝宗",
    "posthumousTitle": "达天明道纯诚中正圣文神武至仁大德敬皇帝",
    "experience": "一生只娶一妻，励精图治整顿朝政，减免赋税发展生产，开创“弘治中兴”，明朝短暂复苏"
},
{ 
    "dynasty": "明", 
    "emperor": "朱厚照（明武宗）",
    "birthDeath": "1491-1521年",
    "templeName": "武宗",
    "posthumousTitle": "承天达道英肃睿哲昭德显功弘文思孝毅皇帝",
    "experience": "沉迷玩乐，宠信刘瑾等宦官，设立豹房，荒于朝政，虽荒唐但未酿成大乱，多次赈灾平叛维持统治"
},
{ 
    "dynasty": "明", 
    "emperor": "朱厚熜（明世宗）",
    "birthDeath": "1507-1567年",
    "templeName": "世宗",
    "posthumousTitle": "钦天履道英毅神圣宣文广武洪仁大孝肃皇帝",
    "experience": "通过“大礼议”巩固皇权，前期推行“嘉靖新政”成效显著，后期沉迷炼丹求仙，引发“壬寅宫变”，朝政渐腐"
},
{ 
    "dynasty": "明", 
    "emperor": "朱载坖（明穆宗）",
    "birthDeath": "1537-1572年",
    "templeName": "穆宗",
    "posthumousTitle": "契天隆道渊懿宽仁显文光武纯德弘孝庄皇帝",
    "experience": "推行“隆庆开关”允许民间海外贸易，与蒙古俺答达成封贡协议，边境和平，明朝经济短暂回升"
},
{ 
    "dynasty": "明", 
    "emperor": "朱翊钧（明神宗）",
    "birthDeath": "1563-1620年",
    "templeName": "神宗",
    "posthumousTitle": "范天合道哲肃敦简光文章武安仁止孝显皇帝",
    "experience": "前期在张居正辅佐下推行“万历新政”，国力复苏，后期怠政30年，党争加剧，明朝由盛转衰"
},
{ 
    "dynasty": "明", 
    "emperor": "朱常洛（明光宗）",
    "birthDeath": "1582-1620年",
    "templeName": "光宗",
    "posthumousTitle": "崇天契道英睿恭纯宪文景武渊仁懿孝贞皇帝",
    "experience": "经历“国本之争”后即位，沉迷酒色纵欲过度，在位仅29天便病逝，引发“红丸案”，明末三大案之一"
},
{ 
    "dynasty": "明", 
    "emperor": "朱由校（明熹宗）",
    "birthDeath": "1605-1627年",
    "templeName": "熹宗",
    "posthumousTitle": "达天阐道敦孝笃友章文襄武靖穆庄勤悊皇帝",
    "experience": "热衷木匠活，被称为“木匠皇帝”，宠信魏忠贤等阉党，朝政黑暗腐败，农民起义与后金威胁加剧"
},
{ 
    "dynasty": "明", 
    "emperor": "朱由检（明思宗）",
    "birthDeath": "1611-1644年",
    "templeName": "思宗",
    "posthumousTitle": "绍天绎道刚明恪俭揆文奋武敦仁懋孝烈皇帝",
    "experience": "崇祯帝，勤政节俭试图挽救明朝，无奈积重难返，诛杀魏忠贤但多疑猜忌，最终李自成攻破北京，自缢于煤山，明朝灭亡"
},
{ 
    "dynasty": "南明", 
    "emperor": "朱由崧（南明弘光帝）",
    "birthDeath": "1607-1646年",
    "templeName": "安宗",
    "posthumousTitle": "奉天遵道宽和静穆修文布武温恭仁孝简皇帝",
    "experience": "南明首位皇帝，在南京即位，沉迷酒色荒于政事，党争不断，清军南下后被俘，押往北京处死"
},
{ 
    "dynasty": "南明", 
    "emperor": "朱聿键（南明隆武帝）",
    "birthDeath": "1602-1646年",
    "templeName": "绍宗",
    "posthumousTitle": "配天至道弘毅肃穆思文烈武敏仁广孝襄皇帝",
    "experience": "南明最有作为的皇帝，力图北伐抗清，联合农民军余部，无奈受制于权臣，最终被俘绝食而死"
},
{ 
    "dynasty": "南明", 
    "emperor": "朱聿鐭（南明绍武帝）",
    "birthDeath": "1605-1647年",
    "templeName": "文宗",
    "posthumousTitle": "贞天应道昭崇德毅宁文宏武达仁闵孝节皇帝",
    "experience": "在广州即位，与永历帝朱由榔争夺正统，爆发内战，清军趁机攻城，在位仅40天便自缢身亡"
},
{ 
    "dynasty": "南明", 
    "emperor": "朱由榔（南明永历帝）",
    "birthDeath": "1623-1662年",
    "templeName": "昭宗",
    "posthumousTitle": "应天推道敏毅恭俭经文纬武礼仁克孝匡皇帝",
    "experience": "南明末代皇帝，辗转西南各地抗清，依附李定国等部，最终被吴三桂俘获，在昆明绞杀，南明灭亡"
},
{ 
    "dynasty": "清", 
    "emperor": "皇太极（清太宗）",
    "birthDeath": "1592-1643年",
    "templeName": "太宗",
    "posthumousTitle": "应天兴国弘德彰武宽温仁圣睿孝敬敏昭定隆道显功文皇帝",
    "experience": "清朝开国皇帝，努尔哈赤第八子，改后金国号为“清”，正式建立清朝，统一东北全境，东征朝鲜、西征蒙古，完善八旗制度，为清军入关统一全国奠定坚实基础，猝死于入关前夕"
},
{ 
    "dynasty": "清", 
    "emperor": "福临（清世祖）",
    "birthDeath": "1638-1661年",
    "templeName": "世祖",
    "posthumousTitle": "体天隆运定统建极英睿钦文显武大德弘功至仁纯孝章皇帝",
    "experience": "顺治帝，清朝入关后首位皇帝，幼年即位由多尔衮辅政，清军逐步统一全国大部，亲政后整顿吏治、恢复生产，推崇汉文化，后期因董鄂妃病逝身心俱疲，最终早逝（亦有出家传闻）"
},
{ 
    "dynasty": "清", 
    "emperor": "玄烨（清圣祖）",
    "birthDeath": "1654-1722年",
    "templeName": "圣祖",
    "posthumousTitle": "合天弘运文武睿哲恭俭宽裕孝敬诚信中和功德大成仁皇帝",
    "experience": "康熙帝，中国历史上在位时间最长的皇帝，擒鳌拜、平三藩、收台湾、亲征噶尔丹、驱逐沙俄，开创“康乾盛世”的奠基之治，整顿吏治、发展生产，奠定清朝疆域版图"
},
{ 
    "dynasty": "清", 
    "emperor": "胤禛（清世宗）",
    "birthDeath": "1678-1735年",
    "templeName": "世宗",
    "posthumousTitle": "敬天昌运建中表正文武英明宽仁信毅睿圣大孝至诚宪皇帝",
    "experience": "雍正帝，历经“九子夺嫡”即位，推行摊丁入亩、火耗归公、官绅一体当差纳粮等改革，加强中央集权，设立军机处，肃清吏治、充盈国库，为乾隆盛世的到来铺平道路"
},
{ 
    "dynasty": "清", 
    "emperor": "弘历（清高宗）",
    "birthDeath": "1711-1799年",
    "templeName": "高宗",
    "posthumousTitle": "法天隆运至诚先觉体元立极敷文奋武钦明孝慈神圣纯皇帝",
    "experience": "乾隆帝，在位60年，后禅位为太上皇仍掌实权，“康乾盛世”达至顶峰，编纂《四库全书》，晚年好大喜功、闭关锁国，重用和珅，导致朝政腐败，清朝由盛转衰"
},
{ 
    "dynasty": "清", 
    "emperor": "颙琰（清仁宗）",
    "birthDeath": "1760-1820年",
    "templeName": "仁宗",
    "posthumousTitle": "受天兴运敷化绥猷崇文经武光裕孝恭勤俭端敏英哲睿皇帝",
    "experience": "嘉庆帝，即位后迅速诛杀权臣和珅，整顿吏治，试图扭转清朝衰败之势，无奈积重难返，白莲教起义席卷全国，消耗大量国力，清朝衰落进一步加剧"
},
{ 
    "dynasty": "清", 
    "emperor": "旻宁（清宣宗）",
    "birthDeath": "1782-1850年",
    "templeName": "宣宗",
    "posthumousTitle": "效天符运立中体正至文圣武智勇仁慈俭勤孝敏宽定成皇帝",
    "experience": "道光帝，力行节俭、整顿吏治，却难挽清朝颓势，鸦片战争爆发后战败，被迫签订中国近代史上首个不平等条约《南京条约》，中国开始沦为半殖民地半封建社会"
},
{ 
    "dynasty": "清", 
    "emperor": "奕𬣞（清文宗）",
    "birthDeath": "1831-1861年",
    "templeName": "文宗",
    "posthumousTitle": "协天翊运执中垂谟懋德振武圣孝渊恭端仁宽敏庄俭显皇帝",
    "experience": "咸丰帝，在位期间爆发太平天国运动，席卷南方半壁江山，第二次鸦片战争战败，英法联军火烧圆明园，被迫签订《天津条约》《北京条约》，内忧外患中病逝，留下顾命八大臣辅政"
},
{ 
    "dynasty": "清", 
    "emperor": "载淳（清穆宗）",
    "birthDeath": "1856-1875年",
    "templeName": "穆宗",
    "posthumousTitle": "继天开运受中居正保大定功圣智诚孝信敏恭宽明肃毅皇帝",
    "experience": "同治帝，幼年即位，慈禧太后与慈安太后垂帘听政，依靠曾国藩、李鸿章等大臣镇压太平天国运动，推行“洋务运动”，史称“同治中兴”，实则大权旁落，年仅19岁早逝"
},
{ 
    "dynasty": "清", 
    "emperor": "载湉（清德宗）",
    "birthDeath": "1871-1908年",
    "templeName": "德宗",
    "posthumousTitle": "同天崇运大中至正经文纬武仁孝睿智端俭宽勤景皇帝",
    "experience": "光绪帝，幼年被慈禧太后拥立，实为傀儡皇帝，亲政后力图维新变法，推行“戊戌变法”试图挽救清朝危亡，仅维持103天便被慈禧软禁，甲午中日战争、八国联军侵华接连战败，最终离奇病逝"
},
{ 
    "dynasty": "清", 
    "emperor": "溥仪（清末帝）",
    "birthDeath": "1906-1967年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "宣统帝，中国历史上最后一位皇帝，3岁即位，1912年辛亥革命后退位，清朝灭亡；后在日本扶持下建立伪满洲国傀儡政权，抗战胜利后被俘，经改造成为新中国普通公民，一生跌宕起伏"
},
{ 
    "dynasty": "南宋", 
    "emperor": "赵昺（宋末帝）",
    "birthDeath": "1272-1279年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "南宋末代皇帝，崖山海战中宋军战败，年仅7岁的赵昺被陆秀夫背着跳海殉国，南宋彻底灭亡，华夏第一次整体沦陷于异族"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李元昊（西夏景宗）",
    "birthDeath": "1003-1048年",
    "templeName": "景宗",
    "posthumousTitle": "武烈皇帝",
    "experience": "西夏开国皇帝，正式称帝建立西夏，创制西夏文字，击败宋辽联军，奠定西夏与宋辽三足鼎立格局，晚年荒淫残暴，被儿子宁令哥弑杀"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李秉常（西夏惠宗）",
    "birthDeath": "1061-1086年",
    "templeName": "惠宗",
    "posthumousTitle": "康靖皇帝",
    "experience": "幼年即位，由梁太后与梁乙埋专权，推行蕃礼压制汉礼，亲政后试图恢复汉制，引发内乱，在位期间西夏国力受损"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李乾顺（西夏崇宗）",
    "birthDeath": "1083-1139年",
    "templeName": "崇宗",
    "posthumousTitle": "圣文皇帝",
    "experience": "亲政后清除外戚势力，推行汉化改革，依附金朝对抗宋朝，拓展西夏疆域，使西夏进入稳定发展期"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李仁孝（西夏仁宗）",
    "birthDeath": "1124-1193年",
    "templeName": "仁宗",
    "posthumousTitle": "圣德皇帝",
    "experience": "西夏在位时间最长的皇帝，推崇儒学、完善科举，与金朝保持和平，国内经济文化繁荣，史称“仁宗盛治”，西夏达到鼎盛"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李纯祐（西夏桓宗）",
    "birthDeath": "1177-1206年",
    "templeName": "桓宗",
    "posthumousTitle": "昭简皇帝",
    "experience": "在位期间西夏开始衰落，蒙古崛起后多次侵扰边境，后被李安全发动政变推翻，不久后病逝"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李安全（西夏襄宗）",
    "birthDeath": "1170-1211年",
    "templeName": "襄宗",
    "posthumousTitle": "敬穆皇帝",
    "experience": "篡位登基，联蒙抗金却遭蒙古掠夺，与金朝连年征战两败俱伤，西夏国力急剧衰退，后被宗室废杀"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李遵顼（西夏神宗）",
    "birthDeath": "1163-1226年",
    "templeName": "神宗",
    "posthumousTitle": "英文皇帝",
    "experience": "西夏唯一以状元身份登基的皇帝，坚持联蒙抗金政策，导致西夏民穷国困，后期禅位于儿子李德旺，成为西夏唯一太上皇"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李德旺（西夏献宗）",
    "birthDeath": "1181-1226年",
    "templeName": "献宗",
    "posthumousTitle": "孝哀皇帝",
    "experience": "即位后试图改变联蒙政策，与金朝和解共同抗蒙，无奈蒙古势强，西夏接连战败，李德旺忧愤而死"
},
{ 
    "dynasty": "西夏", 
    "emperor": "李𪾢（西夏末主）",
    "birthDeath": "1204-1227年",
    "templeName": "无",
    "posthumousTitle": "无",
    "experience": "西夏末代皇帝，李德旺病逝后即位，蒙古大军攻破中兴府，李𪾢投降后被蒙古所杀，西夏灭亡"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜旻（金太祖）",
    "birthDeath": "1068-1123年",
    "templeName": "太祖",
    "posthumousTitle": "应乾兴运昭德定功睿神庄孝仁明大圣武元皇帝",
    "experience": "金国开国皇帝，统一女真各部，建立金国，率军击败辽国，创制女真文字，为金国灭辽、伐宋奠定基础"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜晟（金太宗）",
    "birthDeath": "1075-1135年",
    "templeName": "太宗",
    "posthumousTitle": "体元应运世德昭功哲惠仁圣文烈皇帝",
    "experience": "在位期间灭辽破宋，俘虏徽钦二帝，占据中原大片领土，完善金国官制与赋税制度，国力迅速强盛"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜亶（金熙宗）",
    "birthDeath": "1119-1150年",
    "templeName": "熙宗",
    "posthumousTitle": "弘基缵武庄靖孝成皇帝",
    "experience": "前期推行汉化改革，完善典章制度，后期酗酒嗜杀，朝政混乱，被完颜亮发动政变弑杀"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜亮（金海陵王）",
    "birthDeath": "1122-1161年",
    "templeName": "无",
    "posthumousTitle": "无（史称海陵王）",
    "experience": "弑君篡位，迁都燕京（中都），改革官制加强集权，发动伐宋战争失败，途中被部下弑杀"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜雍（金世宗）",
    "birthDeath": "1123-1189年",
    "templeName": "世宗",
    "posthumousTitle": "光天兴运文德武功圣明仁孝皇帝",
    "experience": "发动政变即位，推行“大定之治”，整顿吏治、与民休息，倡导节俭，金国进入鼎盛时期"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜璟（金章宗）",
    "birthDeath": "1168-1208年",
    "templeName": "章宗",
    "posthumousTitle": "宪天光运仁文义武神圣英孝皇帝",
    "experience": "延续汉化政策，文化、经济达金代顶峰，后期朝政腐败，蒙古崛起，金国由盛转衰"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜永济（金卫绍王）",
    "birthDeath": "1153-1213年",
    "templeName": "无",
    "posthumousTitle": "无（史称卫绍王）",
    "experience": "在位期间蒙古多次南侵，金国屡战屡败，后被权臣胡沙虎弑杀，政权动荡"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜珣（金宣宗）",
    "birthDeath": "1163-1224年",
    "templeName": "宣宗",
    "posthumousTitle": "继天兴统述道勤仁英武圣孝皇帝",
    "experience": "南迁汴京（开封），导致北方领土沦陷，与西夏、南宋交恶，三面受敌，金国国力急剧衰退"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜守绪（金哀宗）",
    "birthDeath": "1198-1234年",
    "templeName": "哀宗",
    "posthumousTitle": "敬天德运忠文靖武天圣烈孝庄皇帝",
    "experience": "力图抗蒙复国，联合西夏、南宋未果，蔡州被围后传位完颜承麟，自缢而死"
},
{ 
    "dynasty": "金", 
    "emperor": "完颜承麟（金末帝）",
    "birthDeath": "？-1234年",
    "templeName": "无",
    "posthumousTitle": "无（史称金末帝）",
    "experience": "中国历史上在位时间最短的皇帝，即位仅1小时便率军出战，战死沙场，金国灭亡"
},
{ 
    "dynasty": "元", 
    "emperor": "忽必烈（元世祖）",
    "birthDeath": "1215-1294年",
    "templeName": "世祖",
    "posthumousTitle": "圣德神功文武皇帝",
    "experience": "元朝开国皇帝，1271年改国号为元，1279年灭南宋统一中国，推行汉法与蒙古旧制并行，奠定元朝统治基础"
},
{ 
    "dynasty": "元", 
    "emperor": "铁穆耳（元成宗）",
    "birthDeath": "1265-1307年",
    "templeName": "成宗",
    "posthumousTitle": "钦明广孝皇帝",
    "experience": "守成之君，维持元朝疆域稳定，后期疏于朝政，权臣专权，朝政渐趋混乱"
},
{ 
    "dynasty": "元", 
    "emperor": "海山（元武宗）",
    "birthDeath": "1281-1311年",
    "templeName": "武宗",
    "posthumousTitle": "仁惠宣孝皇帝",
    "experience": "靠军权即位，挥霍无度，加重赋税与徭役，消耗国力，短暂在位后病逝"
},
{ 
    "dynasty": "元", 
    "emperor": "爱育黎拔力八达（元仁宗）",
    "birthDeath": "1285-1320年",
    "templeName": "仁宗",
    "posthumousTitle": "圣文钦孝皇帝",
    "experience": "推行“延祐复科”恢复科举，整顿吏治、推行汉化改革，元朝出现短暂清明"
},
{ 
    "dynasty": "元", 
    "emperor": "硕德八剌（元英宗）",
    "birthDeath": "1303-1323年",
    "templeName": "英宗",
    "posthumousTitle": "睿圣文孝皇帝",
    "experience": "锐意改革触动蒙古贵族利益，推行新政整顿弊政，最终爆发“南坡之变”被弑杀"
},
{ 
    "dynasty": "元", 
    "emperor": "也孙铁木儿（元泰定帝）",
    "birthDeath": "1276-1328年",
    "templeName": "无",
    "posthumousTitle": "无（史称泰定帝）",
    "experience": "由贵族拥立，维稳为主，无显著改革举措，在位期间朝政维持表面平静"
},
{ 
    "dynasty": "元", 
    "emperor": "阿速吉八（元天顺帝）",
    "birthDeath": "1320-1328年",
    "templeName": "无",
    "posthumousTitle": "无（史称天顺帝）",
    "experience": "与图帖睦尔争夺帝位，爆发“两都之战”，兵败被杀，在位仅1个月"
},
{ 
    "dynasty": "元", 
    "emperor": "图帖睦尔（元文宗）",
    "birthDeath": "1304-1332年",
    "templeName": "文宗",
    "posthumousTitle": "圣明元孝皇帝",
    "experience": "两度登基，热衷文化建设，编纂《经世大典》，朝政被权臣燕帖木儿操控"
},
{ 
    "dynasty": "元", 
    "emperor": "和世㻋（元明宗）",
    "birthDeath": "1300-1329年",
    "templeName": "明宗",
    "posthumousTitle": "翼献景孝皇帝",
    "experience": "被图帖睦尔迎立为帝，即位后不久便被毒杀，史称“天历之变”"
},
{ 
    "dynasty": "元", 
    "emperor": "懿璘质班（元宁宗）",
    "birthDeath": "1326-1332年",
    "templeName": "宁宗",
    "posthumousTitle": "冲圣嗣孝皇帝",
    "experience": "幼年即位，在位仅53天便病逝，权臣继续掌控朝政"
},
{ 
    "dynasty": "元", 
    "emperor": "妥懽帖睦尔（元惠宗）",
    "birthDeath": "1320-1370年",
    "templeName": "惠宗",
    "posthumousTitle": "宣仁普孝皇帝（史称元顺帝）",
    "experience": "元朝末代皇帝，前期力图改革失败，后期荒淫无道，明军北伐后逃亡漠北，元朝灭亡"
},
{ 
    "dynasty": "北元", 
    "emperor": "爱猷识理答腊（北元昭宗）",
    "birthDeath": "1339-1378年",
    "templeName": "昭宗",
    "posthumousTitle": "无",
    "experience": "元顺帝之子，北元首位君主，力图组织反攻复国，与明朝多次交战未果，国力日渐衰弱"
},
{ 
    "dynasty": "北元", 
    "emperor": "脱古思帖木儿（北元益宗）",
    "birthDeath": "1342-1388年",
    "templeName": "益宗",
    "posthumousTitle": "无",
    "experience": "北元末代君主，被明军在捕鱼儿海击败，主力尽失，后被部下也速迭儿弑杀，北元政权名存实亡"
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
