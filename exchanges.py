from datetime import datetime
import json

class Exchange():
    def __init__(self, orderbooks):
        self.matched = {}
        self.orderbooks = orderbooks
        
    def fee_ladder(self, quantity, price):
        # fee ladder will be less for the bulk orders, higher for the smaller orders
        if quantity <= 50:
            fee_ladder = price*0.05

        elif 50 < quantity <= 150:
            fee_ladder =  price*0.03

        else:
             fee_ladder = price*0.01
        
        return round(fee_ladder,2)

    def update(self, current_matches):
        """ Updates the matched dictionary

        Args:
            current_matches (dict): matched dict from sorts
        """
        if self.matched:
            # if there are previous matches and stock has already have a match extend the matches
            for key in current_matches.keys():
                if key in self.matched.keys():
                    self.matched[key].extend(current_matches[key])
                else:
                    self.matched[key] = current_matches[key]
        else:
            self.matched = current_matches

    def update_todays_trade(self, path="trade_history.json"):
        """Gets today's date and updates json file for trade_history

        Args:
            path (str, optional): [description]. Defaults to "trade_history.json".
        """
        today = datetime.today().strftime('%d-%m-%Y')
        
        try:
            with open(path, "r") as f:
                trade_history = json.load(f)
        except:
            print("File Not Found!")
            
        with open(path, "w") as f:
            trade_history[today] = self.matched
            json.dump(trade_history, f, indent=4)
        
        return self.todays_trade_value(today, trade_history)
        
    def todays_trade_value(self,today, trade_history):
        """Returns today's trade's fees -- fees by matched buy_orders' prices
        Args:
            today (str): date of today '%d-%m-%Y'
            trade_history (dict): trade history dictionary

        Returns:
            [float]: today's total trade fee
        """
        trade_values = 0
        for key, value in trade_history.items():
            if key == today:
                for trade in value: #trade -> key=stock name
                    for order in value[trade]: #value[trade]: orders for a specific stock
                        trade_values += order[3] # fee is stored in the 3. index

        return round(trade_values,2)

    def view_history(self, path="trade_history.json"):
        """loads trade_history.json file for viewing selection

        Args:
            path (str, optional): path of the trade_history.json file. Defaults to "trade_history.json".

        Returns:
            [dict]: trade history dictionary
        """
        with open(path, "r") as f:
            trade_history = json.load(f)
        return trade_history

    def sorting_orders(self):
        """for each stock it sorts buy_orders from max to min and sell orders from min to max and returns them as a sorted lists

        Yields:
            [tuple]: sorted buy and sell orders' lists and the stock name
        """
        for stock in self.orderbooks.buy_order.keys(): # for each stock
            # sort buys from max to min
            buy_infos = zip(self.orderbooks.buy_order[stock]["price"], self.orderbooks.buy_order[stock]["quantity"], self.orderbooks.buy_order[stock]["status"], self.orderbooks.buy_order[stock]["username"])
            # convert list of tuples to list of lists because tuples are not mutable
            sorted_buys = list(map(list, sorted(buy_infos, key=lambda x: x[0], reverse=True)))
            # sort sells from min to max
            sell_infos = zip(self.orderbooks.sell_order[stock]["price"], self.orderbooks.sell_order[stock]["quantity"], self.orderbooks.sell_order[stock]["status"], self.orderbooks.sell_order[stock]["username"])
            # convert list of tuples to list of lists because tuples are not mutable
            sorted_sells = list(map(list, sorted(sell_infos, key=lambda x: x[0])))
            yield sorted_buys, sorted_sells, stock
