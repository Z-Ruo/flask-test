# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
 
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-web-security')

# 使用禁用 SSL 验证的选项
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)
