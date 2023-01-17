import datetime
import time 
import os
import requests

enableSysTray = False
if os.name == 'nt':
    from infi.systray import SysTrayIcon
    enableSysTray = True

walletaddress = 'xch1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx''

sendDiscord = True
discordWebhook = r'https://discord.com/api/webhooks/0000000000000000/xxxxxxxxxxxxxxxxxxxxxxxxxxxx''

#Send push notification over Pushover?
sendPushover = False
pushoverUserKey = 'xxxxxxxxxx'
pushoverAPIKey = 'xxxxxxxxxxxxxxxx'

#Play a custom sound file?
playSound = False
song = 'audio.mp3'

#Send a slack notification?
sendSlack = False
slack_token = 'xoxb-my-bot-token'
slack_channel = '#my-channel'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Chia Wallet Monitor'


#SendPushBullet notification?
sendPushBullet = False
pbAPIKey = 'XXXXXXXXXXXXXXXXXXXXX'

def on_quit_callback(systray):
    print("QUIT!")
    if systray:
        systray.shutdown()
   

def checkWallet(systray):
    print("Wallet check")

menu_options = (("Check Wallet", None, checkWallet),)
if enableSysTray:
    systray = SysTrayIcon("chia.ico", "ChiaWalletMonitor", menu_options, on_quit=on_quit_callback)



#BEGIN


#let there is no data initially
chiaWallet = None
currXCH = 0
netBalance = -1
firstRun = True
if enableSysTray:
    systray.start()

headers = requests.utils.default_headers()
print(headers)      
headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36;"})

while(True):

    shouldPrint = None
    try:
        
        chiaWallet = requests.get("https://xchscan.com/api/account/balance?address=" + walletaddress, headers=headers)
    except:
        print("Please! Check your internet connection")

    if (chiaWallet != None):
        data = chiaWallet.json()
        netBalance = data['xch']

        if (firstRun == True):
            shouldPrint = True
            msgTitle = "Your wallet as of {}".format(datetime.date.today())
            msgTxt = "You have a total of {} XCH, Farmer!".format(netBalance)
            
        else:
            if currXCH != netBalance:
                shouldPrint = True
                msgTxt = "Your Chia balance has changed, for a total of {netBalance} XCH!".format(netBalance = data['xch'])
                msgTitle = 'Congrats, Chia Farmer!'
                
                
                if sendDiscord == True:
                    import discord_notify as dn
                    discord_info = msgTxt
                    notifier = dn.Notifier(discordWebhook)
                    notifier.send(discord_info, print_message=False)
                
    if shouldPrint == True:
        print(msgTxt)
    
    shouldPrint = False
    firstRun = False
    currXCH = netBalance
    time.sleep(60*3)
