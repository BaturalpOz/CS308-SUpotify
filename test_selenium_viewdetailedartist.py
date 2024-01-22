import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class ViewArtistDetailsTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # ChromeDriver yolu güncellenmeli
        self.driver.get('http://localhost:8000/view_detailed_artist.html')  # HTML dosya yolu güncellenmeli

    def test_page_load(self):
        # Sayfanın başarıyla yüklendiğini kontrol et
        self.assertIn("View Artist Details", self.driver.title)

    def test_elements_exist(self):
        # Öğelerin varlığını kontrol et
        subscribe_button = self.driver.find_element(By.ID, "subscribeButton")
        unsubscribe_button = self.driver.find_element(By.ID, "unsubscribeButton")

        self.assertIsNotNone(subscribe_button)
        self.assertIsNotNone(unsubscribe_button)

    def test_subscribe_button_click(self):
        # subscribeButton'a tıkla ve sonucu kontrol et
        subscribe_button = self.driver.find_element(By.ID, "subscribeButton")
        subscribe_button.click()
        # Burada sonuçları kontrol etmek için ek adımlar gerekebilir

    def test_unsubscribe_button_click(self):
        # unsubscribeButton'a tıkla ve sonucu kontrol et
        unsubscribe_button = self.driver.find_element(By.ID, "unsubscribeButton")
        unsubscribe_button.click()
        # Burada sonuçları kontrol etmek için ek adımlar gerekebilir


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
