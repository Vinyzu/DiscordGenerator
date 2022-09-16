# Edited by FuckingToaster's Fork:
  ## New Features & Improvments
    - Got rid of Tempmail.lol (their ip for dns record is blocked by discord & more code take longer to execute)
    - Using IMAP (free custom domain, not blocked by discord & faster verification)
    - Added external configuration file to setup IMAP
    - Fixed Tokens aren't saved in the file after verìfîcation (wasn't saved before if joining a invite failed)
  [Note: Some TLDs are blocked by discord (discord won't send a email to them. I noticed it for .monster but there might be more]

  ## Setup Mail Verification:
    - Create a GMAIL Account which is used to forward all Discord Mails to
    - Setup 2FA on the GMAIL Account you just made
    - Navigate to this Site: https://mail.google.com/mail/u/2/#settings/fwdandpop and enable the IMAP Option
    - Add a App Password here: https://myaccount.google.com/u/2/security (Option is only shown if 2FA is enabled) | Set App to Other and choose a random Name)
    - Add your Details in the config File.
  
## Using a Custom Domain:
    - Follow the Steps above in Setup Mail Verification and then contine with the Info below
    - Register a Account at https://improvmx.com
    - Setup the DNS Records the Site provide you with in your Domain's DNS Settings
    - Add your Domain Forwarding to * (This forward all mails sent to custom domain to the gmail you just made)
  

# Orginal Readme created by the orginal Author's
# DISLOCK

# I accidently deleted the v2.0 update files (bout 1 week or 30 workhours), this project is discontinued for a bit, while im working on botright.

# I decided to do that because i can easily build this on botright when its finished.

DISLOCK is the most advanced Discord Browser Generator.

It is capable of generating Unlocked Tokens for free by Using AI.
DISLOCK is currently undetected by Discord because its Human Emulation.

You will have to use HQ Proxies/IPs to get unlocked tokens.

## Features

- TokenGenerator on discord.com [Almost always Unlocked]
- TokenGenerator on discord.com/register [Mostly Unlocked]
- Captcha Tester on hcaptcha.com

## Demo Videos

### Unclaimed Generator
https://streamable.com/4wvhdw

### Normal Generator
https://streamable.com/w9l2fz

## Proxies

You will have to use HQ Proxies/IPs to get Unlocked Tokens.
If you really want to generate proxies, you maight have to spend fairly big amounts of money, to get undetected/unflagged IPs.
If you just want to test the Generator, you can also just restart your InternetRouter (if you have a rotating IP) and Discord wont notice.

(Btw your Proxy AD can stand here, DM me for offers ;d ;:D)

## Artificial Intelligence

The AI of this bot is not mine and i dont take any credits for it.

It was created by QIN2DIM and can be found [here](https://github.com/QIN2DIM/hcaptcha-challenger).
If you want to update the AI because im late, you will have to grab the files from given repository.

`You maight want to regulary update objects.yaml by copy and pasting https://github.com/QIN2DIM/hcaptcha-challenger/blob/main/src/objects.yaml`

However, i edited out some code/files, to make DISLOCK lightweighter and to use less imports.

Also, i coded a MouseMovement Generator, to get more realistic MotionData. It uses Interpolation between CaptchaImage-Coordinates to do so.

My Playwright hCaptchaSolver can be easily plugged by replicating [check_captcha()](https://github.com/Vinyzu/DiscordGenerator/blob/main/main.py#L491) in your project.

## Installation

### Installing DISLOCK with Python

```bash
  git clone https://github.com/Vinyzu/DISLOCK DISLOCK
  cd DISLOCK
  pip install -r requirements.txt
  playwright install
  python main.py
```

### Further Requirements

- Windows

- [Git](https://git-scm.com/downloads) (To install DISLOCK)
- [Pip](https://pip.pypa.io/en/stable/installation/) (To install DISLOCK)

## Using

Type     | Recommended Usage              |
 :------- | :------------------------- |
| `Token Generator` | Generating HQ token (sometimes) locked the classic way |
| `Unclaimed Generator` | Generating Unclaimed, HQ (mostly) unlocked tokens  |
| `Captcha Tester` | Testing the CaptchaAI on hCaptcha.com |

##### Usages will be updated when Discord fixxes Modes

## Contributing

Contributions are always welcome!

See [Contributing](https://github.com/Vinyzu/DiscordGenerator/blob/main/contributing.md) for ways to get started.


## To the Skids

Hello, skid. I know its in your nature to laboriously copy and paste this project and sell it as yours. And i can´t 100% prevent that. However, legally you aren´t allowed to share your skidded DISLOCK other than the source code. And i know that you give a fuck about Licenses and Copyright, but if you gonna use this code as yours and don´t mark me as the original author, i can assure you that you won´t have a good time selling this ;d.

## Copyright and License
© [Vinyzu](https://github.com/Vinyzu/)

[GNU GPL](https://choosealicense.com/licenses/gpl-3.0/)

(Commercial Usage is allowed, but source, license and copyright has to made available. DISLOCK does not provide and Liability or Warranty)

## Authors

- [@Vinyzu](https://github.com/Vinyzu)

`If you appreciate this Repository, I would love to see you star and share this. It took a lot of effort and time to code all of those features and i originally planned to sell this project, so I´m "wasting" money for everyone´s fun ;:D.`



[![mjolnir-discord](https://img.shields.io/badge/Mjolnir_Discord-000?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/rpd4gzrqGN)
[![my-discord](https://img.shields.io/badge/My_Discord-000?style=for-the-badge&logo=google-chat&logoColor=blue)](https://discordapp.com/users/935224495126487150)
[![buy-me-a-coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-000?style=for-the-badge&logo=ko-fi&logoColor=brown)](https://ko-fi.com/vinyzu)


## Thanks to

[QIN2DIM](https://github.com/QIN2DIM/) (For his great AI work.)

[MaxAndolini](https://github.com/MaxAndolini) (For shared knowledge of hCaptcha bypassing)

[Dönerbäcker](https://github.com/DoenerBaecker) (For Proxies)


![Version](https://img.shields.io/badge/DISÖOCK-v1.0.0-blue)
![License](https://img.shields.io/badge/License-GNU%20GPL-green)
![Python](https://img.shields.io/badge/Python-v3.x-lightgrey)
![Platforms](https://img.shields.io/badge/Platform-win--32%20%7C%20win--64-lightgrey)
