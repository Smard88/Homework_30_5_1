# from typing import List
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Edge()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


# Проверка карточек всех питомцев.
def test_show_all_pets(driver):
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    images = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    names = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(1)')
    ages = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(3)')

    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        assert image_source != ''
        assert name_text != ''
        assert ages[i].text != ''


# 30.3.1.1
def test_show_all_pets_full(driver):
    # Проверяем что на странице со списком моих питомцев присутствуют все питомцы
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/my_pets']")))
    # Открываем страницу /my_pets.
    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    data_my_pets = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # Ищем на странице /my_pets всю статистику пользователя,
    # и вычленяем из полученных данных количество питомцев пользователя:
    all_statistics = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

    # Проверяем, что количество строк в таблице с моими питомцами равно общему количеству питомцев,
    # указанному в статистике пользователя:
    assert len(data_my_pets) == all_my_pets


# 30.3.1.2
def test_all_my_pets_photos(driver):
    # Поверяем что на странице со списком моих питомцев хотя бы у половины питомцев есть фото.
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

# driver.find_element(By.CSS_SELECTOR, "span.navbar-toggler-icon").click()
    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))

    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # Находим питомцев у которых есть фото
    image_count = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image/")]')
    # Проверяем что фотографии имеются более чем у половины питомцев
    assert len(image_count) >= len(pets_count) / 2


# 30.3.1.3
def test_all_age_name_breed_pets(driver):
    # Поверяем что на странице со списком моих питомцев, у всех питомцев есть имя, возраст и порода
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))

    names = driver.find_elements(By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr/td[1]')
    breeds = driver.find_elements(By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr/td[2]')
    ages = driver.find_elements(By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr/td[3]')
#    print(len(breeds))
#    print(len(names))
    for i in range(len(names)):
        assert names[i] != ''
        assert breeds[i] != ''
        assert ages[i] != ''


# 30.3.1.4
def test_all_Unical_name_pets(driver):
    # Проверяем что на странице со списком питомцев, у всех питомцев разные имена
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr/td[1]')))

    names = driver.find_elements(By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr/td[1]')

    # Находим все строки в таблице
    all_rows = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr')
    pet_names = []

    for row in all_rows:
        name_element = row.find_element(By.TAG_NAME, 'td')
        pet_names.append(name_element.text)
        unique_names = set(pet_names)
        assert len(unique_names) == len(pet_names), "Имеются дубликаты имен "


# 30.3.1.5
def test_no_duplicate_pets(driver):
    # Проверяем что на странице со списком моих питомцев нет повторяющихся питомцев

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('smardQA@postman.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную pet_data элементы с данными о питомцах
    pet_data = driver.find_elements(By.XPATH, '//table[contains(@class,"table table-hover")]/tbody[1]/tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склеенные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0





