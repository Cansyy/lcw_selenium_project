from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Locatorlari listele
main_category_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__bottom > nav > ul > li:nth-child(2)")
category_link_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__bottom > nav > ul > li.menu-header-item.menu-header-item--active > div > div.flex-row > div.flex-col.flex-col--zone-items > ul > li:nth-child(3) > a")
product_link_locator = (By.CSS_SELECTOR, "#root > div > div.product-list-container > div.product-list > div:nth-child(5) > div > div.product-grid > div:nth-child(2) > a > div.product-card__product-info > h5.product-card__brand-title")
size_link_locator = (By.CSS_SELECTOR, "#option-size > a")
add_to_basket_button_link_locator = (By.CSS_SELECTOR, "#pd_add_to_cart")
show_basket_link_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__middle > div.header__middle__right > div > div:nth-child(3)")
badge_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__middle > div.header__middle__right > div > div:nth-child(3) > a > span.badge-circle")
go_to_basket_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__middle > div.header__middle__right > div > div:nth-child(3) > div:nth-child(2) > div > div.cart-action > a")
shopping_cart_item_locator = (By.CSS_SELECTOR, "#ShoppingCartContent > div:nth-child(5) > div.col-md-8 > div.products-area > div.seller-products-area > div:nth-child(2)")
homepage_link_locator = (By.CSS_SELECTOR, "#header__container > header > div.header__middle > div.header__middle__left > a")


# Chrome WebDriver baslat
driver = webdriver.Chrome()

# LC Waikiki Anasayfasini Ac
driver.get("https://www.lcwaikiki.com/tr-TR/TR")
title = WebDriverWait(driver, 10).until(EC.title_contains("LC Waikiki"))

# ERKEK kategorisinin uzerine gel ve Hover menuyu ac.
main_category_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(main_category_locator))

action_chain = ActionChains(driver)
action_chain.move_to_element(main_category_link).perform()

# Polo Yaka Tisort alt kategorisini sec.
category_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(category_link_locator))
driver.execute_script("arguments[0].click()", category_link)  # eventi tetiklemek edebilmek icin
assert "Erkek Polo Yaka Tişört" in driver.title

# 2. siradaki urun sec.
product_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(product_link_locator))
driver.execute_script("arguments[0].click()", product_link)
assert "Polo Yaka" in driver.title

# Beden secimi yap.
size_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(size_link_locator))

# Tum bedenler arasindan stok miktari 0dan buyuk olan ilk secenegi sec.
for size_link in size_links:
    data_stock = size_link.get_attribute("data-stock")
    if int(data_stock) > 0:
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(size_link))
        driver.execute_script("arguments[0].click()", link)
        assert "selected" in link.get_attribute("class")
        break

# Secilen bedeni sepete ekle.
add_to_basket_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(add_to_basket_button_link_locator))
driver.execute_script("arguments[0].click()", add_to_basket_link)

# Sepet butonuna tikla.
show_basket_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(show_basket_link_locator))
action_chain.move_to_element(show_basket_link).perform()

# Sepet popup penceresini ve urunun sepete eklendigini kontrol et.
badge = WebDriverWait(driver, 10).until(EC.presence_of_element_located(badge_locator))
assert "1" in badge.text

# Sepete git
go_to_basket_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(go_to_basket_locator))
go_to_basket_link.click()
title = WebDriverWait(driver, 10).until(EC.title_contains("Sepetim"))

# Sepet sayfasinda eklenmis urunu kontrol et.
shopping_cart_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(shopping_cart_item_locator))
assert len(shopping_cart_items) == 1

# Anasayfaya geri don.
homepage_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(homepage_link_locator))
homepage_link.click()
assert "LC Waikiki" in driver.title

driver.quit()
