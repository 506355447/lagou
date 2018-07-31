from selenium.webdriver.chrome.options import Options

#无界面Chrome配置
chrome_options = Options()
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--headless')#浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('--disable-gpu')#谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

#搜索内容
KEYWORD='美食'

#mongodb数据库
MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_TABLE='taobao_meishi'
