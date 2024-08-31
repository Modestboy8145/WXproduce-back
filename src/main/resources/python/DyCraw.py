# -*- coding: utf8 -*-
import requests  # 数据请求库第三方库
import re  # 正则模块
import json
import sys

# 伪装请求头方式/请求头参数
headers = {
    'cookie': 'ttwid=1%7Cfvq1MDgcqlTGGR5coTYXM3un0u3MdSujKf5dbcY_DLo%7C1723355773%7C06fdd508f92df785db38aa8fa8082d669b82f619b244a56d96cdd7383f23dd98; UIFID_TEMP=a6000b6bd0597977c28c1dbb751d8a8c80ef4c078dbea6da280536e6f6924b8290a994698cea9ee82c4e844cfe157a629657ae865483234498d3d88caab427cba0b71936bd2f1252d887167171afcad9; s_v_web_id=verify_lzp5j86b_RE2L8JYl_jXKb_4fIN_8tWc_0FlE0fcp2isd; passport_csrf_token=4c0ec3f66595d91cd68543e53359a7bd; passport_csrf_token_default=4c0ec3f66595d91cd68543e53359a7bd; fpk1=U2FsdGVkX1+Uks6E0Ivi5tOIPsPjFhGBv0Z2KgRDiGr2LZRnjN8YM8XRfeDZ3lz5lXwpbOIQkZLr6EAcLcKgqA==; fpk2=c28c178f7fc01e92a5161b6c80153add; bd_ticket_guard_client_web_domain=2; UIFID=a6000b6bd0597977c28c1dbb751d8a8c80ef4c078dbea6da280536e6f6924b8293d206240588933ba483533554ecb23280effd80ee118cc2fb8b1a1e97d166395c31f66380aa86d310920d48a8a1fe2a01f5f3ed3125328d8804fd04fc6ba280a6b499549d0e14db1b92f3efab823ad82366ed632f832577601c2d3abe1a2ce034e1e83cd9e1247c365dcfddf313e57cc1b947721dc1af85534ec5fca3bf5f63; d_ticket=b7f039c567e17cc8c595e724398ff662cd055; n_mh=UXgMlLR9pi1IxcFZ7CE2JX-V5-j3Tpu9Z1wV7LAAb58; sso_auth_status=19f329cef8262834ce253ed7ef552e6d; sso_auth_status_ss=19f329cef8262834ce253ed7ef552e6d; passport_auth_status=0d2f0f8770e940df726c28d6e3d3f174%2Cdba5d1e35a6192435ac6564197542620; passport_auth_status_ss=0d2f0f8770e940df726c28d6e3d3f174%2Cdba5d1e35a6192435ac6564197542620; is_staff_user=false; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region=cn-gx; store-region-src=uid; live_use_vvc=%22false%22; MONITOR_WEB_ID=f5c85603-6212-4bf8-9fe5-7ec547a0e596; xgplayer_user_id=836764525116; passport_assist_user=CkE7VQyFfS4WVNPtcth5jaQSiFUr6SebHbWAfInWi0vnKtxf-HewG9BulBRjxc5CfNAzgdL3Gzslidc5DgEyUwfatRpKCjxJ_u_s3B4bqu5YrkdoYV687Daj1rf2RUoA27bjkX4_Zv64W04FCh3umJ32EuGvYnc_1Eceal4MLIT7qV8Qrq_ZDRiJr9ZUIAEiAQMZOHBi; sso_uid_tt=785fa1f061d06ef491220fff084a46d0; sso_uid_tt_ss=785fa1f061d06ef491220fff084a46d0; toutiao_sso_user=11f8d631000befefbe6370c135d50fdc; toutiao_sso_user_ss=11f8d631000befefbe6370c135d50fdc; sid_ucp_sso_v1=1.0.0-KGFlNWFmZjVlMGZiNzQ0MjhiYjBhODgzYWNhYmE4OGQzNzFmNTY5NDQKIQiI6IDl2YyWBhDUxfK1BhjvMSAMMOyX54oGOAVA-wdIBhoCbHEiIDExZjhkNjMxMDAwYmVmZWZiZTYzNzBjMTM1ZDUwZmRj; ssid_ucp_sso_v1=1.0.0-KGFlNWFmZjVlMGZiNzQ0MjhiYjBhODgzYWNhYmE4OGQzNzFmNTY5NDQKIQiI6IDl2YyWBhDUxfK1BhjvMSAMMOyX54oGOAVA-wdIBhoCbHEiIDExZjhkNjMxMDAwYmVmZWZiZTYzNzBjMTM1ZDUwZmRj; uid_tt=d42b5d0422ca68da477b9d3f26670763; uid_tt_ss=d42b5d0422ca68da477b9d3f26670763; sid_tt=e5f584a3f0b6580f7216a31069a7ec0d; sessionid=e5f584a3f0b6580f7216a31069a7ec0d; sessionid_ss=e5f584a3f0b6580f7216a31069a7ec0d; _bd_ticket_crypt_cookie=4ce7f1debd0eb353be187177847b47ef; sid_guard=e5f584a3f0b6580f7216a31069a7ec0d%7C1723638496%7C5183991%7CSun%2C+13-Oct-2024+12%3A28%3A07+GMT; sid_ucp_v1=1.0.0-KDQ3YzM1NzhiZGNjNjU1NDNlYWI3OTFiMjI0MWM2ZTg3YzJlNTI0MTIKGwiI6IDl2YyWBhDgxfK1BhjvMSAMOAVA-wdIBBoCaGwiIGU1ZjU4NGEzZjBiNjU4MGY3MjE2YTMxMDY5YTdlYzBk; ssid_ucp_v1=1.0.0-KDQ3YzM1NzhiZGNjNjU1NDNlYWI3OTFiMjI0MWM2ZTg3YzJlNTI0MTIKGwiI6IDl2YyWBhDgxfK1BhjvMSAMOAVA-wdIBBoCaGwiIGU1ZjU4NGEzZjBiNjU4MGY3MjE2YTMxMDY5YTdlYzBk; my_rd=2; __ac_signature=_02B4Z6wo00f01eihVZgAAIDAN.qm1VH7grnogVEAAByYcf; _tea_utm_cache_6383={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; _tea_utm_cache_2018={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; _tea_utm_cache_1300={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; architecture=amd64; dy_swidth=1920; dy_sheight=1080; csrf_session_id=55fbfe437f572a2711992f0ce57e374c; strategyABtestKey=%221724393057.295%22; biz_trace_id=376c5287; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSkwxa09DTGhsd04wZDdiQXEydUU5WmdNMlNWWkpwUmpWaGhEZHU2KzZlczFwZU5sYWYrVjdXVmQ2TWlJOUh5cW92L0ZYRG5YbUlrQ1ZNZDdrY1J6SVk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; publish_badge_show_info=%220%2C0%2C0%2C1724393059048%22; xg_device_score=7.658235294117647; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; odin_tt=087b85ebd66674daa2c7726809fe5c0b40b03188e2aa9dfd709bd8c2adf78a464ffe0d2ab0c5528a9baf6e20eae94b2853bb795df555081f87bbbb1f76f052ae; download_guide=%221%2F20240823%2F0%22; pwa2=%220%7C0%7C1%7C0%22; passport_fe_beating_status=false; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70 '
}


