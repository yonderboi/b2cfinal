import time
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BY_PHONE = 0
BY_MAIL = 1
BY_LOGIN = 2
BY_LS = 3
BY_VK = 4
BY_OK = 5
BY_MAILRU = 6
BY_GOOGLE = 7
BY_YANDEX = 8
BY_INVALID = 100

FIRSTNAME_CODEPAGE_INVALID = 0
FIRSTNAME_TOO_SHORT = 1
FIRSTNAME_TOO_LONG = 2
EMAIL_INVALID = 3
PASSWORD_INVALID = 4
PASSWORD_DOESNT_MATCH = 5


def generate_password_lowercase():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

def generate_password():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

def generate_login():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


class TestLoginELKWeb:

    def setup(self):
        self.user_phone = "+79202955545"
        self.user_mail = "akostovich@gmail.com"
        self.user_login = "yonderboi_80"
        self.user_ls = "yonderboi_80"
        self.password = "rampas-jeJwin-kidgu8"

        self.name_valid = 'Александр'
        self.name_invalid = 'Tester'
        self.name_short = 'A'
        self.name_long = 'A' * 40
        self.test_mail_valid = "akostovich@gmx.com"
        self.test_mail_invalid = 'akostovich@gmx.com'
        self.test_pwd_valid = generate_password()
        self.test_pwd_invalid = generate_password_lowercase()

    def open(self):
        self.driver = webdriver.Chrome(executable_path=r'C:/chromedriver/chromedriver.exe')
        self.driver.get("https://b2c.passport.rt.ru")

    def close(self):
        self.driver.quit()

    def fill_credentials_and_login(self, locator, login_id):
        self.driver.find_element(By.XPATH, locator).click()
        self.driver.find_element(By.XPATH, "//input[@type='text' and @id='username']").send_keys(login_id)
        self.driver.find_element(By.XPATH, "//input[@type='password' and @id='password']").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@id='kc-login']").click()

    def login(self, credential_id):
        locator_social = "//div[@class='ext-widget_h_tx' and contains(text(), 'Одноклассники')]"
        if credential_id == BY_PHONE:
            locator = "//div[@id='t-btn-tab-phone']"
            login_id = self.user_phone
        elif credential_id == BY_MAIL:
            locator = "//div[@id='t-btn-tab-mail']"
            login_id = self.user_mail
        elif credential_id == BY_LOGIN:
            locator = "//div[@id='t-btn-tab-login']"
            login_id = self.user_login
        elif credential_id == BY_LS:
            login_id = self.user_ls
            locator = "//div[@id='t-btn-tab-ls']"
        elif credential_id == BY_VK:
            locator = "//div[@class='social-providers']/a[@id='oidc_vk']"
            locator_social = "//div[@class='box_msg_gray box_msg_padded']/b[contains(text(), 'ВКонтакте')]"
        elif credential_id == BY_OK:
            locator = "//div[@class='social-providers']/a[@id='oidc_ok']"
            locator_social = "//div[@class='ext-widget_h_tx' and contains(text(), 'Одноклассники')]"
        elif credential_id == BY_MAILRU:
            locator = "//div[@class='social-providers']/a[@id='oidc_mail']"
            locator_social = "//span[@class='header__logo' and contains(text(), 'Мой Мир@Mail.Ru')]"
        elif credential_id == BY_GOOGLE:
            locator = "//div[@class='social-providers']/a[@id='oidc_google']"
            locator_social = "//div[contains(text(), 'Войдите в аккаунт Google')]"
        elif credential_id == BY_YANDEX:
            locator = "//div[@class='social-providers']/a[@id='oidc_ya']"
            locator_social = "//span[@class='passp-add-account-page-title' and contains(text(), 'Яндекс ID')]"
        elif credential_id == BY_INVALID:
            locator = "//div[@id='t-btn-tab-login']"
            login_id = generate_login()

        if credential_id == BY_VK or \
                credential_id == BY_OK or \
                credential_id == BY_MAILRU or \
                credential_id == BY_GOOGLE or \
                credential_id == BY_YANDEX:
            self.driver.find_element(By.XPATH, locator).click()
            assert WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, locator_social)))
            return
        else:
            self.fill_credentials_and_login(locator, login_id)
        if credential_id != BY_INVALID:
            assert WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='user-info home__user-info']/button")))

    def fill_registration_data(self, firstname, lastname, address, password, password_confirm):
        self.driver.find_element(By.XPATH, "//input[@type='text' and @name='firstName']").send_keys(firstname)
        self.driver.find_element(By.XPATH, "//input[@type='text' and @name='lastName']").send_keys(lastname)
        self.driver.find_element(By.XPATH, "//input[@type='text' and @id='address']").send_keys(address)
        self.driver.find_element(By.XPATH, "//input[@type='password' and @id='password']").send_keys(password)
        self.driver.find_element(By.XPATH, "//input[@type='password' and @id='password-confirm']").send_keys(password_confirm)

    def register_valid(self):
        self.fill_registration_data('тест', 'тест', self.test_mail_valid, self.test_pwd_valid, self.test_pwd_valid)
        self.driver.find_element(By.XPATH, "//button[@type='submit' and @name='register']").click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Подтверждение email')]")))

    def register_invalid(self, option):
        if option == FIRSTNAME_CODEPAGE_INVALID:
            self.fill_registration_data(self.name_invalid,
                                        self.name_valid,
                                        self.test_mail_valid,
                                        self.test_pwd_valid,
                                        self.test_pwd_valid)
        elif option == FIRSTNAME_TOO_SHORT:
            self.fill_registration_data(self.name_short,
                                        self.name_valid,
                                        self.test_mail_valid,
                                        self.test_pwd_valid,
                                        self.test_pwd_valid)
        elif option == FIRSTNAME_TOO_LONG:
            self.fill_registration_data(self.name_long,
                                        self.name_valid,
                                        self.test_mail_valid,
                                        self.test_pwd_valid,
                                        self.test_pwd_valid)
        elif option == EMAIL_INVALID:
            self.fill_registration_data(self.name_valid,
                                        self.name_valid,
                                        self.test_mail_invalid,
                                        self.test_pwd_valid,
                                        self.test_pwd_valid)
        elif option == PASSWORD_INVALID:
            self.fill_registration_data(self.name_valid,
                                        self.name_valid,
                                        self.test_mail_valid,
                                        self.test_pwd_invalid,
                                        self.test_pwd_invalid)
        elif option == PASSWORD_DOESNT_MATCH:
            self.fill_registration_data(self.name_valid,
                                        self.name_valid,
                                        self.test_mail_valid,
                                        generate_password(),
                                        generate_password())
        self.driver.find_element(By.XPATH, "//button[@type='submit' and @name='register']").click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Подтверждение email')]")))

    def test_login_by_phone_number_valid(self):
        """Проверяем, что вход в личный кабинет выполняется корректно при вводе валидного номера телефона и пароля"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        self.login(BY_PHONE)
        # time.sleep(2)

    def test_login_by_mail_address_valid(self):
        """Проверяем, что вход в личный кабинет выполняется корректно при вводе валидного адреса почты и пароля"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        self.login(BY_MAIL)
        # time.sleep(2)

    def test_login_by_login_invalid(self):
        """Проверяем, что вход в личный кабинет не выполняется при вводе невалидного логина и пароля"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        self.login(BY_LOGIN)
        # time.sleep(2)

    def test_login_by_ls_invalid(self):
        """Проверяем, что вход в личный кабинет не выполняется при вводе невалидного лицевого счета и пароля"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        self.login(BY_LS)
        # time.sleep(2)

    def test_login_by_vk_valid(self):
        """Проверяем, что выполняется переход на аутентификацию через ВК"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='social-providers']")))
        self.login(BY_VK)
        # time.sleep(2)

    def test_login_by_ok_valid(self):
        """Проверяем, что выполняется переход на аутентификацию через ОК"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='social-providers']")))
        self.login(BY_OK)
        # time.sleep(2)

    def test_login_by_mailru_valid(self):
        """Проверяем, что выполняется переход на аутентификацию через MAIL.RU"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='social-providers']")))
        self.login(BY_MAILRU)
        # time.sleep(2)

    def test_login_by_google_valid(self):
        """Проверяем, что выполняется переход на аутентификацию через GOOGLE.COM"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='social-providers']")))
        self.login(BY_GOOGLE)
        # time.sleep(2)

    def test_login_by_yandex_valid(self):
        """Проверяем, что выполняется переход на аутентификацию через YANDEX.RU"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='social-providers']")))
        self.login(BY_YANDEX)
        # time.sleep(2)

    def test_password_recovery_valid(self):
        """Проверяем, что при нажатии на кнопку 'Забыл пароль' переходим на форму восстановления пароля"""
        self.open()
        WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                         (By.XPATH, "//a[contains(@class, 'login-form__forgot-pwd--muted')]"))).click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Восстановление пароля')]")))
        # time.sleep(2)

    def test_password_recovery_return_valid(self):
        """Проверяем, что при нажатии на кнопку 'Забыл пароль' переходим на форму восстановления пароля и можем
        перейти обратно на форму авторизации"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class, 'login-form__forgot-pwd--muted')]"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Восстановление пароля')]")))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@name='back_to_login']"))).click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        # time.sleep(2)

    def test_forgot_password_button(self):
        """Проверяем, что кнопка 'Забыл пароль' подсвечивается при вводе неправильных логина-пароля"""
        self.open()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='login-form__remember-forgot-con']")))
        self.login(BY_INVALID)
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class, 'login-form__forgot-pwd--animated')]")))
        # time.sleep(2)

    def test_registration_opened_valid(self):
        """Проверяем, что при нажатии на кнопку 'Зарегистрироваться' переходим на форму регистрации"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        # time.sleep(2)

    def test_user_registration_valid(self):
        """Проверяем, что форма регистрации принимает валидные данные пользователя
        и переходит на форму проверки кода подтверждения"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_valid()
        # time.sleep(2)

    def test_user_registration_codepage_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если Имя не кириллица"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(FIRSTNAME_CODEPAGE_INVALID)
        # time.sleep(2)
    #
    def test_user_registration_name_short_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если Имя слишком короткое"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(FIRSTNAME_TOO_SHORT)
        # time.sleep(2)

    def test_user_registration_name_long_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если Имя слишком длинное"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(FIRSTNAME_TOO_LONG)
        # time.sleep(2)

    def test_user_registration_email_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если почта в неверном формате"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(EMAIL_INVALID)
        # time.sleep(2)

    def test_user_registration_password_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если пароль в неверном формате"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(PASSWORD_INVALID)
        # time.sleep(2)

    def test_user_registration_password_match_invalid(self):
        """Проверяем, что форма регистрации не принимает не валидные данные пользователя
        и не переходит на форму проверки кода подтверждения, если пароли не совпадают"""
        self.open()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='login-form__register-con']/a"))).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card-container__wrapper']/h1[contains(text(), 'Регистрация')]")))
        self.register_invalid(PASSWORD_DOESNT_MATCH)
        # time.sleep(2)

    def teardown(self):
        self.close()
