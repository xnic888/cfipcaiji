import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
       'https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz'
        # 'https://stock.hostmonit.com/CloudFlareYes'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址,则写入文件
            for ip in ip_matches:
                file.write(ip + '\n')
    
    # response = requests.post('https://api.hostmonit.com/get_optimization_ip', json={"key": "iDetkOys"})
    # if response.status_code == 200:
    #     # 解析响应内容为JSON
    #     response_json = response.json()
        
    #     # 提取info列表
    #     info_list = response_json.get('info', [])
        
    #     # 提取所有IP地址并打印
    #     ip_list = [item['ip'] for item in info_list if 'ip' in item]
    #     for ip in ip_list:
    #         file.write(ip + '\n')
    # else:
    #     print("Error:", response.status_code)
print('IP地址已保存到ip.txt文件中。')
