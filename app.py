from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
# from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate

app = Flask(__name__)
print("body")  

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'lyNxRy1rYRDTvdmcuufHqZbFiaFQruKN3ClJ5xXm5P6+1u+m9l32lye8p5W76iaDy2bqT6rxB4szS/37wE+3bFopLOwm0PSO2BjQJRTXl2MW73yHhL4KgYhiX1Ps/E6oZdR9FwsVBPWXCXj9FfP49AdB04t89/1O/w1cDnyilFU='
        secret = '10dcc9676f2f97281be46d562a636ea3'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()
    
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    ConfirmTemplate,
    MessageAction,
    TextMessage,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)
import os

app = Flask(__name__)
configuration = Configuration(access_token=os.getenv('YOUR_CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('YOUR_CHANNEL_SECRET'))
# configuration = Configuration(access_token='lyNxRy1rYRDTvdmcuufHqZbFiaFQruKN3ClJ5xXm5P6+1u+m9l32lye8p5W76iaDy2bqT6rxB4szS/37wE+3bFopLOwm0PSO2BjQJRTXl2MW73yHhL4KgYhiX1Ps/E6oZdR9FwsVBPWXCXj9FfP49AdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('10dcc9676f2f97281be46d562a636ea3')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#加入好友事件
@line_handler.add(FollowEvent)
def handler_follow(event):
    with ApiClient(configuration) as api_client:
        # line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text='歡迎光臨甲骨翻譯社智慧聊天室系統，若下列項目都無法滿足您的需求，請直接留言即可，會有專員跟您聯繫。')]
        #     )
        # )

        line_bot_api = MessagingApi(api_client)
        buttons_template = ButtonsTemplate(
            # thumbnail_image_url=url,
            # title='Postback Sample',
            text='歡迎光臨甲骨翻譯社智慧聊天室系統，若下列項目都無法滿足您的需求，請直接留言即可，會有專員跟您聯繫。\n請選擇您的問題',
            actions=[
                PostbackAction(label='文件翻譯', text='文件翻譯', data='event_Translate'),
                PostbackAction(label='文件公證', text='文件公證', data='event_NT'),
                # PostbackAction(label='英國簽證', text='英國簽證', data='event_UK'),
                PostbackAction(label='錄音聽打', text='錄音聽打', data='event_Record'),
                PostbackAction(label='匯款資訊', text='匯款資訊', data='event_Bank')
            ]
        )
        template_message = TemplateMessage(
            alt_text='Postback Sample',
            template=buttons_template
        )
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )
    # print(f'Got {event.type} event')


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # if event.message.text == '111':
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text=event.message.text)]
        #         )
        #     )
        if event.message.text == '1':
            # url = request.url_root + 'img/title.jpg'
            # url = url.replace("http", "https")
            # app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                # thumbnail_image_url=url,
                # title='Postback Sample',
                text='請選擇您的問題',
                actions=[
                    PostbackAction(label='文件翻譯', text='文件翻譯', data='event_Translate'),
                    PostbackAction(label='文件公證', text='文件公證', data='event_NT'),
                    # PostbackAction(label='英國簽證', text='英國簽證', data='event_UK'),
                    PostbackAction(label='錄音聽打', text='錄音聽打', data='event_Record'),
                    PostbackAction(label='匯款資訊', text='匯款資訊', data='event_Bank')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        elif event.message.text == '文件翻譯':  # 如果回傳值為「event_Translate」
            buttons_template = ButtonsTemplate(
                text='請選擇您的問題',
                actions=[
                    PostbackAction(label='文件書本翻譯', text='文件書本翻譯', data='event_Bank'),
                    PostbackAction(label='英國簽證', text='英國簽證', data='event_UK'),
                    PostbackAction(label='財務報表', text='報表翻譯', data='event_Record'),
                    PostbackAction(label='回首頁', text='1', data='1')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

@line_handler.add(PostbackEvent)
def handler_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == 'event_Translate_1':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='請將要翻譯的檔案上傳，我們評估後會盡快回覆您報價。')]
                )
            )
        elif postback_data == 'event_NT':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='event_NT')]
                )
            )
        if postback_data == 'event_UK':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='請準備30天的銀行交易明細，並且上傳到此LINE帳號。\n我們評估後會盡快回覆您報價。')]
                )
            )
        elif postback_data == 'event_Record':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='請將要錄音聽打的檔案上傳，我們評估後會盡快回覆您報價。')]
                )
            )
        elif postback_data == 'event_Bank':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='玉山銀行，銀行代號 : 808\n帳號 : 1234567890')]
                )
            )

# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )

if __name__ == "__main__":
    app.run()