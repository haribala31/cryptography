import math
n = math.factorial(25)
power_of_2 = math.log2(n)
print("=== PLAYFAIR CIPHER KEYSPACE SIZE ===")
print(f"Total possible keys (25!) = {n:e}")
print(f"Approximate power of 2 = 2^{power_of_2:.2f}")
