numday = int(input("How many day's temperature? "))

templist = []
total = 0
for day in range(1,numday+1):
    nextDay = int(input("Day " + str(day) +"'s high temp:"))
    total += nextDay
    templist.append(nextDay)

avg =  round(total/numday,2)
print("\nAverage = " + str(avg))

above = 0
for i in templist:
    if i > avg:
        above += 1

print(str(above) + "days above average")