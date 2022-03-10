import json

class Sort:

    def __init__(self, orderbooks, exchanges):
        self.orderbooks = orderbooks
        self.exchanges = exchanges

    def executeTrade(self, algo_type = "single"):
        """
        Args:
            algo_type (str, optional): Algorithm type for matching. single or multiple. Defaults to "single".
        """
        matched = {}
        threshold = 0.9

        # buy price should be maximum and sell price should be minimum and price differences between buy and sell cannot be more than threshold
        for sorted_buys, sorted_sells, stock in self.exchanges.sorting_orders():
            for i in range(len(sorted_buys)):
                for j in range(len(sorted_sells)):
                    if 0 <= sorted_buys[i][0] - sorted_sells[j][0] <= threshold and sorted_sells[i][2] != "Fully Filled" and sorted_buys[i][2] != "Fully Filled":
                        # take matched buys and sells to a dictionary - works for multiple and single matching
                        if stock in matched.keys():
                            matched[stock].append([sorted_buys[i][0], sorted_sells[i][0], min(sorted_buys[i][1], sorted_sells[i][1]),
                                                    self.exchanges.fee_ladder(sorted_buys[i][1], min(sorted_buys[i][1], sorted_sells[i][1]))])
                        else:
                            matched[stock] = [[sorted_buys[i][0], sorted_sells[i][0], min(sorted_buys[i][1], sorted_sells[i][1]),
                                                    self.exchanges.fee_ladder(sorted_buys[i][1], min(sorted_buys[i][1], sorted_sells[i][1]))]]     

                        # if more buy quantities than sell quantities
                        if sorted_buys[i][1] > sorted_sells[i][1]:
                            sorted_buys[i][1] = sorted_buys[i][1] - sorted_sells[i][1]
                            sorted_sells[i][1] = 0
                            sorted_buys[i][2] = "Partially Filled"
                            sorted_sells[i][2] = "Fully Filled"
                        # if more sell quantities than buy quantities
                        elif sorted_buys[i][1] < sorted_sells[i][1]:
                            sorted_sells[i][1] = sorted_sells[i][1] - sorted_buys[i][1]
                            sorted_buys[i][1] = 0
                            sorted_sells[i][2] = "Partially Filled"
                            sorted_buys[i][2] = "Fully Filled"
                        else: # if both same
                            sorted_sells[i][1] = 0
                            sorted_buys[i][1] = 0
                            sorted_sells[i][2] = "Fully Filled"
                            sorted_buys[i][2] = "Fully Filled"

                        # if single match is desired and if there is a match:
                        if algo_type == "single":
                            break
                # if single match and there is a stock matched:
                if algo_type == "single" and stock in matched.keys():
                    break


            # update buy and sell orders of the order books according to sorted and altered results
            self.orderbooks.buy_order[stock]["price"], self.orderbooks.buy_order[stock]["quantity"], self.orderbooks.buy_order[stock]["status"], self.orderbooks.buy_order[stock]["username"] = list(map(list, zip(*sorted_buys)))
            self.orderbooks.sell_order[stock]["price"], self.orderbooks.sell_order[stock]["quantity"], self.orderbooks.sell_order[stock]["status"], self.orderbooks.sell_order[stock]["username"] = list(map(list, zip(*sorted_sells)))
        
        self.exchanges.update(matched)

        #write udated orders to json files
        with open("buy_orders.json","w") as f:
            json.dump(self.orderbooks.buy_order, f, indent=4)

        with open("sell_orders.json","w") as f:
            json.dump(self.orderbooks.sell_order, f, indent=4)