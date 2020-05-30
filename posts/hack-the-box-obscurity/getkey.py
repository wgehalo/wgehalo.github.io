with open("passwordreminder.txt", "r") as e_in:
    with open("out.txt", "r") as u_in:
        enc = e_in.read()
        unenc = u_in.read()
        key = ""
        for x in range(len(unenc)):
            e = ord(enc[x])
            u = ord(unenc[x])
            if e > u:
                key += chr(e - u)
            else:
                key += chr(255 + e - u)

        print(key)
