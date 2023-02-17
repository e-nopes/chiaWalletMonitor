import datetime 
import time 
import os
import requests
import discord_notify as dn


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
                    msgTxt = ':four_leaf_clover: {wallet} balance : {} XCH :four_leaf_clover:'.format(float(netBalance[name]), wallet = name )
                    discord_info = msgTxt
                    notifier = dn.Notifier(discordWebhook)
                    notifier.send(discord_info, print_message=False)
                    
                else:
                   if currXCH[name] != netBalance[name]:
                        shouldPrint[name] = True
                        amount = netBalance[name] - currXCH[name]
                        msgTxt = ':four_leaf_clover: {wallet} balance : {netBalance:0.5} XCH :four_leaf_clover:           {sign}{amount:0.5} :seedling:'.format(wallet = name,  netBalance = netBalance[name], sign= '+' if (amount>0) else '', amount = amount)

                        #notify discord
                        discord_info = msgTxt
                        notifier = dn.Notifier(discordWebhook)
                        notifier.send(discord_info, print_message=False)

                currXCH[name] = netBalance[name]
            
            if shouldPrint[name] == True:
                print(msgTxt)
            
            shouldPrint[name] = False
            firstRun[name] = False
            time.sleep(1)
           
    except Exception as e: 
        print (e)

    time.sleep(60*3)
