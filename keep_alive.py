
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time


def keep_streamlit_alive():
    # 设置无头浏览器
    options = Options()
    # options.add_argument("--headless")  # 无头模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 初始化 Chrome 浏览器（GitHub Actions 默认支持 Chrome）
    driver = webdriver.Edge(options=options)

    try:
        # 访问你的 Streamlit 应用
        streamlit_url = "https://goddamnvideo.streamlit.app/"
        driver.get(streamlit_url)

        # 搜索操作
        # driver.find_element(by=By.CSS_SELECTOR,value="#text_input_1").send_keys('神探夏洛克')
        # driver.find_element(by=By.CSS_SELECTOR,value="[kind='secondary']").click()

        # 模拟用户操作（可选）
        print("访问成功:", driver.title)
        time.sleep(10)  # 停留10秒，模拟真实用户

    except Exception as e:
        print("访问失败:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    keep_streamlit_alive()
