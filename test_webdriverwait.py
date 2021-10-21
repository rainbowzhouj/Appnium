import time

import pytest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestWebDriverwait:
    def setup(self):
        desired_caps={}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['automationName'] = 'uiautomator2'
        desired_caps['appPackage'] = 'com.larksuite.suite'
        desired_caps['appActivity'] = "com.ss.android.lark.main.app.MainActivity"
        #desired_caps['appActivity'] = "com.ss.android.lark.guide.landing.general.ui.GuidePageActivity"
        # noReset 保留缓存，比如登录状态
        desired_caps['noReset'] = True
        # 不停止应用，直接运行测试用例
        desired_caps['dontStopAppOnReset'] = True
        # 中文输入
        desired_caps['unicodeKeyBoard'] = 'true'
        desired_caps['resetKeyBoard'] = 'true'
        # 跳过设备初始化
        desired_caps['skipDeviceInitialization']=True
        desired_caps['settings[waitForIdleTimeout]']=0
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(5)

    def teardown(self):
        self.driver.quit()

    #@pytest.skip
    def test_login(self):
        """
        1.点击搜索框，进行搜索成员
        2.选择搜索后的其中一个成员
        3.定位第二点contacts
        """
        #self.driver.find_element_by_id("com.larksuite.suite:id/startLoginBtn")
        # 第一次登录
        self.driver.find_element(MobileBy.XPATH,"//*[@text='Log In']").click()

        # 切换语言为简体中文
        self.driver.find_element(By.ID,"com.larksuite.suite:id/tvChangeLanguage").click()
        self.driver.find_element(By.XPATH,"//*[@text='简体中文']").click()
        self.driver.find_element(By.XPATH,"//*[@text='Done']").click()
        self.driver.find_element(By.XPATH, "//*[@text='Switch']").click()

        # 用手机号方式进行登录
        self.driver.find_element(MobileBy.XPATH, "//*[@text='手机号']").click()
        # 输入手机号
        self.driver.find_element(MobileBy.ACCESSIBILITY_ID,"phone number").send_keys("15001731170")
        # 勾选政策
        self.driver.find_element_by_id("com.larksuite.suite:id/checkBoxPolicy").click()
        # 点击下一步
        self.driver.find_element(By.ID,"com.larksuite.suite:id/tvNextStep").click()
        time.sleep(2)

    def test_daka(self):
        """
        1.点击工作台
        2.滑动后，点击打卡
        3.第一次进入时，会弹出授权提示，可以选择允许或禁止   noReset后不用此句
        4.利用显示等待，定位打卡或更新打卡，点击
        5.点击确认更新打卡，利用高级定位方式（xpath与class结合定位外勤打卡）后，点击外勤打卡
        6.断言打卡成功

        """
        self.driver.find_element(MobileBy.XPATH,'//*[@text="工作台"]').click()
        self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("打卡").instance(0));').click()

        #self.driver.find_element(MobileBy.ID,"com.android.permissioncontroller:id/permission_allow_foreground_only_button").click()
        #WebDriverWait(self.driver,10).until(lambda x: x.find_element(MobileBy.XPATH,"//*[contains(@text,'打卡')]"))
        #//*[contains(@text,'下班时间')]/../*[@text='更新打卡']
        time.sleep(10)
        aaa=WebDriverWait(self.driver,10).until(lambda x: x.find_element(MobileBy.XPATH,"//*[contains(@text,'更新打卡')]"))
        aaa.click()

        print("成功")
        #self.driver.find_elements_by_xpath("//*[contains(@text,'更新打卡')]")[0].click()
        #print(self.driver.page_source)
        #self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
        #                         'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("更新打卡").instance(0));').click()

        #/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[2]/android.view.View[1]

        #WebDriverWait(self.driver, 10).until(lambda x: "打卡时间" in x.page_source)
        #WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(MobileBy.XPATH,"//*[@text='更新打卡']"))
        #self.driver.find_element(MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[2]/android.view.View[1]/android.view.View[2]").click()


        self.driver.find_element(MobileBy.ID,"com.larksuite.suite:id/confirm").click()
        # #self.driver.find_element(MobileBy.XPATH,"//*[contains(@text,'外勤打卡')]")  此时碰到一个页面存在同名的元素
        # self.driver.find_element(MobileBy.XPATH,"//*[@text='外勤打卡' and @class='android.view.View']").click()
        # self.driver.find_element(MobileBy.ID, "com.larksuite.suite:id/confirm").click()
        time.sleep(2)
        assert "外勤打卡" in self.driver.page_source
        # 显式等待

        #WebDriverWait(self.driver, 10).until(lambda x: "打卡成功" in x.page_source)



    def test_webwait(self):
        """
        1.点击工作台，进行搜索成员
        2.选择搜索后的其中一个成员
        3.定位第二点contacts
        """
        pass




