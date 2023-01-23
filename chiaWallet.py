import datetime #for reading present date
import time 
import os
import requests #for retreiving coronavirus data from web

enableSysTray = False
if os.name == 'nt':
    from infi.systray import SysTrayIcon
    enableSysTray = True

walletaddress = 'xch1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

addressList   = {   'wallet1'  :    'xch1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' ,
                    'wallet2'  :    'xch1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' }

sendDiscord = True
discordWebhook = r'https://discord.com/api/webhooks/0000000000000000/xxxxxxxxxxxxxxxxxxxxxxxxxxxx'


chiaWallet = None
currXCH = dict.fromkeys(addressList.keys(),0)       #rememberd balances
netBalance = dict.fromkeys(addressList.keys(),0)    #taken from chiaWalletRequest
firstRun = dict.fromkeys(addressList.keys(),True)   #init

headers = requests.utils.default_headers()
print(headers)      
headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36;"})

while(True):

    shouldPrint = dict.fromkeys(addressList.keys(),False)

    try:
        # https://xchscan.com/rest-api 
        for name in addressList.keys():
            #print("Requesting ", name, addressList[name])
            chiaWallet = requests.get("https://xchscan.com/api/account/balance?address=" + addressList[name], headers=headers)

            if (chiaWallet != None):
                data = chiaWallet.json()
                netBalance[name] = data['xch']

                if (firstRun[name] == True):
                    shouldPrint[name] = True
                    msgTxt = '* {wallet} has a total of {} XCH'.format(float(netBalance[name]), wallet = name )
                    
                else:
                    if currXCH[name] != netBalance[name]:
                        shouldPrint[name] = True
                        amount = netBalance[name] - currXCH[name]
                        msgTxt = "{wallet} balance changed {sign}{amount:0.5}, {netBalance:0.5} XCH total".format(wallet = name, sign= '+' if (amount>0) else '', amount = amount, netBalance = netBalance[name])
                        
                        import discord_notify as dn
                        discord_info = msgTxt
                        notifier = dn.Notifier(discordWebhook)
                        notifier.send(discord_info, print_message=False)

                currXCH[name] = netBalance[name]
            
            if shouldPrint[name] == True:
                print(msgTxt)
            
            shouldPrint[name] = False
            firstRun[name] = False
            time.sleep(3)
           
    except Exception as e: 
        print (e)

    time.sleep(60*3)
