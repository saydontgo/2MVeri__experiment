prime_table=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,103,
107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]

def main():
    for sid in range(19,37):
        with open(f'rules/s{sid}-commands.txt', 'a')as f:
            f.write('\n\n// Phase 1: consistency verification\n')
            f.write(f'table_set_default MyEgress.tbl_bf add_bf {sid}\n')
            f.write(f'table_set_default MyEgress.tbl_prime prime_multiply {prime_table[sid-1]}\n')
            f.write(f'// Phase 2: inconsistency location\n')
            f.write(f'table_set_default MyEgress.swtrace add_swtrace {sid}\n')

main()