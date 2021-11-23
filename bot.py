from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, choice


class PollBot(object):

    def __init__(self):
        binary = FirefoxBinary("/bin/firefox")
        self.browser = webdriver.Firefox(firefox_binary=binary)
        self.browser.get("https://www.1ka.si/a/330025")
        WebDriverWait(self.browser, timeout=3).until(lambda d: d.find_element_by_tag_name("html"))
        self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/form/div[2]/input").click()
        self.choices = []
        self.devices = dict()
        form = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/form")
        self.elems = [div for div in form.find_elements_by_tag_name('div') if div.get_attribute('data-vrstni_red')]
        self.get_poll_elements()
        try:
            self.generate_answers()
            self.browser.close()
        except Exception:
            self.browser.close()

    def generate_answers(self):
        for i, c in enumerate(self.choices):
            el = self.elems[i]

            if not el.is_displayed():
                self.browser.execute_script("arguments[0].scrollIntoView();", el)
                WebDriverWait(self.browser, timeout=5).until(lambda d: d.find_element_by_id(el.get_attribute('id')))

            div = el.find_elements_by_tag_name('div')[1]
            if "tip_7" in el.get_attribute('class'):
                el.find_element_by_xpath("//*[@id='spremenljivka_12877354_vrednost_1']").send_keys(c[0])
            elif "tip_1" in el.get_attribute('class'):

                if i == 4:
                    if self.choices[3][0] == 3:
                        if not div.find_elements_by_tag_name('input')[c[0]].is_displayed():
                            self.browser.execute_script("arguments[0].scrollIntoView();", div)
                        div.find_elements_by_tag_name('input')[c[0]].click()
                else:
                    if not div.find_elements_by_tag_name('input')[c[0]].is_displayed():
                        self.browser.execute_script("arguments[0].scrollIntoView();", div)
                    div.find_elements_by_tag_name('input')[c[0]].click()

            elif "tip_2" in el.get_attribute('class'):

                if i in range(6, 11):
                    if self.choices[5][i - 6]:
                        for j, ch in enumerate(c):
                            if not el.find_elements_by_tag_name('div')[1].find_elements_by_tag_name('input')[j + 1].is_displayed():
                                self.browser.execute_script("arguments[0].scrollIntoView();", div)
                            if ch:
                                self.browser.execute_script("arguments[0].scrollIntoView();", div)
                                el.find_elements_by_tag_name('div')[1].find_elements_by_tag_name('input')[j + 1].click()
                    else:
                        for i in el.find_elements_by_tag_name('input'):
                            if "text" in i.get_attribute('type'):
                                i.click()
                                i.send_keys("nimam")
                else:
                    for j, ch in enumerate(c):
                        if not el.find_elements_by_tag_name('div')[1].find_elements_by_tag_name('input')[j + 1].is_displayed():
                            self.browser.execute_script("arguments[0].scrollIntoView();", div)
                        if ch:
                            self.browser.execute_script("arguments[0].scrollIntoView();", div)
                            el.find_elements_by_tag_name('div')[1].find_elements_by_tag_name('input')[j + 1].click()

            elif "tip_6" in el.get_attribute('class'):
                for j, ch in enumerate(c):
                    self.browser.execute_script("arguments[0].scrollIntoView();", el)
                    els = el.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
                    els[j].find_elements_by_class_name('category')[ch].click()

        self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/form/div[2]/input[2]").click()
        self.browser.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[3]/input[2]").click()

    def get_poll_elements(self):
        age = [randint(10, 20)]
        for i, e in enumerate(self.elems):
            variabla = e.find_elements_by_class_name('variabla   ')
            if e.get_attribute('class'):
                if "tip_7" in e.get_attribute('class') and "tip_21" not in e.get_attribute('class'):
                   self.choices.append(age)
                elif "tip_1" in e.get_attribute('class'):
                    rand = randint(1, 20)
                    if i == 0:
                        self.choices.append(choice([[0], [1]]))
                    elif i == 1:
                        if age[0] >= 15:
                            self.choices.append(choice([[1], [2], [3]]))
                        else:
                            self.choices.append(choice([[0]]))
                    elif i == 3:
                        self.choices.append([3] if rand in range(1, 18) else [choice([[0], [1], [2]])])
                    elif i == 4:
                        self.choices.append([3] if rand in range(1,3) else choice([[0],[1],[2]]))
                    else:
                        self.choices.append([randint(1, len(variabla) - 1)])
                elif "tip_2" in e.get_attribute('class'):
                    if i == 5:
                        self.choices.append([randint(0,1), 1, randint(0,1), 1, randint(0,1), 0, 0])
                    else:
                        self.choices.append([randint(0, 1) for i in range(0, len(variabla) - 1)])
                elif "tip_6" in e.get_attribute('class'):
                    self.choices.append([randint(0, 4) for tr in range(0, len(e.find_element_by_tag_name(
                        'tbody').find_elements_by_tag_name('tr')))])
