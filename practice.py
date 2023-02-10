def format_number(num):
    int(num)
    x ="{:,}".format(abs(num))
    return str(x)

print(format_number())
print(format_number(-1000000000))



