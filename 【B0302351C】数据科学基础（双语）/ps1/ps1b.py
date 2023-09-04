###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):

    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    pass
# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    # 初始化一个记录每种重量鸡蛋使用数量的列表
    dp = [0] + [float('inf')] * target_weight
    egg_count = [0] * len(egg_weights)

    # 记录使用每种重量鸡蛋的数量
    used_eggs = [list(egg_count) for _ in range(target_weight + 1)]

    for i in range(1, target_weight + 1):
        for j, egg_weight in enumerate(egg_weights):
            if i >= egg_weight:
                # 如果当前组合使用的鸡蛋数量更少
                if dp[i - egg_weight] + 1 < dp[i]:
                    dp[i] = dp[i - egg_weight] + 1
                    # 更新使用每种重量鸡蛋的数量
                    used_eggs[i] = used_eggs[i - egg_weight].copy()
                    used_eggs[i][j] += 1

    # 返回目标重量时每种重量鸡蛋用了多少个
    return used_eggs[target_weight]


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (2, 5, 8)
    n = 99
    print("Actual output:", dp_make_weight(egg_weights, n))

"""Explain why it would be difficult to use a brute force algorithm to solve this problem if there
were 30 different egg weights. You do not need to implement a brute force algorithm in order to
answer this.

因为用暴力的方法的话，在这里随着问题规模的增大， 会有非常非常多没必要的计算，这些计算极大的增加了代码的复杂度，使得消耗时间增长非常迅速。这里更接近于乘方级别的复杂度。

If you were to implement a greedy algorithm for finding the minimum number of eggs
needed, what would the objective function be? What would the constraints be? What strategy
would your greedy algorithm follow to pick which coins to take? You do not need to implement a
greedy algorithm in order to answer this.

如果用贪心的话，目标为使用最小的数量，因为每一步尽可能用最重的egg，因此每一步尽可能用可以用上的最大重量的egg，每一步的约束为(小于limit-sum(已经取出的金币)，且尽可能大)。实现非常容易，且很容易理解将按照自己的贪心思路进行。

Will a greedy algorithm always return the optimal solution to this problem? Explain why it is
optimal or give an example of when it will not return the optimal solution. Again, you do not need
to implement a greedy algorithm in order to answer this

贪心算法不一定有最优解，例如：三种eggs: 11 1 5 ,如果目标为15，则贪心返回11 1 1 1 ，实际最优解为5 5 5 . 因此贪心不一定有最优解
"""