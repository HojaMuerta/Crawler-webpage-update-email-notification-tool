import datetime, time
import re
import smtplib
import requests
from bs4 import BeautifulSoup


def get_new():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
                    (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}  # 设置headers信息，模拟成浏览器取访问网站
    req = requests.get("http://yjsy.cmc.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016", headers=headers)  # 向网站发起请求，并获取响应对象
    req.encoding = "utf-8"
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")
    time_items = soup.find_all(text="2022-04-01")
    print(time_items)
    return time_items  # 运行get_new()函数，会返回值


def update():
    print('通知系统启动中')
    old_pattern = get_new()  # 记录原始内容列表
    while True:
        new_pattern = get_new()  # 记录新内容列表
        # new_pattern = ['2022-04-01', '2022-04-01', '2022-04-01', '2022-04-01']
        if new_pattern != old_pattern:  # 判断内容列表是否更新
            old_pattern = new_pattern  # 原始内容列表改变
            send_email()  # 发送邮件
        else:
            now = datetime.datetime.now()
            print(now, "尚无更新")
        time.sleep(3)  # 五分钟检测一次


def send_email():
    HOST = 'smtp.qq.com'  # 邮箱smtp
    PORT = '465'
    send_mail = '*****8@qq.com'  # 发送人邮箱
    get_mail = '****9@qq.com'  # 收件人邮箱
    title = '有更新，速查！！！'  # 邮件标题
    new_pattern = get_new()  # 提取网页内容列表
    context = new_pattern[0]  # 邮件内容
    # context = "test"
    smtp = smtplib.SMTP_SSL(HOST, 465)  # 启用SSL发信, 端口一般是465
    res = smtp.login(user=send_mail, password='snvohsbdjci')  # 登录验证，password是邮箱授权码而非密码，需要去网易邮箱手动开启
    print('发送结果：', res)
    msg = '\n'.join(
        ['From: {}'.format(send_mail), 'To: {}'.format(get_mail), 'Subject: {}'.format(title), '', context])
    smtp.sendmail(from_addr=send_mail, to_addrs=get_mail, msg=msg.encode('utf-8'))  # 发送邮件
    print(context)


if __name__ == '__main__':
    update()
