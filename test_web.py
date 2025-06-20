from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
import unittest
import time
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import os

class TestUserWeb(unittest.TestCase):
    def handle_alert(self, accept=True):
        """处理浏览器的警告框、确认框和提示框"""
        try:
            alert = self.driver.switch_to.alert
            if accept:
                alert.accept()
            else:
                alert.dismiss()
        except Exception as e:
            print("没有找到弹出框:", str(e))
    
    @classmethod
    def setUpClass(cls):
        # 手动指定 Edge 驱动程序路径
        edge_driver_path = "D:/mycode/codetest/flask-test/edgedriver_win64/msedgedriver.exe"
        if not os.path.exists(edge_driver_path):
            raise FileNotFoundError(f"Edge WebDriver 未找到，请确保路径正确: {edge_driver_path}")
        
        # 配置 Edge 选项
        options = Options()
        options.add_argument('--disable-dev-shm-usage')  # fix:DevToolsActivePort file doesn't exist
        options.add_argument("--headless")  # 使用新版headless模式
        options.add_argument("--no-sandbox")  # 必须禁用沙箱
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")  # 使用随机端口
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-browser-side-navigation")
        # 初始化浏览器
        cls.driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=options)
        cls.driver.get('http://127.0.0.1:5000')
        cls.wait = WebDriverWait(cls.driver, 10)  # 设置最大等待时间为10秒

    def refresh_and_wait(self, wait_seconds=2):
        """刷新页面并等待加载完成"""
        self.driver.refresh()
        time.sleep(wait_seconds)  # 基础等待时间
        try:
            # 等待表格元素加载完成
            self.wait.until(
                EC.presence_of_element_located((By.ID, "userTable"))
            )
            print("页面刷新成功，表格已加载")
        except Exception as e:
            print("等待表格加载超时:", str(e))
            self.driver.save_screenshot("refresh_error.png")
            raise e

    def test_01_add_user(self):
        # 测试添加用户
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        age_input = self.driver.find_element(By.ID, "age")
        add_button = self.driver.find_element(By.ID, "addBtn")

        name_input.send_keys("张三")
        age_input.send_keys("20")
        add_button.click()

        # 等待用户出现在表格中
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '张三')]")))
        
        # 验证用户是否添加成功
        users_table = self.driver.find_element(By.ID, "userTable")
        self.assertIn("张三", users_table.text)
        self.assertIn("20", users_table.text)

        # 验证用户是否添加成功后刷新页面
        self.refresh_and_wait()

    def test_02_edit_user(self):
        self.refresh_and_wait()  # 开始编辑前刷新页面
        try:
            # 找到编辑按钮并点击
            edit_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '张三')]/following-sibling::td//button[contains(text(), '编辑')]"))
            )
            edit_button.click()
            time.sleep(2)

            # 修改用户信息
            name_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'editName')]"))
            )
            age_input = self.driver.find_element(By.XPATH, "//input[contains(@id, 'editAge')]")
            
            name_input.clear()
            name_input.send_keys("李四")
            age_input.clear()
            age_input.send_keys("22")
            
            # 点击保存
            save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '保存')]")
            save_button.click()
            time.sleep(2)
            
            # 刷新页面并验证修改是否成功
            self.refresh_and_wait()
            users_table = self.driver.find_element(By.ID, "userTable")
            self.assertIn("李四", users_table.text)
            self.assertIn("22", users_table.text)
        except Exception as e:
            self.driver.save_screenshot("edit_error.png")
            raise e

    def test_03_delete_user(self):
        print("开始执行删除用户测试...")
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                self.refresh_and_wait(3)
                print(f"尝试第 {retry_count + 1} 次删除")
                
                # 首先验证用户是否存在
                user_row = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//tr[.//td[contains(text(), '李四')]]"))
                )
                print(f"找到用户行: {user_row.text}")

                # 找到删除按钮
                delete_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//tr[.//td[contains(text(), '李四')]]//button[contains(text(), '删除')]"))
                )
                print("找到可点击的删除按钮")
                
                # 注入 JavaScript 来处理确认对话框
                self.driver.execute_script("window.confirm = () => true")
                print("已设置自动确认删除")
                
                # 点击删除按钮
                delete_button.click()
                print("点击删除按钮")
                
                # 等待删除操作完成
                time.sleep(2)
                
                # 刷新页面并等待表格重新加载
                self.refresh_and_wait(3)
                
                # 验证用户是否已被删除
                def check_user_deleted():
                    try:
                        users_table = self.driver.find_element(By.ID, "userTable")
                        return "李四" not in users_table.text
                    except:
                        return False
                
                # 等待确认用户已被删除
                if self.wait.until(lambda x: check_user_deleted()):
                    print("删除用户测试完成")
                    return
                else:
                    raise Exception("用户未被成功删除")
                
            except Exception as e:
                last_error = e
                print(f"第 {retry_count + 1} 次尝试失败: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    print("等待后重试...")
                    time.sleep(2)
                else:
                    print("达到最大重试次数")
                    self.driver.save_screenshot(f"delete_error_{retry_count}.png")
                    raise Exception(f"删除用户失败，已重试 {retry_count} 次。最后的错误: {str(last_error)}")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
