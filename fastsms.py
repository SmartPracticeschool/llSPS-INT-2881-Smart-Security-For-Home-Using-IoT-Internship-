import requests


r=requests.get("https://www.fast2sms.com/dev/bulk?authorization=Pg1DKz8AwHGL0ydvitrfxsamoWkIC4O95ZYNbnqechUul62jTR3QjpwZOLDEeutbHBGd1iNmWMc2krUP&sender_id=FSTSMS&message=EMERGENCY ALERT:SOMEONE IS IN DANGER..&language=english&route=p&numbers=8179639950")


print(r.status_code)
