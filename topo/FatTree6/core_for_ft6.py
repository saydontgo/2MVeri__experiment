def d2h(d):
    if d > 15:
        return f'{hex(d)[2:]}'
    return f'0{hex(d)[2:]}'

def create_add(sid, hid, src_p, dest_p, f):
    f.write(f"table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.{sid}.{hid}/32 {src_p} => 00:00:0a:00:{d2h(sid)}:{d2h(hid)} {dest_p}\n")


def entry_rule(sid, f):
    hid=1
    sid_start = 1
    sid_last = 4
    for dest_p in range(1,7):
        for sid in range(sid_start,sid_last):
            for hid_tmp in range(hid,hid+3):
                for src_p in range(1,7):
                    if src_p!=dest_p:
                        create_add(sid, hid_tmp, src_p, dest_p, f)
                f.write('\n')
            hid+=3
        f.write('\n')
        sid_start+=3
        sid_last+=3

def main():
    for sid in range(37, 46):
        with open(f'rules/s{sid}-commands.txt', 'w')as f:
            f.write('// entry rules\n')
            entry_rule(sid, f)

main()