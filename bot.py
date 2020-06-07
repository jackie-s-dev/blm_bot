from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
from logger import Logger

# constants that this bot relies on
ADD_COMMENT_XPATH = '//*[@id="labelAndInputContainer"]'
SUBMIT_COMMENT_XPATH = '//*[@id="submit-button"]'

YT_SEARCH = '/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input'
YT_SEARCH_GO = '/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/button'
YT_SEARCH_VID = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]'

################################################################
# DOING THINGS BY CSS!
ADD_COMMENT_CSS = '#contenteditable-root'
SUBMIT_COMMENT_CSS = '#button'
YT_PLAY_CSS = '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button'
YT_TIME_CURR_CSS = '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div > span.ytp-time-current'
YT_TIME_TOTAL_CSS = '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div > span.ytp-time-duration'
YT_VID_SETTINGS_CSS = '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button.ytp-button.ytp-settings-button'
YT_AUTOPLAY_CSS = '#ytp-id-20 > div > div > div:nth-child(1) > div.ytp-menuitem-content > div'
YT_SEARCH_CSS = '#search'
YT_SEARCH_GO_CSS = '#search-icon-legacy > yt-icon'
YT_SEARCH_VID_CSS = '#video-title > yt-formatted-string'
YT_AD_BUTTON_CSS = '#movie_player > div.video-ads.ytp-ad-module'

class Bot():
    def __init__(self, comments, tags, home_url):
        """
        Comments is a list of comment provided by user to add to random
        videos.
        """
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        self.logger = Logger({"Comments: " : comments,
                         "Tags: " : tags,
                         "Home URL" : str(home_url)})
        self.logger.log("=============================")

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.comments = comments
        self.tags = tags
        self.home_url = home_url

    def login(self, username, password):
        """
        Responsible for logging in the user based on a given username and password.
        """
        self.logger.log("Navigating to stackoverflow to sign in...")
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        time.sleep(2)
        self.logger.log("Successfully signed in. Navigating to YouTube.com...")
        self.driver.get('https://youtube.com')

    def check_if_exists_by_css(self, css):
        self.logger.log("Checking to see if the element: " + css + " exists...")
        try:
            self.driver.find_element_by_css_selector(css)
            time.sleep(2)
            self.logger.log("The element: " + css + " exists.")
        except NoSuchElementException:
            self.logger.log("The element: " + css + " does not exist!", failure=True)
            return False
        return True

    def watch_video(self, url=None, comment=False):
        """
        Watching a video in its entirety. Leave a comment?
        """
        if url == None:
            url = self.home_url

        self.driver.get(url)
        self.logger.log("Navigating to the url: " + url + "...")
        time.sleep(2)

        self.find_element(YT_PLAY_CSS).click()
        time.sleep(2)
        self.logger.log("Playing video...")

        try: # turning off autoplay since it complicates things
            self.logger.log("Attempting to turn off autoplay...")
            self.find_element(YT_VID_SETTINGS_CSS).click()
            time.sleep(2)
            self.find_element(YT_AUTOPLAY_CSS).click()
            time.sleep(2)
        except:
            self.logger.log("Detected an ad...")
            video_duration = self.find_element(YT_TIME_TOTAL_CSS).text
            time.sleep(self.time_to_wait(video_duration) + 2)

            self.logger.log("Attempting to turn off autoplay...")
            try:
                self.find_element(YT_VID_SETTINGS_CSS).click()
                time.sleep(2)
                self.find_element(YT_AUTOPLAY_CSS).click()
                time.sleep(2)
            except:
                self.logger.log("Failed to turn of autoplay.", failure=True)

        # adding a comment if indicated
        self.logger.log("Adding comment...")
        if (comment == True):
            try:
                rand_index = random.randint(0, len(self.comments))
                new_comment = self.comments[rand_index - 1]
                self.find_element(ADD_COMMENT_CSS).send_keys(new_comment)
                time.sleep(3)
                self.find_element(SUBMIT_COMMENT_CSS).click()
                time.sleep(3)
            except:
                self.logger.log("Failed to add comment.", failure=True)

        # check if the video is still playing
        self.logger.log("Checking current video duration...")
        video_duration = self.find_element(YT_TIME_TOTAL_CSS).text
        time.sleep(self.time_to_wait(video_duration))

        return True

    def time_to_wait(self, time_string):
        """
        Changes string from duration into seconds to wait.
        """
        self.logger.log("Calculating the time to wait...")
        time_list = [0, 0, 0]

        string_list = time_string.split(':')
        string_list = string_list[::-1]
        for i in range(0, len(string_list)):
            if (string_list[i] != ''):
                time_list[i] = int(string_list[i])

        total_time = time_list[0] + (time_list[1] * 60) + (time_list[2] * 3600)
        self.logger.log("The calculated wait time is: " + str(total_time))
        return total_time

    def find_element(self, link):
        """
        Returning an element by its css selector.
        """
        try:
            return self.driver.find_element_by_css_selector(link)
        except NoSuchElementException:
            return None

    def watch_by_tags(self):
        """
        Watches a video and places a comment to promote.
        """
        rand_index = random.randint(0, len(self.tags))
        random_tag = self.tags[rand_index - 1]
        self.logger.log("Random tag for YouTube search is: " + random_tag)
        self.driver.get('https://youtube.com')
        self.logger.log("Navigating to https://youtube.com...")
        self.driver.find_element_by_xpath(YT_SEARCH).send_keys(random_tag)
        time.sleep(3)
        self.driver.find_element_by_xpath(YT_SEARCH_GO).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(YT_SEARCH_VID).click()
        time.sleep(3)

        tagged_url = self.driver.current_url
        self.logger.log("The searched video URL is: " + tagged_url)
        self.watch_video(url=tagged_url, comment=True)

    def run(self, limit):
        """
        Runs until the specified video limit
        """

        counter = 0
        while(counter < limit):
            counter = counter + 3
            self.logger.log("~~~Watching by tags...")
            self.watch_by_tags()
            self.logger.log("~~~Watching video...")
            self.watch_video()
            self.logger.log("~~~Watching by tags...")
            self.watch_by_tags()

        self.logger.log("BOT WATCHING SESSION COMPLETE.")
        self.logger.log("===Closing===")
        self.logger.stop_close()

bot = Bot(['heelloo', 'hi'], ['turtle', 'people', 'cars', 'bees'], 'https://www.youtube.com/watch?v=5h6oGxHVZW0')
bot.login('chompyjackie@gmail.com', 'B0ssJackie')
bot.run(1)
