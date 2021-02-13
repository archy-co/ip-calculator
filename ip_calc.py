'''
IP Calc
https://github.com/archy-co/lab2_task1https://github.com/archy-co/lab2_task1
'''

def get_ip_from_raw_address(raw_address):
    '''
    Returns ip address from raw_address
    >>> get_ip_from_raw_address('192.127.255.10/32')
    '192.127.255.10'
    '''
    return raw_address.split('/')[0]


def get_network_address_from_raw_address(raw_address):
    '''
    Returns network address from raw_address
    >>> get_network_address_from_raw_address('91.124.230.205/30')
    '91.124.230.204'
    '''
    binary_ip = to_binary_ip_address(get_ip_from_raw_address(raw_address))
    binary_mask = get_binary_mask_from_raw_address(raw_address)
    binary_network_address = ''
    for i in range(len(binary_mask)):
        if binary_ip[i] != '.':
            binary_network_address += str(int(int(binary_ip[i]) and int(binary_mask[i])))
        else: binary_network_address += '.'

    return to_decimal_ip_address(binary_network_address)


def to_decimal_ip_address(binary_ip):
    '''
    Transforms binary interpretation of ip into decimal interpretation
    '''
    ip_n, ip_dec_parts = binary_ip.split('.'), []
    for part in ip_n:
        ip_dec_parts.append(str(int(part, 2)))

    return '.'.join(ip_dec_parts)


def get_broadcast_address_from_raw_address(raw_address):
    '''
    Returns broadcast address
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    '91.124.230.207'
    '''
    binary_ip = to_binary_ip_address(get_ip_from_raw_address(raw_address))
    binary_mask = get_binary_mask_from_raw_address(raw_address)
    binary_network_address = ''
    for i in range(len(binary_mask)):
        if binary_ip[i] != '.':
            binary_network_address += str(int(int(binary_ip[i]) or not int(binary_mask[i])))
        else: binary_network_address += '.'

    return to_decimal_ip_address(binary_network_address)


def get_binary_mask_from_raw_address(raw_address):
    '''
    Returns binary interpretation of mask from raw_address

    >>> get_binary_mask_from_raw_address('91.124.230.205/30')
    '11111111.11111111.11111111.11111100'
    >>> get_binary_mask_from_raw_address('91.124.230.205/4')
    '11110000.00000000.00000000.00000000'
    '''
    mask_n = int(raw_address.split('/')[1])
    mask_parts_lst = []
    for _ in range(mask_n//8):
        mask_parts_lst.append('11111111')

    if len(mask_parts_lst)*8 < mask_n:
        part = '1'*(mask_n-len(mask_parts_lst)*8)
        part += '0'*(8-len(part))
        mask_parts_lst.append(part)

    while len(mask_parts_lst) != 4:
        mask_parts_lst.append('00000000')

    return '.'.join(mask_parts_lst)


def get_first_usable_ip_address_from_raw_address(raw_address):
    '''
    Returns first usable ip address
    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    '''
    binary_ip = to_binary_ip_address(get_network_address_from_raw_address(raw_address))[:-1] + '1'
    return to_decimal_ip_address(binary_ip)


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    '''
    Returns penultimate usable ip
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    '''
    splited_ip = get_broadcast_address_from_raw_address(raw_address).split('.')
    for i in range(len(splited_ip)-1, -1, -1):
        if int(splited_ip[i]) > 1:
            splited_ip[i] = str(int(splited_ip[i])-2)
            break

    return '.'.join(splited_ip)


def get_number_of_usable_hosts_from_raw_address(raw_address):
    '''
    Returns number of usable hosts
    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/30')
    2
    '''
    return 2**(32-int(raw_address.split('/')[1]))-2


def get_ip_class_from_raw_address(raw_address):
    '''
    Returns ip class as capital latin letter
    >>> get_ip_class_from_raw_address('173.199.231.74')
    'B'
    '''
    if int(raw_address.split('.')[0]) <= 127:
        return 'A'

    if 128 <= int(raw_address.split('.')[0]) <= 191:
        return 'B'

    if 192 <= int(raw_address.split('.')[0]) <= 223:
        return 'C'

    if 224 <= int(raw_address.split('.')[0]) <= 239:
        return 'D'

    return 'E'


def to_binary(num: int) -> str:
    '''
    Transfroms num to binary number length 8
    '''
    bin_num = bin(num).split('b')[1]
    while len(bin_num) < 8:
        bin_num = '0' + bin_num

    return bin_num


def to_binary_ip_address(ip_address):
    '''
    Transforms decimal interpretation of ip into binary interpretation
    '''
    ipa_blocks, bin_ip_blocks = ip_address.split('.'), []
    for ipa_block in ipa_blocks:
        bin_ip_blocks.append(to_binary(int(ipa_block)))

    return '.'.join(bin_ip_blocks)


def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    '''
    Checks if ip address is private
    >>> check_private_ip_address_from_raw_address('10.12.14.174/24')
    True
    >>> check_private_ip_address_from_raw_address('172.31.15.241/11')
    True
    >>> check_private_ip_address_from_raw_address('172.32.147.93/31')
    False
    '''
    ip_address = get_ip_from_raw_address(raw_address)
    if (ip_address.split('.')[0] == '10') or\
       (ip_address.split('.')[0] == '172' and ip_address.split('.')[1] in ['16', '31']) or\
       (ip_address.split('.')[0] == '192' and ip_address.split('.')[1] == '168'):
        return True
    return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(get_number_of_usable_hosts_from_raw_address("192.168.10.10/16"))
    print(get_number_of_usable_hosts_from_raw_address("230.250.33.233/13"))