def DyVideoCraw(url):
    response = requests.get(url=url, headers=headers)
    # 获取网页源代码
    # print(response.text)
    try:
        html_date = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script', response.text)[0]
        html_date = requests.utils.unquote(html_date)
        # print(html_date)
        # 解析出标题
        title_data = re.findall('"desc":"(.*?)","', html_date)[0]
        # print(title_date)
        # 解析出封面
        cover_data = 'https:' + re.findall('originCover":"(.*?)","', html_date)[0]
        # print(cover_date)
        # 解析出视频地址
        date1 = re.findall('playAddr(.*?),', html_date)[0]
        video_url = 'https:' + re.findall('"src":"(.*?)"}', date1)[0]
        # print(video_url)
        video_obj = {
            "type": "video",
            "video": video_url,
            "title": title_data,
            "cover": cover_data
        }
        r_data = json.dumps(video_obj)
        print(r_data)
    except IndexError:
        print("1")




def DyImageCraw(url):
    response = requests.get(url=url, headers=headers)
    # 获取网页源代码
    # print(response.text)
    try:
        html_date = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script', response.text)[0]
        html_date = requests.utils.unquote(html_date)
        # print(html_date)
        # 解析出标题
        title_date = re.findall('"desc":"(.*?)","', html_date)[0]
        # print(title_date)
        # 解析出图片地址
        date1 = re.findall('"images":\[(.*?)],"imageInfos"', html_date)[0]
        date1 = re.findall('"urlList":\["(.*?)"],"downloadUrlList', date1)
        images_list = []
        for i in date1:
            images_list.append(i.split('","')[0])
        images_obj = {
            "type": "image",
            "images": images_list,
            "title": title_date
        }
        r_data = json.dumps(images_obj)
        print(r_data)
    except IndexError:
        print("1")


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append(sys.argv[i])
    # print(a[0])
    if a[0][23:28]=='video':
        DyVideoCraw(a[0])
    else:
        DyImageCraw(a[0])