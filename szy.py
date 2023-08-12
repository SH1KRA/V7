from datetime import datetime, timedelta
import json
import requests
from lunardate import LunarDate

def send_weather_report():
    # 获取天气数据
    api_key = "0fd11deb4556496a8d30d5253f33e44e"
    location = "101230101"
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={api_key}"
    response = requests.get(url)
    json_obj = json.loads(response.text)

    today_weather = json_obj["daily"][0]

    # 计算日期
    today = datetime.now().date()
    qwq_birthday = LunarDate(2002, 4, 24)
    sz_birthday = LunarDate(2001, 4, 16)
    anniversary = datetime(2023, 3, 27).date()

    qwq_birthday_solar = qwq_birthday.toSolarDate()
    sz_birthday_solar = sz_birthday.toSolarDate()

    qwq_days_left = (qwq_birthday_solar.replace(year=today.year) - today).days
    if qwq_days_left < 0:
        qwq_days_left = (qwq_birthday_solar.replace(year=today.year + 1) - today).days

    sz_days_left = (sz_birthday_solar.replace(year=today.year) - today).days
    if sz_days_left < 0:
        sz_days_left = (sz_birthday_solar.replace(year=today.year + 1) - today).days

    days_together = (today - anniversary).days

    # 提示信息
    extra_tips = ""

    if '雨' in today_weather['textDay'] or '雨' in today_weather['textNight']:
        extra_tips += "今天会下雨，出门记得带伞☂️嗷。\n"

    if float(today_weather["tempMin"]) < 25:
        extra_tips += "今晚👻会冷滴，记得带个外套🧥嗷。\n"

    if float(today_weather["uvIndex"]) >= 6:
        extra_tips += "今天紫外线较强，出门请涂抹防晒霜。\n"

    message = f"""
商梓🐷专属天气推送
🌤️ {today_weather["fxDate"]} 天气预报
-------------------
☀️白天天气：<font color="red">{today_weather['textDay']}</font>
🌙夜间天气：<font color="red">{today_weather['textNight']}</font>
最高温度：<font color="red">{today_weather['tempMax']}℃</font>
最低温度：<font color="red">{today_weather['tempMin']}℃</font>
我们在一起已经<font color="red">{days_together}</font>天了
{extra_tips}
"""

    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c703030a-7443-496d-803a-0487614adbdd"

    wechat_message = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }

    headers = {'Content-Type': 'application/json'}
    result = requests.post(webhook_url, json.dumps(wechat_message, ensure_ascii=False).encode('utf-8'), headers=headers)

    return result.status_code == 200

send_weather_report()