# PreInstalled PyPackages
import asyncio
import logging
import os
import random
import re
import time

# Pip Install Packages
import numpy as np
import scipy.interpolate
import playwright_stealth
import requests
from playwright.async_api import async_playwright
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# Imports from Files
from hcaptcha_challenger import (DIR_CHALLENGE, DIR_MODEL, PATH_OBJECTS_YAML,
                                 ArmorCaptcha)


class Faker():
    def __init__(self):
        return

    class Person():
        def __init__(selff, gender="random"):
            url = f"https://api.namefake.com/english-united-states/{gender}"
            r = requests.get(url)
            data = r.json()
            selff.name = data.get("name")
            selff.maiden_name = data.get("maiden_name")
            selff.birth_date = data.get("birth_data")
            selff.birth_year = selff.birth_date.split("-")[0]
            # selff.birth_month = selff.birth_date.split("-")[1]
            # selff.birth_day = selff.birth_date.split("-")[2]
            selff.birth_month = str(random.randint(1, 12))
            selff.birth_day = str(random.randint(1, 12))
            selff.email_name = data.get("email_u")
            selff.email_domain = data.get("email_d")
            selff.email = f"{selff.email_name}@{selff.email_domain}"
            selff.username = data.get("username")
            selff.password = data.get("password")
            selff.domain = data.get("domain")
            selff.company = data.get("company")
            selff.height = data.get("height")
            selff.weight = data.get("weight")
            selff.eye = data.get("eye")
            selff.hair = data.get("hair")
            selff.sport = data.get("sport")

        def __str__(selff):
            return str(selff.__dict__)

    class Geolocation():
        def __init__(selff, country=""):
            url = f"https://api.3geonames.org/randomland.{country}.json"
            r = requests.get(url)
            data = r.json()["nearest"]
            selff.latitude = data.get("latt")
            selff.longitude = data.get("longt")
            selff.city = data.get("city")
            selff.country = data.get("prov")
            selff.state = data.get("state")
            selff.region = data.get("region")
            selff.elevation = data.get("elevation")
            selff.timezone = data.get("timezone")

        def __str__(selff):
            return str(selff.__dict__)

    class Computer():
        def __init__(selff):
            try:
                # Sometimes the API is offline
                while True:
                    url = "http://fingerprints.bablosoft.com/preview?rand=0.1&tags=Firefox,Desktop,Microsoft%20Windows"
                    r = requests.get(url)
                    data = r.json()
                    selff.useragent = data.get("ua")
                    selff.vendor = data.get("vendor")
                    selff.renderer = data.get("renderer")
                    selff.width = data.get("width")
                    selff.height = data.get("height")
                    selff.avail_width = data.get("availWidth")
                    selff.avail_height = data.get("availHeight")
                    # If the Window is too small for the captcha
                    if selff.height > 810 and selff.avail_height > 810:
                        return
            except Exception as e:
                # If Bablosoft Website is offline
                software_names = [SoftwareName.FIREFOX.value]
                operating_systems = [OperatingSystem.WINDOWS.value]
                user_agent_rotator = UserAgent(
                    software_names=software_names, operating_systems=operating_systems, limit=1)
                selff.useragent = user_agent_rotator.get_random_user_agent()
                selff.vendor = "Google Inc."
                selff.renderer = "Google Inc. (AMD)"
                selff.width = 1280
                selff.height = 720
                selff.avail_width = 1280
                selff.avail_height = 720

        def __str__(selff):
            return str(selff.__dict__)

    # Shit Method To Get Locale of Country code
    class Locale():
        def __init__(selff, country_code="US"):
            url = f"http://restcountries.com/v3.1/alpha/{country_code}"
            r = requests.get(url)
            data = r.json()[0]
            selff.languages = data.get("languages")
            selff.language_code = list(selff.languages.keys())[0][:2]
            selff.locale = f"{selff.language_code.lower()}-{country_code.upper()}"

        def __str__(selff):
            return str(selff.__dict__)


