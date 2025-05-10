import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def detail(url):
    # 配置无头模式
    edge_options = Options()
    edge_options.add_argument("--headless")  # 新版Edge推荐使用--headless=new
    #edge_options.add_argument("--disable-gpu")  # 在无头模式下禁用GPU加速

    # 创建Edge浏览器驱动
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(10)

    # 使用示例
    driver.get(url)

    try:
        imgs=driver.find_elements(by=By.CSS_SELECTOR,value='div.main_img>div>img')
        for img in imgs:
            img_url=img.get_attribute('data-src')
            img_src=img.get_attribute('src')
            try:
                st.image(img_url)
            except:
                st.image(img_src)

    except:
        st.write('Error')

    driver.quit()

def manhua(name):

    if name == '斗破苍穹':
        response = requests.get('http://m.rumanhua1.com/DjRyvRf/')
    elif name == '逆天邪神':
        response = requests.get('http://m.rumanhua1.com/CmLIVCY/')
    else:
        response = requests.get('http://m.rumanhua1.com/DjRyvRf/')

    soup = BeautifulSoup(response.text, 'lxml')

    url_list = []
    all_a = soup.select('ul>li>a')
    for url in all_a[:20]:
        url_list.append('http://m.rumanhua1.com/'+url.get('href'))
    url_list.reverse()

    return url_list


header = 'https://www.tv121.com/'
header1 = 'https://www.tv121.com/static/js/player.html?url='

if 'search' not in st.session_state:
    st.session_state.search = False

with st.sidebar:
    select_type=st.selectbox("你想看什么", ["视频", "漫画"])
    st.write('---')
    if select_type == '漫画':
        st.title("常看漫画")
        select_option=st.radio("", ["斗破苍穹", "逆天邪神", "选项3"],index=0)
        st.write('---')
        st.write('后',20,'话(0是第20话，即最后一话)')
        num_input = st.text_input('请输入：')
        if st.button('GET'):
            st.session_state.search = True

    elif select_type == '视频':
        st.title("Goddamn Video")
        videoName = st.text_input("输入影视名称", key='search_name')
        col1, col2 = st.columns(2)
        with col1:
            on = st.toggle("无图模式")

        with col2:
            if st.button("搜索", key='search_button'):
                st.session_state.seach = True
        st.write("---")
        st.write('如有侵权，可联系邮件\n\n< gytc163@163.com >')


if select_type == '漫画':
    if select_option == "斗破苍穹":
        if num_input != '':
            if num_input.isdigit():
                if int(num_input) <= 20:
                    if st.session_state.search:
                        detail(manhua(select_option)[int(num_input)-1])
                else:
                    st.write('艾玛！后20话！只有20话！！！')
            else:
                st.write('输入非负整数，就是0，1，2，3，4……')
        else:
            st.write('这是一个广告位，但没广告^_^')

    elif select_option == "逆天邪神":
        if num_input != '':
            if num_input.isdigit():
                if int(num_input) <= 20:
                    if st.session_state.search:
                        detail(manhua(select_option)[int(num_input)-1])
                else:
                    st.write('艾玛！后20话！只有20话！！！')
            else:
                st.write('输入非负整数，就是0，1，2，3，4……')
        else:
            st.write('这是一个广告位，但没广告^_^')
    else:
        st.write('待定……')


elif select_type == '视频':
    if videoName == '':
        st.write("---")
        st.write("温馨提示：\n\n请勿相信视频内的广告，小心骗得你裤衩子都没得")
        st.write("---")

    elif st.session_state.seach and on:

        response = requests.get(f"https://www.tv121.com/sow/{videoName}----------1---.html")

        soup = BeautifulSoup(response.text, "lxml")

        results = soup.select('div.thumb>a')

        num = 1
        for url in results:
            name = url.get('title')
            url = header + url.get('href')
            st.markdown(name)

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            li_urls = soup.select('#con_playlist_1>li>a')

            li_list = []
            for li_url in li_urls:
                li_list.append(header + li_url.get('href'))

            st.write(f"共{len(li_list)}集")

            if len(li_list) != 1:
                input_num = st.text_input('选集：', key=f'key{num}')
            else:
                input_num = '1'

            if st.button('获取', key=f'input_key{num}'):
                if input_num.isdigit():

                    if int(input_num) > len(li_list):
                        st.write(f'一共才{len(li_list)}集，你搞什么！！！')
                    elif int(input_num) <= 0:
                        st.write('输入正整数，就是1，2，3，4……')
                    else:
                        input_url = li_list[int(input_num) - 1]

                        response = requests.get(input_url)
                        soup = BeautifulSoup(response.text, 'lxml')

                        aa = re.search(r'\+"https:(.+?).m3u8', response.text).group(0).replace('+"', '')

                        play_url = header1 + aa
                        iframe_html = f"""
                        <iframe src="{play_url}" width="300" height="150" frameborder="0" allowfullscreen></iframe>
                        """

                        st.markdown(iframe_html, unsafe_allow_html=True)
                else:
                    st.write('输入正整数，就是1，2，3，4……')
                break

            st.write('---')

            num += 1

    else:
        if st.session_state.seach:
            response = requests.get(f"https://www.tv121.com/sow/{videoName}----------1---.html")

            soup = BeautifulSoup(response.text, "lxml")

            results = soup.select('div.thumb>a')

            num = 1
            for url in results:
                col1, col2 = st.columns(2)
                with col1:
                    col3, col4 = st.columns(2)
                    with col3:
                        try:
                            st.image(url.get('data-original'))
                        except:
                            st.image('./nvwa.jpg')
                            st.write('图像出问题了，只能拿来充数了')
                with col2:
                    name = url.get('title')
                    url = header + url.get('href')
                    st.markdown(name)

                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'lxml')
                    li_urls = soup.select('#con_playlist_1>li>a')

                    li_list = []
                    for li_url in li_urls:
                        li_list.append(header + li_url.get('href'))

                    st.write(f"共{len(li_list)}集")
                    if len(li_list) != 1:
                        input_num = st.text_input('选集：', key=f'key{num}')
                    else:
                        input_num = '1'

                    if st.button('获取', key=f'input_key{num}'):
                        if input_num.isdigit():

                            if int(input_num) > len(li_list):
                                st.write(f'一共才{len(li_list)}集，你搞什么！！！')
                            elif int(input_num) <= 0:
                                st.write('输入正整数，就是1，2，3，4……')
                            else:
                                input_url = li_list[int(input_num) - 1]

                                response = requests.get(input_url)
                                soup = BeautifulSoup(response.text, 'lxml')

                                aa = re.search(r'\+"https:(.+?).m3u8', response.text).group(0).replace('+"', '')

                                play_url = header1 + aa
                                iframe_html = f"""
                                    <iframe src="{play_url}" width="300" height="150" frameborder="0" allowfullscreen></iframe>
                                    """

                                st.markdown(iframe_html, unsafe_allow_html=True)
                        else:
                            st.write('输入正整数，就是1，2，3，4……')

                st.write('---')

                num += 1

    # if on:
    #     print("搜索内容：" + videoName + '（无图模式）')
    # else:
    #     print("搜索内容：" + videoName)








