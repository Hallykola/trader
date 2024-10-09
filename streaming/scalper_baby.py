
import threading
from queue import Queue
import time

from constants import defs
from models.trade_decision import TradeDecision
from scalperhelper import close_order
# from streaming.trade_manager import place_trade

class ScalperBaby(threading.Thread):

    def __init__(self,mt5Api,position,offenders_work_queue,log_message ) :
        super().__init__()
        self.mt5Api  = mt5Api
        self.position  = position
        self.offenders_work_queue = offenders_work_queue
        self.log_message = log_message

    def monitor_profit(self, position,max_loss,min_gain):
        # Handle negative values ok..... TODO
        
        try:
            position = self.mt5Api.positions_get(ticket=position.ticket)[0]
            
            max_profit = position.profit
            count = 0
            loss=0
            percent_loss = 0
            while True:
                count = count + 1
                time.sleep(1)
                allpositions=self.mt5Api.positions_get(symbol=position.symbol)
                position=self.mt5Api.positions_get(ticket=position.ticket)[0]
                
                #handle negative profit to wait while not less than bearable threashold
                if position.profit < 0: 
                    print(f" i am in monitor profit {position.symbol} but less than 0")
                    if position.profit < defs.report_loss_threashold :
                        
                        
                        # avoid a counter counter
                        if len(allpositions) < 3:  #27
                            print(f"Putting offender {position.symbol} in queue")
                            self.offenders_work_queue.put(position)
                            time.sleep(3)
                        break
                    elif position.profit  > max_loss:
                        continue
                    else:
                        break

                if position.profit > max_profit:
                    max_profit = position.profit
                    loss = 0
                elif position.profit < min_gain:
                    continue
                else:
                    loss = max_profit - position.profit
                    percent_loss = ((abs(loss)/max_profit)*100)
                    if percent_loss > 10:
                        break
                if count % 2 == 0:
                    print(f"current profit: {position.profit}, max profit: {max_profit}...loss{loss} ... percentage loss {percent_loss}")
                
            close_order(self.mt5Api,position)
        except Exception as error:
            self.log_message(f"Exception in monitor profit: {error}", 'error')


    def run(self):
        while True:
            # pass
            # self.log_message(f"ScalperWorker : ", 'main')
            # self.log_message(f"ScalperWorker : ", self.pair)
            # print("Scalper Worker: Hello")
            #paused scalperworker
            self.monitor_profit(self.position, -0.9,0.10)
            
        
           