import random
import base64
import platform
import re
import tempfile
import os

import httpx

from modules import tempmail

res = httpx.get("https://discord.com/login").text
file_with_build_num = 'https://discord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(res)[-2]+'.js'
req_file_build = httpx.get(file_with_build_num).text
index_of_build_num = req_file_build.find('buildNumber')+24
DISCORD_BUILD_NUM = int(req_file_build[index_of_build_num:index_of_build_num+6])

class Discord:
    async def get_headers(self, payload):
        cookies = await self.browser.cookies()
        __dcfduid = [item for item in cookies if item['name'] == "__dcfduid"][0]["value"]
        __sdcfduid = [item for item in cookies if item['name'] == "__sdcfduid"][0]["value"]
        cookies = f"__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}"

        super_props = {"os": platform.system(), "browser":"Firefox", "release_channel":"stable", "client_version": self.browser.browser.version, "os_version": str(platform.version()), "os_arch": "x64" if platform.machine().endswith('64') else "x86", "system_locale": self.browser.faker.locale, "client_build_number": DISCORD_BUILD_NUM, "client_event_source": None}
        super_props = base64.b64encode(str(super_props).encode()).decode()

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "de,de-DE;q=0.9",
            "authorization": self.token,
            "content-length": str(len(str(payload))),
            "content-type": "application/json",
            "cookie": cookies,
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.browser.faker.useragent,
            "x-discord-locale": "en",
            "x-super-properties": super_props,
        }
        return headers

    async def humanize_token(self):
        await self.page.goto("https://discord.com/channels/@me")
        await self.page.wait_for_timeout(1000)
        # Clicking Settings Button
        settings_button = self.page.locator('[class *= "button-12Fmur"]').last
        await settings_button.click()
        # Click Profile Button
        await self.page.wait_for_timeout(500)
        profile_button = self.page.locator('[class *= "item-3XjbnG"]').nth(6)
        await profile_button.click()

        await self.page.wait_for_timeout(random.randint(2000, 3000))

        # Setting Random Avatar
        pics = httpx.get("https://api.github.com/repos/itschasa/Discord-Scraped/git/trees/cbd70ab66ea1099d31d333ab75e3682fd2a80cff")
        random_pic = random.choice(pics.json().get("tree")).get("path")
        pic_url = f"https://raw.githubusercontent.com/itschasa/Discord-Scraped/main/avatars/{random_pic}"
        pic = httpx.get(pic_url).content

        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_file.write(pic)
        temp_file.file.seek(0)  # change the position to the beginning of the file

        self.page.on("filechooser", lambda file_chooser: file_chooser.set_files(temp_file.name))

        upload_avatar_button = self.page.locator('[class *= "buttonsContainer-12kYno"]').locator('[class *= "lookFilled-yCfaCM "]')
        await upload_avatar_button.click()

        await self.page.wait_for_timeout(random.randint(500, 1000))

        upload_own = self.page.locator('[class *= "file-input"]')
        await upload_own.click()

        await self.page.wait_for_timeout(random.randint(500, 1000))
        confirm_button = self.page.locator('[class *= "button-f2h6uQ"]').last
        await confirm_button.click()

        temp_file.close()
        os.unlink(temp_file.name)


        await self.page.wait_for_timeout(random.randint(2000, 3000))

        # Setting AboutME
        try:
            quote = httpx.get("https://free-quotes-api.herokuapp.com")
            quote = quote.json().get("quote")
        except:
            self.logger.warning('Couldnt Get a Random Quote, Setting "Dislock" as AboutMe')
            quote = "Dislock"

        profile_button = self.page.locator('[role="textbox"]')
        await profile_button.click()
        await self.page.keyboard.type(quote)

        await self.page.wait_for_timeout(random.randint(500, 1000))
        confirm_button = self.page.locator('[class *= "colorGreen-3y-Z79"]').last
        await confirm_button.click()

        # Going to Hypesquad Page
        hypesquad_button = self.page.locator('[aria-controls="hypesquad-online-tab"]')
        await hypesquad_button.click()

        await self.page.wait_for_timeout(random.randint(5000, 6000))

        # Setting Hypesquad
        # payload = {"house_id": random.randint(1, 3)}
        # headers = await Discord.get_headers(self, payload)
        # hypesquad = await self.page.request.post("https://discord.com/api/v9/hypesquad/online", data=payload, headers=headers)
        # print(await hypesquad.json())

        is_locked = await Discord.is_locked(self)
        if is_locked:
            self.logger.error(f"Token {self.token} got locked whilst humanizing!")
            await self.close()
            return

        self.log_output()
        self.logger.info(f"Set Bio and ProfilePic!")

    async def join_server(self):
        await self.page.goto("https://discord.com/channels/@me")
        await self.page.wait_for_timeout(1000)
        # Clicking Join Server Button
        create_join_button = self.page.locator('[data-list-item-id *= "create-join-button"]')
        await create_join_button.click()
        await self.page.wait_for_timeout(500)
        # Clicking Join a Server Button
        another_server_button = self.page.locator('[class *= "footerButton-24QPis"]')
        await another_server_button.click()
        # Type Invite Code
        await self.page.wait_for_timeout(1000)
        await self.page.type("[placeholder='https://discord.gg/hTKzmak']", self.invite_link)
        # Clicking Join Server Button
        join_server_button = self.page.locator('[class *= "lookFilled-yCfaCM"]').last
        await join_server_button.click()

        try:
            await self.page.solve_hcaptcha()
        except:
            self.logger.info("No JoinServer Captcha detected.")

        is_locked = await Discord.is_locked(self)
        if is_locked:
            self.logger.error(f"Token {self.token} got locked whilst joining a Server!")
            await self.close()
            return

        self.log_output()
        self.logger.info("Joined Server successfully.")

    async def is_locked(self):
        token_check = await self.page.request.get('https://discord.com/api/v9/users/@me/library', headers={"Authorization": self.token})
        token_check = token_check.status == 200
        if token_check:
            r = await self.page.request.get('https://discord.com/api/v9/users/@me', headers={"Authorization": self.token})
            response = await r.json()
            self.id = response.get("id")
            self.email = response.get("email")
            self.username = response.get("username")
            self.discriminator = response.get("discriminator")
            self.tag = f"{self.username}#{self.discriminator}"
            self.flags = response.get("public_flags")

        return not token_check

    async def set_email(self, email):
        try:
            # Setting Email
            await self.page.goto("https://discord.com/channels/@me")
            await self.page.wait_for_timeout(1000)
            # Clicking Settings Button
            settings_button = self.page.locator('[class *= "button-12Fmur"]').last
            await settings_button.click()
            # Click Email Button
            await self.page.wait_for_timeout(500)
            settings_button = self.page.locator('[class *= "fieldButton-14lHvK"]').nth(1)
            await settings_button.click()

            # Typing Mail
            mail_input = self.page.locator('[type="text"]').last
            await mail_input.type(email)

            # Typing Password
            password_input = self.page.locator('[type="password"]').last
            await password_input.type(self.browser.faker.password)

            # Click Claim Button
            claim_button = self.page.locator('[type="submit"]').last
            await claim_button.click()
        except Exception as e:
            print(e)

    async def confirm_email(self):
        before_token = self.token
        self.logger.info("Confirming Email...")
        # Getting the email confirmation link from the email
        self.scrape_emails = True
        while self.scrape_emails:
            emails = tempmail.TempMail.getEmails(self.inbox)
            for mail in emails:
                if "mail.discord.com" in str(mail.sender):
                    for word in mail.body.split():
                        if "https://click.discord.com" in word:
                            self.email_link = word
                            self.scrape_emails = False
                            break
        self.email_link = self.email_link.replace("[", "").replace("]", "")

        self.logger.info("Waiting 10 seconds for a more realistic email-verify")
        await self.page.wait_for_timeout(random.randint(10000, 12000))

        # Confirming the email by link
        await self.page.goto(self.email_link)

        try:
            await self.page.solve_hcaptcha()
        except:
            self.logger.info("No EmailCaptcha detected")

        # Waiting until new token is set
        while self.token == before_token:
            await self.page.wait_for_timeout(1000)

        is_locked = await Discord.is_locked(self)
        if is_locked:
            self.logger.error(f"Token {self.token} got locked whilst verifying the Email!")
            await self.close()
            return

        self.log_output()
        return True

