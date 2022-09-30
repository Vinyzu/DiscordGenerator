# PreInstalled PyPackages
import asyncio
import logging
import os
import random
import traceback

# Pip Install Packages
import botright
import httpx
import validators

# Imports from Files
from modules.discord import Discord
from modules.tempmail import TempMail

class Generator:
    async def initialize(self, botright_client, proxy, mode=None, output_file="output.txt", email=True, humanize=True, output_format="token:email:pass", invite_link=""):
        # Initializing the Thread
        self.output_file, self.output_format = output_file, output_format
        self.email_verification, self.humanize, self.invite_link = email, humanize, invite_link
        self.token, self.email, self.output = "", "", ""
        # SettingUp Logger
        logging.basicConfig(
            format='\033[34m[%(levelname)s] - \033[94mLine %(lineno)s  - \033[36m%(funcName)s() - \033[96m%(message)s\033[0m')
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.DEBUG)

        # Initializing Browser and Page
        self.browser = await botright_client.new_browser(proxy)
        self.logger.info("Spawned Browser successfully")

        self.page = await self.browser.new_page()

        if mode == 1:
            await self.generate_unclaimed()
        elif mode == 2:
            await self.generate_token()
        elif mode == 3:
            await self.check_captcha()
        return

    # Helper Functions
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

    def log_output(self):
        output = ""
        for item in self.output_format.split(":"):
            if "token" in item and self.token:
                output += self.token + ":"
            if "email" in item and self.email:
                output += self.email + ":"
            if "pass" in item:
                output += self.browser.faker.password + ":"
            if "proxy" in item and self.browser.proxy:
                output += self.browser.proxy + ":"

        # Remove last :
        output = output[:-1]
        self.output = output

    async def close(self):
        try:
            await self.page.close()
        except:
            pass
        try:
            await self.browser.close()
        except:
            pass

    # Main Functions
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
            # Click Open InBrowser Button
            await self.page.click('[class *= "gtm-click-class-open-button"]')
            # Typing Username
            await self.page.type('[class *= "username"]', self.browser.faker.username)
            # Clicking Tos and Submit Button
            try:
                await self.page.click("[class *= 'checkbox']", timeout=10000)
            except Exception as e:
                self.logger.debug("No TOS Checkbox was detected")
                pass
            await self.page.click('[class *= "gtm-click-class-register-button"]')

            # Solving Captcha
            await self.page.solve_hcaptcha()

            while not self.token:
                await self.page.wait_for_timeout(2000)

            self.logger.info(f"Generated Token: {self.token}")
            await self.page.wait_for_timeout(2000)

            is_locked = await Discord.is_locked(self)
            if is_locked:
                self.logger.error(f"Token {self.token} is locked!")
                await self.close()
                return
            else:
                self.logger.info(f"Token: {self.token} is unlocked! Flags: {self.flags}")

            self.log_output()

            await self.page.wait_for_timeout(3000)
            try:
                await self.page.type('[id="react-select-2-input"]', self.browser.faker.birth_day)
                await self.page.keyboard.press("Enter")
                await self.page.type('[id="react-select-3-input"]', self.browser.faker.birth_month)
                await self.page.keyboard.press("Enter")
                await self.page.type('[id="react-select-4-input"]', self.browser.faker.birth_year)
                await self.page.keyboard.press("Enter")
                await self.page.wait_for_timeout(1000)
                await self.page.keyboard.press("Enter")
            except:
                pass

            # Closing PopUps
            for _ in range(2):
                try:
                    await self.page.click("[class *= 'closeButton']", timeout=5000)
                except:
                    pass

            if self.email_verification:
                self.inbox = TempMail.generateInbox()
                self.logger.info("Claiming Account...")
                await Discord.set_email(self, self.inbox.address)

                await self.page.wait_for_timeout(2000)

                self.logger.info("Verifying email...")
                await Discord.confirm_email(self)

            self.log_output()

            await self.page.wait_for_timeout(2000)

            if self.humanize:
                await Discord.humanize_token(self)

            await self.page.wait_for_timeout(2000)

            if self.invite_link:
                await Discord.join_server(self)

            self.log_output()
            with open(self.output_file, 'a') as file:
                file.write(f"{self.output}\n")

            self.logger.info("Successfully Generated Account! Closing Browser...")

            await self.close()

        # Catch Exceptions and save output anyways
        except:
            self.logger.error(f"Catched Exception, trying to save Token anyways... \n Error: \n {traceback.format_exc()}")
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
            # Typing Email, Username, Password
            self.email = f"{self.browser.faker.username}{random.randint(10, 99)}@gmail.com"

            if self.email_verification:
                self.inbox = TempMail.generateInbox()
                self.email = self.inbox.address
            await self.page.type('[name="email"]', self.email)
            await self.page.type('[name="username"]', self.browser.faker.username)
            await self.page.type('[name="password"]', self.browser.faker.password)
            # Typing BirthDay, BirthMonth, BirthYear
            await self.page.type('[id="react-select-2-input"]', self.browser.faker.birth_day)
            await self.page.keyboard.press("Enter")
            await self.page.type('[id="react-select-3-input"]', self.browser.faker.birth_month)
            await self.page.keyboard.press("Enter")
            await self.page.type('[id="react-select-4-input"]', self.browser.faker.birth_year)
            # Clicking Tos and Submit Button
            try:
                tos_box = self.page.locator("[type='checkbox']").first
                await tos_box.click()
            except Exception as e:
                self.logger.debug("No TOS Checkbox was detected")
                pass
            await self.page.click('[type="submit"]')

            await self.page.solve_hcaptcha()

            while not self.token:
                await self.page.wait_for_timeout(2000)

            self.logger.info(f"Generated Token: {self.token}")
            await self.page.wait_for_timeout(2000)

            is_locked = await Discord.is_locked(self)
            if is_locked:
                self.logger.error(f"Token {self.token} is locked!")
                await self.close()
                return
            else:
                self.logger.info(
                    f"Token: {self.token} is unlocked! Flags: {self.flags}")

            self.log_output()

            await self.page.wait_for_timeout(2000)

            # Closing PopUps
            for _ in range(2):
                try:
                    await self.page.click("[class *= 'closeButton']", timeout=5000)
                except:
                    pass

            if self.email_verification:
                self.logger.info("Verifying email...")
                await Discord.confirm_email(self)

            self.log_output()

            await self.page.wait_for_timeout(2000)

            if self.humanize:
                await Discord.humanize_token(self)

            await self.page.wait_for_timeout(2000)

            if self.invite_link:
                await Discord.join_server(self)

            self.log_output()
            with open(self.output_file, 'a') as file:
                file.write(f"{self.output}\n")

            self.logger.info(
                "Successfully Generated Account! Closing Browser...")

            await self.close()

        # Catch Exceptions and save output anyways
        except:
            self.logger.error(f"Catched Exception, trying to save Token anyways... \n Error: \n{traceback.format_exc()}")
            if self.output:
                with open(self.output_file, 'a') as file:
                    file.write(f"{self.output}\n")

    # Testing (Maybe used later?)
    async def login_token(self):
        # Going on Discord Register Site
        try:
            await self.page.goto("https://discord.com/register")
        except:
            self.logger.error("Site didn´t load")
            return False
        await self.page.evaluate(str('setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"' + self.token + '"`}, 2500); setTimeout(() => {location.reload();}, 2500);'))
        await self.page.wait_for_timeout(5000)

        if self.email_verification:
            self.inbox = TempMail.generateInbox()
            self.logger.info("Claiming Account...")
            await Discord.set_email(self, self.inbox.address)
            await self.page.wait_for_timeout(2000)
            self.logger.info("Verifying email...")
            await Discord.confirm_email(self)
        # self.log_output()
        # await self.page.wait_for_timeout(2000)
        # if self.humanize:
        #     await Discord.humanize_token(self)
        # await self.page.wait_for_timeout(2000)
        if self.invite_link:
            await Discord.join_server(self)
        self.log_output()
        with open(self.output_file, 'a') as file:
            file.write(f"{self.output}\n")
        self.logger.info("Successfully Generated Account! Closing Browser...")
        await self.close()


