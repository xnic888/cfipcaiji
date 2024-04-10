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
def get_cf_ip_top20_json():
    # 发送 HTTP 请求
    response = requests.get("https://vps789.com/vps/sum/cfIpTop20")

    # 检查响应状态码
    if response.status_code == 200:
        # 返回 JSON 数据
        return response.json()
    else:
        # 返回 None 表示请求失败
        return None

def parse_cf_ip_top20():
    # 获取优选IP
    data = get_cf_ip_top20_json()

    # 提取服务器信息
    servers = data["data"]["good"]

    # 选丢包率小于1的IP
    ip_addresses = []
    for server in servers:
        if server["avgLatency"] < 500:
            ip_addresses.append(server["ip"].strip().split()[0]+"#"+server["hostProvider"])

    return ip_addresses
def addVps789Ip(file):
    ip_addresses = parse_cf_ip_top20()
    print(ip_addresses)
    for ip in ip_addresses:
        file.write(ip + '\n')
def addHostmonitIp(file):
    response = requests.post('https://api.hostmonit.com/get_optimization_ip', json={"key": "iDetkOys"})
    if response.status_code == 200:
        # 解析响应内容为JSON
        response_json = response.json()
        
        # 提取info列表
        info_list = response_json.get('info', [])
        
        # 提取所有IP地址并打印
        ip_list = [item['ip'] for item in info_list if 'ip' in item]
        for ip in ip_list:
            file.write(ip + '\n')
    else:
        print("Error:", response.status_code)


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
    try:
        addHostmonitIp(file)
    except:
        print("addHostmonitIp Error")
    try:
        addVps789Ip(file)
    except:
        print("addVps789Ip Error")
    
print('IP地址已保存到ip.txt文件中。')
