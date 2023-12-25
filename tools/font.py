
with open("fonts.txt", "r") as fp:
    with open("fonts_output.txt", "w") as op:
        i = 0
        while True:
            c = fp.read(1)
            if ("" == c):
                break;
            op.write(hex(ord(c)))
            op.write(',\r\n')
