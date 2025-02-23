
def d2h(d):
    if d > 15:
        return f'{hex(d)[2:]}'
    return f'0{hex(d)[2:]}'

def create_add(sid, hid, src_p, dest_p, f):
    f.write(f"table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.{sid}.{hid}/32 {src_p} => 00:00:0a:00:{d2h(sid)}:{d2h(hid)} {dest_p}\n")

def entry_rule(sid, f):
    hid = (sid - 1)*3 + 1
    for i in range(1,4):
        for j in range(1,7):
            if i!=j:
                create_add(sid, hid, j, i, f)
        f.write('\n')
        hid+=1

def output_rule(sid, f):
    for i in range(1,4):
        hid=0
        for j in range(1,19):
            if j==sid:
                for k in range(1,4):
                    hid+=1
                    create_add(j, hid, i, k, f)
                continue
            for k in range(4,7):
                hid+=1
                create_add(j, hid, i, k, f)
        f.write('\n')

def main():
    for i in range(1,19):
        with open(f"rules/s{i}-commands.txt", "w") as f:
            f.write('// entry rules\n\n')
            entry_rule(i, f)
            f.write('\n\n\n\n\n\n')
            f.write('// output rules\n\n')
            output_rule(i, f)

main()