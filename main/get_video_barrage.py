import json
import re
from main import public_smalltool as mytool

# 根据视频的av号获取cid
def get_cid(av_full, log_general_folder):
    av_id = av_full.strip('av')
    uri = f'https://api.bilibili.com/x/player/pagelist?aid={av_id}&jsonp=jsonp'
    status, res = mytool.download_website_page(uri)
    if status == -1:
        return -1, 0
    res_text = res.text
    res_dict = json.loads(res_text)
    response_code = res_dict['code']
    if response_code != 0:
        mytool.bugavid_file_write(av_full, f'{log_general_folder}\\av_id_404_list.txt')  # 将不存在的视频av号写入txt
        return -1, 0
    else:
        cid = res_dict['data'][0]['cid']
        return 0, cid

# 根据cid获取弹幕列表
def get_barragelist(cid):
    video_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    status, video_url_res = mytool.download_website_page(video_url)
    res_xml = video_url_res.content.decode('utf-8')
    pattern = re.compile('<d.*?>(.*?)</d>')
    barrage_list = pattern.findall(res_xml)
    return barrage_list

# 把弹幕写到文件中
def save_barrage_to_file(barrage_list, barrage_filename):
    if mytool.checkFileExist(barrage_filename):
        print('该弹幕文件已存在')
    else:
        with open(barrage_filename, mode='w', encoding='utf-8') as f:
            for barrage in barrage_list:
                f.write(barrage)
                f.write('\n')

# 弹幕获取主函数
def vb_main(av_id, barrage_filename,log_general_folder):
    status, av_cid = get_cid(av_id, log_general_folder)
    if status == -1:
        print("弹幕获取失败，进行下一个视频弹幕获取")
        return -1
    else:
        barrage_list = get_barragelist(av_cid)
        save_barrage_to_file(barrage_list, barrage_filename)
        return 0
