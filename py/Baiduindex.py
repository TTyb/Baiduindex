# !/usr/bin/python3.4
# -*- coding: utf-8 -*-


# 百度指数的抓取
# 截图教程：http://www.myexception.cn/web/2040513.html
#
# 登陆百度地址：https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F
# 百度指数地址：http://index.baidu.com

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract


# 打开浏览器
def openbrowser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # 打开谷歌浏览器
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    # 打开浏览器时间
    # print("等待10秒打开浏览器...")
    # time.sleep(10)

    # 找到id="TANGRAM__PSP_3__userName"的对话框
    # 清空输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    # 输入账号密码
    account = []
    try:
        fileaccount = open("../baidu/account.txt", encoding='UTF-8')
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        input("请正确在account.txt里面写入账号密码")
        exit()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # 点击登陆登陆
    # id="TANGRAM__PSP_3__submit"
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    # print('等待登陆10秒...')
    # time.sleep(10)
    print("等待网址加载完毕...")

    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    while 1:
        if select == "y" or select == "Y":
            print("登陆成功！")
            print("准备打开新的窗口...")
            # time.sleep(1)
            # browser.quit()
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":

                # 找到id="TANGRAM__PSP_3__userName"的对话框
                # 清空输入框
                browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
                browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

                # 输入账号密码
                account = []
                try:
                    fileaccount = open("../baidu/account.txt", encoding='UTF-8')
                    accounts = fileaccount.readlines()
                    for acc in accounts:
                        account.append(acc.strip())
                    fileaccount.close()
                except Exception as err:
                    print(err)
                    input("请正确在account.txt里面写入账号密码")
                    exit()

                browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
                browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])
                # 点击登陆sign in
                # id="TANGRAM__PSP_3__submit"
                browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

            elif selectno == "1":
                # 验证码的id为id="ap_captcha_guess"的对话框
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")

        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")


def getindex(keyword, day):
    openbrowser()
    time.sleep(2)

    # 这里开始进入百度指数
    # 要不这里就不要关闭了，新打开一个窗口
    # http://blog.csdn.net/DongGeGe214/article/details/52169761
    # 新开一个窗口，通过执行js来新开一个窗口
    js = 'window.open("http://index.baidu.com");'
    browser.execute_script(js)
    # 新窗口句柄切换，进入百度指数
    # 获得当前打开所有窗口的句柄handles
    # handles为一个数组
    handles = browser.window_handles
    # print(handles)
    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    # 在新窗口里面输入网址百度指数
    # 清空输入框
    time.sleep(5)
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    # 点击搜索
    # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    browser.find_element_by_id("searchWords").click()
    time.sleep(5)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)
    # 构造天数
    sel = '//a[@rel="' + str(day) + '"]'
    browser.find_element_by_xpath(sel).click()
    # 太快了
    time.sleep(2)
    # 滑动思路：http://blog.sina.com.cn/s/blog_620987bf0102v2r8.html
    # 滑动思路：http://blog.csdn.net/zhouxuan623/article/details/39338511
    # 向上移动鼠标80个像素，水平方向不同
    # ActionChains(browser).move_by_offset(0,-80).perform()
    # <div id="trend" class="R_paper" style="height:480px;_background-color:#fff;"><svg height="460" version="1.1" width="954" xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; position: relative; left: -0.5px;">
    # <rect x="20" y="130" width="914" height="207.66666666666666" r="0" rx="0" ry="0" fill="#ff0000" stroke="none" opacity="0" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); opacity: 0;"></rect>
    # xoyelement = browser.find_element_by_xpath('//rect[@stroke="none"]')
    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
    num = 0
    # 获得坐标长宽
    # x = xoyelement.location['x']
    # y = xoyelement.location['y']
    # width = xoyelement.size['width']
    # height = xoyelement.size['height']
    # print(x,y,width,height)
    # 常用js:http://www.cnblogs.com/hjhsysu/p/5735339.html
    # 搜索词：selenium JavaScript模拟鼠标悬浮
    x_0 = 1
    y_0 = 0

    if day == "all":
        day = 1000000

    # 储存日期和数字的数组
    index = {}
    consecutive_data_missing = 0
    try:
        # webdriver.ActionChains(driver).move_to_element().click().perform()
        # 只有移动位置xoyelement[2]是准确的
        for i in range(day):
            # 坐标偏移量???
            ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()

            # 构造规则
            if day == 7:
                x_0 = x_0 + 202.33
            elif day == 30:
                x_0 = x_0 + 41.68
            elif day == 90:
                x_0 = x_0 + 13.64
            elif day == 180:
                x_0 = x_0 + 6.78
            elif day == 1000000:
                x_0 = x_0 + 3.37222222
            time.sleep(2)
            # <div class="imgtxt" style="margin-left:-117px;"></div>
            imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
            date = browser.find_element_by_xpath('//div[@id="viewbox"]/div[1]/div[1]').text
            if date and len(date.strip().split(' ')) > 1:
                date = date.strip().split(' ')[0]
            else:
                print(f'WARN: unrecognized date: {date}')
                consecutive_data_missing += 1
                # quit trying when there are 5 consecutive blank indexes
                if consecutive_data_missing >= 5:
                    break
                else:
                    continue
            consecutive_data_missing = 0

            # 找到图片坐标
            locations = imgelement.location
            # 跨浏览器兼容
            scroll = browser.execute_script("return window.scrollY;")
            top = locations['y'] - scroll
            # 找到图片大小
            sizes = imgelement.size
            # 构造关键词长度
            add_length = (len(keyword) - 2) * sizes['width'] / 15
            # 构造指数的位置
            rangle = (
            int(locations['x'] + sizes['width'] / 4 + add_length), int(top + sizes['height'] / 2),
            int(locations['x'] + sizes['width'] * 2 / 3), int(top + sizes['height']))
            # 截取当前浏览器
            path = "../baidu/" + str(num)
            browser.save_screenshot(str(path) + ".png")
            # 打开截图切割
            img = Image.open(str(path) + ".png")
            jpg = img.crop(rangle)
            jpg.save(str(path) + ".jpg")

            # 将图片放大一倍
            # 原图大小73.29
            jpgzoom = Image.open(str(path) + ".jpg")
            (x, y) = jpgzoom.size
            x_s = 146
            y_s = 58
            out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
            out.save(path + 'zoom.jpg', 'png', quality=95)

            # 图像识别
            try:
                image = Image.open(str(path) + "zoom.jpg")
                code = pytesseract.image_to_string(image) or ''
            except:
                code = ''
            index[date] = code
            num = num + 1

    except Exception as err:
        print(err)
        print(num)

    print(index)
    file = open("../baidu/index.csv", "w")
    file.write('date,score\n')
    for date, score in index.items():
        file.write(f'{date},{score}\n')
    file.close()


if __name__ == "__main__":
    # 每个字大约占横坐标12.5这样
    # 按照字节可自行更改切割横坐标的大小rangle
    keyword = input("请输入查询关键字：")
    sel = int(input("查询7天请按0，30天请按1，90天请按2，半年请按3，全部请按4："))
    day = 0
    if sel == 0:
        day = 7
    elif sel == 1:
        day = 30
    elif sel == 2:
        day = 90
    elif sel == 3:
        day = 180
    elif sel == 4:
        day = "all"
    getindex(keyword, day)
