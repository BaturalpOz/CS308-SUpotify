import unittest
from selenium import webdriver

class SubscribePageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # ChromeDriver yolu güncellenmeli
        self.driver.get('http://localhost:8000/subscribe.html')  # HTML dosya yolu güncellenmeli

    def test_page_load(self):
        # Sayfanın başarıyla yüklendiğini kontrol et
        self.assertIn("Subscribe", self.driver.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()