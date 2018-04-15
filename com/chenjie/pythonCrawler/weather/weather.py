#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
python 3.6
抓取中国天气网上面的最近7天的天气数据
url :http://www.weather.com.cn/weather/101280101.shtml
"""
import requests
import bs4

def get_html(url) :
    # 封装请求
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType':'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
    }
    try:
        htmlcontent = requests.get(url,headers=headers,timeout=30)
        htmlcontent.raise_for_status()
        htmlcontent.encoding='utf-8'
        return  htmlcontent.content
    except :
        return '请求失败'

def get_content(url):
    # 抓取页面天气数据
    weather_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html,'lxml')
    # print('抓取到的整个页面的源代码是:',soup)
    content_ul = soup.find('ul',class_='t').find_all('li')
    for the_content in content_ul :
        try :
            weatherobj = {}
            print(the_content.find('h1'))
            weatherobj['days'] = the_content.find('h1').text
            weatherobj['height_temp'] = the_content.find('p', class_='tem').span.text
            weatherobj['low_temp'] = the_content.find('p', class_='tem').i.text
            weather_list.append(weatherobj)
        except :
            print('查询不到天气信息!')
    print('抓取到的天气情况是:',weather_list)
    write_result_to_txt(weather_list)

def write_result_to_txt(the_result) :
    # 将抓取到的结果写入当前目录下的txt文件中
    # the_result = str(the_result)
    result = '日期          气温\n'
    for temp_obj in the_result :
        result += temp_obj['days']+'  '+temp_obj['height_temp']+'/'+temp_obj['low_temp']+'\n'
    file = open('weather_result.txt', 'a')
    file.write(result + '\n')
    file.close()

if __name__ == '__main__' :
    url = 'http://www.weather.com.cn/weather/101280101.shtml'
    get_content(url)

