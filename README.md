# AstrBot-我要当皇帝插件
发送关键词随机抽取中国历史皇帝，展示皇帝生卒、庙号、谥号、核心经历，内嵌数据无需外部文件。

## 🎯 核心功能
- 多触发词支持：自然语言直接触发（无需 `/` 前缀），如「我要当皇帝」「来个皇帝」「朕要登基」「抽皇帝」等；
- 丰富信息展示：抽取后展示皇帝所属朝代、生卒年份、庙号、谥号、核心历史经历；

## 🚀 触发方式
### 1. 自然语言触发
直接在群/私聊发送以下关键词即可：
`我要当皇帝` / `来个皇帝` / `抽皇帝` / `随机皇帝` / `朕要登基` / `选个皇帝`

### 2. 指令触发
发送带 `/` 前缀指令：
`/我要当皇帝` / `/抽皇帝` / `/皇帝抽奖状态`

## 📋 状态查询
发送 `/皇帝抽奖状态`，可查看插件加载的皇帝数据量、支持的触发词、运行状态。

## ✨ 自定义扩展
如需添加更多皇帝数据，直接修改 `main.py` 中 `CONFIG["emperor_list"]` 列表即可，格式参考现有秦朝皇帝数据，新增字段会自动适配默认值。

## 📦 安装方式
1. 下载插件压缩包；
2. 在 AstrBot 后台「插件管理」上传安装；
3. 重载插件即可使用（无需重启机器人）。

# Supports

- [AstrBot Repo](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot Plugin Development Docs (Chinese)](https://docs.astrbot.app/dev/star/plugin-new.html)
- [AstrBot Plugin Development Docs (English)](https://docs.astrbot.app/en/dev/star/plugin-new.html)