class Proxy():
    def __init__(self):
        return

    def Split(self, proxy):
        if "@" in proxy:
            first, second = proxy.split("@")
            _1, _2 = first.split(":")
            _3, _4 = second.split(":")
            return [_3, _4, _1, _2]
        else:
            return proxy.split(":")

    # OldCheck (Rate Limitation)
    class OldCheck():
        def __init__(selff, proxy):
            proxies = {"http": f"http://{proxy}",
                       "https": f"http://{proxy}"} if proxy else {}
            r = requests.get("http://ip-api.com/json/", proxies=proxies)
            data = r.json()
            selff.country = data.get("country")
            selff.country_code = data.get("countryCode")
            selff.region = data.get("region")
            selff.city = data.get("city")
            selff.zip = data.get("zip")
            selff.country = data.get("country")
            selff.latitude = data.get("lat")
            selff.longitude = data.get("lon")
            selff.timezone = data.get("timezone")
            selff.ip = data.get("query")

        def __str__(selff):
            return str(selff.__dict__)

    class Check():
        def __init__(selff, proxy):
            proxies = {"http": f"http://{proxy}",
                       "https": f"http://{proxy}"} if proxy else {}
            selff.ip = requests.get(
                'https://api.myip.com', proxies=proxies).json().get("ip")
            r = requests.get(f"https://tools.keycdn.com/geo.json?host={selff.ip}", headers={
                             "User-Agent": "keycdn-tools:https://google.com"})
            try:
                data = r.json()["data"]["geo"]
                selff.country = data.get("country_name")
                selff.country_code = data.get("country_code")
                selff.region = data.get("region_name")
                selff.city = data.get("city")
                selff.zip = data.get("postal_code")
                selff.latitude = data.get("latitude")
                selff.longitude = data.get("longitude")
                selff.timezone = data.get("timezone")
            except:
                print(r.text)
                return False

        def __str__(selff):
            return str(selff.__dict__)


