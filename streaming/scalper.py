
import threading
from queue import Queue
import time

from models.trade_decision import TradeDecision
from scalperhelper import close_order
# from streaming.trade_manager import place_trade

class ScalperWorker(threading.Thread):

    def __init__(self,mt5Api,pair,log_message ) :
        super().__init__()
        self.mt5Api  = mt5Api
        self.pair  = pair
        self.log_message = log_message

    def monitor_profit(self, symbol,max_loss):
        # Handle negative values ok..... TODO
        try:
            firstposition = self.mt5Api.positions_get(symbol=symbol)[0]
            max_profit = firstposition.profit
            count = 0
            loss=0
            percent_loss = 0
            while True:
                count = count + 1
                time.sleep(2)
                position=self.mt5Api.positions_get(symbol=symbol)[0]
                print(position)
                #handle negative profit to wait while nnot less than bearable threashold
                if position.profit < 0: 
                    if position.profit  > max_loss:
                        continue
                    else:
                        break

                if position.profit > max_profit:
                    max_profit = position.profit
                    loss = 0
                else:
                    loss = max_profit - position.profit
                    percent_loss = ((abs(loss)/max_profit)*100)
                    if percent_loss > 15:
                        break
                if count % 2 == 0:
                    print(f"current profit: {position.profit}, max profit: {max_profit}...loss{loss} ... percentage loss {percent_loss}")
            close_order(self.mt5Api,position)
        except Exception as error:
            self.log_message(f"Exception in monitor profit: {error}", 'error')


    def run(self):
        while True:
            self.log_message(f"ScalperWorker : ", 'main')
            self.log_message(f"ScalperWorker : ", self.pair)
            # print("Scalper Worker: Hello")
            self.monitor_profit(self.pair, -1.5)
            
        
           