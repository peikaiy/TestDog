class Solution:
    def reverse(self, x: int) -> int:
        if x >= 0:

            reversed_x = int(str(x)[::-1])
        else:
            reversed_x = -int(str(x)[:0:-1])
        return reversed_x

a = Solution()
x = 1230
s = str(x)
b = int(s)
print(s)
print(b)
print(type(b))
