import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(
    page_title="Goddamn Video",  # 这里设置你想要的标题名称
    page_icon=":smile:",
    layout="centered",
    initial_sidebar_state="auto",
)

header = 'https://www.tv121.com/'
header1 = 'https://www.tv121.com/static/js/player.html?url='

# 初始化 session_state
if 'seach' not in st.session_state:
    st.session_state.seach = False

with st.sidebar:
    st.title("Goddamn Video")
    st.write("<看视频，用超简洁的Goddamn Video>")
    videoName = st.text_input("输入影视名称", key='search')
    col1, col2 = st.columns(2)
    with col1:
        on = st.toggle("无图模式")

    with col2:
        if st.button("搜索"):
            st.session_state.seach = True

    st.write("---")
    st.write('如有侵权，可联系邮件\n\n< gytc163@163.com >')

st.write("---")
st.write("温馨提示：\n\n请勿相信视频内的广告，小心骗得你裤衩子都没得")
st.write("---")

if st.session_state.seach and on:

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

if on:
    print("搜索内容："+videoName+'（无图模式）')
else:
    print("搜索内容：" + videoName)