async def main():
    botright_client = await botright.Botright(headless=False)
    print(""" _____     __     ______     __         ______     ______     __  __
/\  __-.  /\ \   /\  ___\   /\ \       /\  __ \   /\  ___\   /\ \/ /
\ \ \/\ \ \ \ \  \ \___  \  \ \ \____  \ \ \/\ \  \ \ \____  \ \  _"-.
 \ \____-  \ \_\  \/\_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\\
  \/____/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/    | Made by Vinyzu
                                                                           | https://github.com/Vinyzu/DiscordGenerator""")

    mode = input("[Select] - [Generation Mode]\n" + "<1> Generate Unclaimed Token\n" + "<2> Generate Token\n" + "<3> Test Captcha\n" + "</> ")
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
                       "<?> Or Leave empty for Proxyless Mode\n" + "</> ").replace('"', "")
    if proxy_file:
        if not os.path.isfile(proxy_file):
            raise ValueError("Provided ProxyPath isnt a file!")
        proxies = open(proxy_file, 'r').readlines()
    else:
        proxies = None

    output_file = input("[Drag&Drop] - [Output File]\n" +
                        "<?> Or Leave empty to use output.txt\n" + "</> ").replace('"', "")
    if output_file:
        if not os.path.isfile(output_file):
            raise ValueError("Provided OutputPath isnt a file!")
    else:
        output_file = "output.txt"

    invite = input("[Input] - [Invite Link]\n" +
                   "<?> Either parse a InviteLink, or an InviteCode\n" + "</> ")

    if not validators.url(invite) and invite:
        invite_link = f"https://discord.gg/{invite}"
        if not validators.url(invite_link) or not httpx.get(f"https://discordapp.com/api/v8/invites/{invite}").is_success:
            raise ValueError(f"Invalid InviteLink: {invite}")
    else:
        invite_code = invite.split("/")[-1]
        if invite and not httpx.get(f"https://discordapp.com/api/v8/invites/{invite_code}").is_success:
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

    try:
        while True:
            threadz = []
            for _ in range(threads):
                proxy = random.choice(proxies) if proxies else None
                threadz.append(Generator().initialize(botright_client, proxy, mode, output_file, email, humanize, output_format, invite_link))

            await asyncio.gather(*threadz)
    except KeyboardInterrupt:
        await botright_client.close()
    except Exception:
        print(traceback.format_exc())
        await botright_client.close()


if __name__ == '__main__':
    asyncio.run(main())
