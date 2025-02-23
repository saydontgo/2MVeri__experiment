def d2h(d):
    if d > 15:
        return f'{hex(d)[2:]}'
    return f'0{hex(d)[2:]}'

def create_add(sid, hid, src_p, dest_p, f):
    f.write(f"table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.{sid}.{hid}/32 {src_p} => 00:00:0a:00:{d2h(sid)}:{d2h(hid)} {dest_p}\n")

def entry_rule(sid, f):
    lsid_start = (sid - 19)//3 * 3 + 1
    for lsid in range(lsid_start, lsid_start + 3):
        hid_start = (lsid - 1)*3 + 1
        for hid in range(hid_start, hid_start+3):
            dest_p = lsid - lsid_start + 1
            for i in range(1,7):
                if i == dest_p:
                    continue
                create_add(lsid, hid, i, dest_p, f)
            f.write('\n')
        f.write('\n\n')

def output_rule(sid, f):
    lsid_start = (sid - 19)//3 * 3+ 1
    for i in range(1,4):
        hid=0
        dest_p=1
        for j in range(1,19):
            if lsid_start + 3>j>=lsid_start:
                for k in range(0,3):
                    hid+=1
                    create_add(j, hid, i, dest_p, f)
                dest_p+=1
            else:
                for k in range(4,7):
                    hid+=1
                    create_add(j, hid, i, k, f)
        f.write('\n')

def main():
    for sid in range(19, 37):
        with open(f'rules/s{sid}-commands.txt', 'w')as f:
            f.write('// entry rules\n')
            entry_rule(sid, f)
            f.write('\n\n\n\n')
            f.write('// output rules\n')
            output_rule(sid, f)

main()