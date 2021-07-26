# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com

#
import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)


idf = open("../id.txt")
YOUR_CHANNEL_ACCESS_TOKEN = idf.readline().rstrip()  # remove newline
YOUR_CHANNEL_SECRET = idf.readline().rstrip()  # remove newline


class line_menu_maker:
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)


with open("control.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-762...", "image/jpeg", f)
    default_menu = {
        "header": {"Authorization": "Bearer " + YOUR_CHANNEL_ACCESS_TOKEN,
                   "Content-Type": "application/json"},
        "body": {
            "size": {"width": 2500, "height": 1686},
            "selected": "true",
            "name": "Controller",
            "chatBarText": "Controller",
            "areas": [
                {
                    "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
                    "action": {"type": "message", "text": "up"}
                },
                {
                    "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
                    "action": {"type": "message", "text": "right"}
                },
                {
                    "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
                    "action": {"type": "message", "text": "down"}
                },
                {
                    "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
                    "action": {"type": "message", "text": "left"}
                },
                {
                    "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
                    "action": {"type": "message", "text": "btn b"}
                },
                {
                    "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
                    "action": {"type": "message", "text": "btn a"}
                }
            ]
        }
    }  # default menu

    def reg_a_menu(self):
        req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                               headers=self.default_menu["header"], data=json.dumps(self.default_menu["body"]).encode('utf-8'))
        print(req.text)
        f = open("default_rich_menu.txt", "a")
        f.write('default rich menu Id: '+req.text)

    def list_all_rich_menus(self):
        rich_menu_list = self.line_bot_api.get_rich_menu_list()
        print("All Rich Menus:")
        for rich_menu in rich_menu_list:
            print(rich_menu.rich_menu_id)

    def set_menu_image(self, menu_id)
    rich_menu_list = self.line_bot_api.get_rich_menu_list()
    rich_menu_id = rich_menu_list[0].rich_menu_id
    with open("control.jpg", 'rb') as f:
        self.line_bot_api.set_rich_menu_image(
            rich_menu_id, "image/jpeg", f)


rich_menus = line_menu_maker()

while True:
    print('************** linebot rich menu making tool ** ****************************')
    print('      1. Register the default rich menu')
    print('      2. Legister the default rich menu')

    command = input('Line Rich menu maker (1..6 ...): ')

    if len(command) < 1:
        print('do nothing')
        break

    if command == '1':
        rich_menus.reg_a_menu()
        break

    if command == '2':
        rich_menus.list_all_rich_menus()

        break
