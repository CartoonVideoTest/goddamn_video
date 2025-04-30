import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

header='https://www.tv121.com/'
header1='https://www.tv121.com/static/js/player.html?url='

# 初始化 session_state
if 'seach' not in st.session_state:
    st.session_state.seach = False

# st.sidebar.write("动漫梦工厂")
st.title("Goddamn Video")
st.write("<看视频，用超简洁的Goddamn Video>")
st.write("<温馨提示：TM的别相信视频内的广告什么的>")
st.write("<小心骗得你裤衩子都不剩>")
videoName=st.text_input("输入影视名称",key='search')

if st.button("搜索"):
    st.session_state.seach = True

st.write("---")

if st.session_state.seach:

    response=requests.get(f"https://www.tv121.com/sow/{videoName}----------1---.html")

    soup=BeautifulSoup(response.text,"lxml")

    results=soup.select('div.thumb>a')

    num = 1
    for url in results:
        col1, col2 = st.columns(2)
        with col1:
            col3, col4 = st.columns(2)
            with col3:
                st.image(url.get('data-original'))
        with col2:
            name = url.get('title')
            url = header + url.get('href')
            st.markdown(name)

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            li_urls = soup.select('#con_playlist_1>li>a')

            li_list = []
            for li_url in li_urls:
                li_list.append(header+li_url.get('href'))

            st.write(f"共{len(li_list)}集")
            if len(li_list)!=1:
                input_num=st.text_input('选集：',key=f'key{num}')
            else:
                input_num=1

            if st.button('获取',key=f'input_key{num}'):
                input_url = li_list[int(input_num) - 1]

                response = requests.get(input_url)
                soup = BeautifulSoup(response.text, 'lxml')

                aa=re.search(r'\+"https://v(.+?).m3u8',response.text).group(0).replace('+"','')

                play_url=header1+aa
                iframe_html =f"""
                <iframe src="{play_url}" width="300" height="150" frameborder="0" allowfullscreen></iframe>
                """

                st.markdown(iframe_html, unsafe_allow_html=True)


        st.write('---')

        num+=1


st.write('如有侵权，可联系邮件\n\n<gytc163@163.com>')
