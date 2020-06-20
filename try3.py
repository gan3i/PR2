class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        l = len(prices)
        if l == 1:
            return 0
        profit = 0
        cur_share = 0
        for i in range(l):
            if not cur_share:
                if i+1 < l and prices[i]<prices[i+1]:
                    cur_share = prices[i]
            else:
                if i+1 <l:
                    if cur_share < prices[i] and prices[i]<prices[i+1]:
                        profit += prices[i] - cur_share 
                        cur_share = 0
                else:
                    if cur_share < prices[i]:
                        profit += prices[i] -cur_share
                        cur_share = 0
        return profit

s = Solution()
print(s.maxProfit([2,1,2,0,1]))

        