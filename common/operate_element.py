# -*- coding: utf-8 -*-
"""
该文件是操作元素的一系列方法封装
todo:进webview
"""
import sys
import os
from logger import logger
from time_base import get_current_time
from appium.webdriver.common.touch_action import TouchAction

reload(sys)
sys.setdefaultencoding('utf-8')

get_file = os.path
path = get_file.dirname(get_file.realpath(__file__))
yaml = get_file.join(path, "../report/screenshot/")


def handle_permission_popup(driver):
    """
    该方法用于处理系统弹窗遮挡，默认点击"同意"
    :param driver: 初始化设备信息 self.driver
    """
    try:
        logger.info('正在尝试关闭系统权限申请弹窗......')
        while True:
            # if "不允许" in driver.page_source or "Don't Allow" in driver.page_source:
            driver.switch_to.alert.accept()
            break
        logger.info('已关闭系统权限申请弹窗！')

    except Exception as error:
        logger.info("handle permission popup exception: %s", error)
        return


def scroll_screen(driver):
    """
    todo:该方法用于滑屏操作
    :param driver: 初始化设备信息 self.driver
    """
    # :param duration: 滑动持续时长
    # :param number: 滚动的次数 默认滑动 次
    try:
        logger.info('开始滑动屏幕......')
        TouchAction(driver).press(x=1, y=395).move_to(x=5, y=419).release().perform()
        # for i in range(number):
        #     driver.execute_script("mobile: scroll", {"direction": direction})
        # size = driver.get_window_size()
        # logger.debug('设备尺寸：%s', size)
        # x1 = int(size['width'] * 0.75)
        # y1 = int(size['height'] * 0.5)
        # x2 = int(size['width'] * 0.25)
        # for i in range(number):
        #     driver.swipe(x1, y1, x2, y1, duration)
        #     logger.info('已滑动屏幕：%s次', i + 1)

    except Exception as error:
        logger.error("scroll screen exception: %s", error)
        return


def operate_element(driver, platform, **kwargs):
    """
    该方法封装了：识别元素、点击元素、发送字符 操作方法
    :param driver: 初始化设备信息 self.driver
    :param platform: 被测设备系统 android | ios 用以存放到不同的报告目录下
    :param kwargs:
    kwargs['position']:element position
    kwargs['find_type']:find_type id or xpath
    kwargs['operate_type']:click
    kwargs['operate_message']:operational information
    kwargs['input_character']:input character
    :return:
    """
    for key in kwargs:
        new_dic = kwargs[key]

        try:
            if new_dic is not None:
                logger.info('获取元素信息：%s', new_dic)
                logger.debug('开始执行操作:%s', new_dic['operate_message'])
                # 隐式等待，使用隐式等待执行测试的时候，如果WebDriver没有在DOM中找到元素，将继续等待，超出设定时间后将抛出找不到元素的异常
                driver.implicitly_wait(5)  # 设置5秒时间等待

                if 'xpath' in new_dic['find_type']:
                    element = driver.find_element_by_xpath(new_dic['position'])
                else:
                    element = driver.find_element_by_id(new_dic['position'])

                if 'click' in new_dic['operate_type']:
                    element.click()
                    logger.debug('点击了元素：%s', new_dic['position'])

                if new_dic['input_character'] != "":
                    element.send_keys(new_dic['input_character'])
                    logger.debug('输入了字符：%s', new_dic['input_character'])
                logger.debug('执行%s操作完毕', new_dic['operate_message'])

        except Exception as error:
            logger.error("operation exception %s", error)
            driver.get_screenshot_as_file(yaml + platform + '/error_' + get_current_time() + '.png')

    return


if __name__ == '__main__':
    print yaml