class Generator:
    async def initialize(self, proxy, mode=None, output_file="output.txt"):
        # Initializing the Thread
        # threading.Thread.__init__(self)
        self.last_x, self.last_y = 0, 0
        self.proxy, self.mode, self.output_file = proxy, mode, output_file
        # SettingUp Logger
        logging.basicConfig(
            format='\033[34m[%(levelname)s] - \033[94mLine %(lineno)s  - \033[36m%(funcName)s() - \033[96m%(message)s\033[0m')
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.DEBUG)
        # Initializing Faker, ComputerInfo, PersonInfo and ProxyInfo
        self.faker = Faker()
        self.computer, self.person, self.proxy_info = self.faker.Computer(
        ), self.faker.Person(), Proxy().Check(self.proxy)
        if not self.proxy_info:
            self.logger.error("Couldnt load the Proxy info")
            return
        # Initializing LocaleInfo and Browser
        self.locale = self.faker.Locale(self.proxy_info.country_code)
        await self.initialize_browser()
        if mode == 1:
            await self.generate_token()
        elif mode == 2:
            await self.generate_unclaimed()
        elif mode == 3:
            await self.check_captcha()

        return

    async def initialize_browser(self):
        # Browser Proxy Formatter
        if self.proxy:
            self.split_proxy = Proxy().Split(self.proxy)
            if len(self.split_proxy) == 4:
                self.browser_proxy = {
                    "server": f"{self.split_proxy[0]}:" + self.split_proxy[1], "username": self.split_proxy[2], "password": self.split_proxy[3]}
            else:
                self.browser_proxy = {
                    "server": f"{self.split_proxy[0]}:" + self.split_proxy[1]}
        else:
            self.browser_proxy = {}
        # Starting Playwright
        playwright = await async_playwright().start()
        # Launching Firefox with Human Emulation
        main_browser = await playwright.firefox.launch(devtools=True, headless=False, proxy=self.browser_proxy if self.proxy else None)
        # Context for more options
        browser = await main_browser.new_context(
            locale="en-US",  # self.locale.locale
            geolocation={'longitude': self.proxy_info.longitude,
                         'latitude': self.proxy_info.latitude, "accuracy": 0.7},
            timezone_id=self.proxy_info.timezone,
            permissions=['geolocation'],
            screen={"width": self.computer.avail_width,
                    "height": self.computer.avail_height},
            user_agent=self.computer.useragent,
            viewport={"width": self.computer.width,
                      "height": self.computer.height},
        )
        # Grant Permissions to Discord to use Geolocation
        await browser.grant_permissions(["geolocation"], origin="https://discord.com")
        # Create new Page and do something idk why i did that lol
        page = await browser.new_page()
        await page.emulate_media(color_scheme="dark", media="screen", reduced_motion="reduce")
        # Stealthen the page with custom Stealth Config
        config = playwright_stealth.StealthConfig()
        config.navigator_languages, config.permissions, config.navigator_platform, config.navigator_vendor, config.outerdimensions = False, False, False, False, False
        config.vendor, config.renderer, config.nav_user_agent, config.nav_platform = self.computer.vendor, self.computer.renderer, self.computer.useragent, "Win32"
        config.languages = ('en-US', 'en', self.locale.locale,
                            self.locale.language_code)
        await playwright_stealth.stealth_async(page, config)
        self.browser, self.page = browser, page

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

    async def click_humanly(self, element="", locator=""):
        # Getting Element by Selector if Element isnt passed
        if not element:
            element = self.page.locator(locator)
        # Get a random coordinate inside the element
        coordinates = await element.bounding_box()
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

    async def captcha_solver(self):
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
            self.logger.error("Captcha Question didnt load")
            return False
        self.label = re.split(
            r"containing a", question)[-1][1:].strip() if "containing" in question else question
        self.label = self.label.replace(".", "")
        # Initializing ArmorCaptcha
        self.challenger = ArmorCaptcha(dir_workspace=DIR_CHALLENGE, dir_model=DIR_MODEL, lang='en', debug=True,
                                       path_objects_yaml=PATH_OBJECTS_YAML, onnx_prefix="yolov5s6")
        # Getting Lavel and Model from AI
        self.challenger.label = self.label
        self.model = self.challenger.switch_solution()  # DIR_MODEL, None
        # Solving Captcha with AI
        self.results, timee = [], time.perf_counter()
        # Getting first 9 of the logged Images (First nine are the CaptchaImages)
        for image_url in self.images[:9]:
            # Getting Content of Image
            data = requests.get(image_url).content
            # Getting Result from AI and appending it to list
            try:
                result = self.model.solution(
                    img_stream=data, label=self.challenger.label_alias[self.label])
            except KeyError:
                self.logger.error(f"AI doesnt support {self.label} yet!")
                return False
            self.results.append(result)
        await self.page.wait_for_timeout(1000)
        # If Results are Invalid Reload Captcha and Recurse
        if not any(self.results):
            self.logger.warning("AI Results were incorrect, redoing Captcha")
            self.images = []
            await self.click_humanly(self.checkbox, "")
            await self.page.wait_for_timeout(2000)
            await self.click_humanly(self.checkbox, "")
            await self.captcha_solver()
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
        for i in range(100):
            captcha_locator = self.page.locator(
                '[title *= "hCaptcha security challenge"]')
            captcha_token = await captcha_locator.get_attribute("data-hcaptcha-response")
            if captcha_token:
                censored_token = f"{captcha_token.split('.')[0]}.{captcha_token.split('.')[1][:5]}*****"
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

    async def get_token(self):
        # js = "(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()"
        js1 = "var iframe = document.createElement('iframe');iframe.style.display = 'none';document.body.prepend(iframe);window.localStorage = iframe.contentWindow.localStorage;"
        await self.page.evaluate(js1)
        token_evaluated = await self.page.evaluate("window.localStorage.token")
        self.token = str(token_evaluated).replace('"', "")
        print(self.token)

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
        except Exception as e:
            self.logger.error("Captcha didn´t load")
            return False
        await self.checkbox.scroll_into_view_if_needed()
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        await self.page.close()
        await self.browser.close()

    async def generate_unclaimed(self):
        # Going on Discord Register Site
        try:
            await self.page.goto("https://discord.com/")
        except:
            self.logger.error("Site didn´t load")
            return False
        # Click Open InBrowser Button
        await self.click_humanly("", '[class *= "gtm-click-class-open-button"]')
        # Typing Username
        await self.type_humanly('[class *= "username"]', self.person.username)
        # Clicking Tos and Submit Button
        try:
            await self.click_humanly("", "[class *='termsCheckbox']")
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
        except:
            self.logger.error("Captcha didn´t load")
            return False
        await self.checkbox.scroll_into_view_if_needed()
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        while True:
            try:
                await self.get_token()
                break
            except Exception as e:
                await self.page.wait_for_timeout(2000)

        self.logger.info(f"Generated Token: {self.token}")
        with open(self.output_file, 'a') as file:
            file.write(f"\n{self.token}")

        await self.page.wait_for_timeout(3000)
        await self.type_humanly('[id="react-select-2-input"]', self.person.birth_day)
        await self.page.keyboard.press("Enter")
        await self.type_humanly('[id="react-select-3-input"]', self.person.birth_month)
        await self.page.keyboard.press("Enter")
        await self.type_humanly('[id="react-select-4-input"]', self.person.birth_year)
        await self.page.keyboard.press("Enter")
        self.logger.info("Successfully entered Birthday! Closing Browser...")

        await self.page.close()
        await self.browser.close()

    async def generate_token(self):
        # Going on Discord Register Site
        try:
            await self.page.goto("https://discord.com/register")
        except:
            self.logger.error("Site didn´t load")
            return False
        # Typing Email, Username, Password
        await self.type_humanly('[name="email"]', self.person.username+f"{random.randint(10,99)}@gmail.com")
        await self.type_humanly('[name="username"]', self.person.username)
        await self.type_humanly('[name="password"]', self.person.password)
        # Typing BirthDay, BirthMonth, BirthYear
        await self.type_humanly('[id="react-select-2-input"]', self.person.birth_day)
        await self.page.keyboard.press("Enter")
        await self.type_humanly('[id="react-select-3-input"]', self.person.birth_month)
        await self.page.keyboard.press("Enter")
        await self.type_humanly('[id="react-select-4-input"]', self.person.birth_year)
        # Clicking Tos and Submit Button
        try:
            await self.click_humanly("", "[type='checkbox']")
        except Exception as e:
            self.logger.debug("No TOS Checkbox was detected")
            pass
        self.click_humanly("", '[type="submit"]')
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
        except:
            self.logger.error("Captcha didn´t load")
            return False
        await self.checkbox.scroll_into_view_if_needed()
        await self.click_humanly(self.checkbox, "")
        await self.page.wait_for_timeout(2000)
        captcha = await self.captcha_solver()

        while True:
            try:
                await self.get_token()
                break
            except Exception as e:
                await self.page.wait_for_timeout(2000)

        self.logger.info(f"Generated Token: {self.token}")
        with open(self.output_file, 'a') as file:
            file.write(f"\n{self.token}")

        self.logger.info("Successfully Generated Account! Closing Browser...")

        await self.page.close()
        await self.browser.close()


async def main():
    mode = input("[Select] - [Generation Mode]\n" + "<1> Generate Token\n" +
                 "<2> Generate Unclaimed Token\n" + "<3> Test Captcha\n" + "</> ")
    if mode not in ("1", "2", "3"):
        raise ValueError("Invalid Mode provided")
    else:
        mode = int(mode)

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

    while True:
        threadz = []
        for _ in range(threads):
            proxy = random.choice(proxies) if proxies else None
            threadz.append(Generator().initialize(proxy, mode, output_file))

        await asyncio.gather(*threadz)


if __name__ == '__main__':
    asyncio.run(main())
