def countdown(n):
    while n > 0:
        yield n  # Pauses and returns the current value of n
        n -= 1  # Resumes from here when next() is called

# Create the generator object
counter = countdown(5)

# Iterating through the generator
for value in counter:
    print(value)
