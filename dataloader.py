import requests, base58, time

GATEWAYS = [
            'https://cloudflare-ipfs.com/ipfs/',
            'https://gateway.pinata.cloud/ipfs/',
            'https://gateway.ipfs.io/ipfs/',
            'https://ipfs.io/ipfs/',
            'https://ipfs.cf-ipfs.com/ipfs/',
            'https://ipfs.fleek.co/ipfs/',
            'https://cf-ipfs.com/ipfs/',
            'https://bluelight.link/ipfs/',
            'https://dweb.link/ipfs/'
            ]

def encode_string(param, fn_id='0x5d58ebc1'):
    line2 = '0' * 62 + '20'
    line3 = hex(len(param))[2:]
    line3 = '0' * (64 - len(line3)) + line3
    param_line = ''
    for i in range(0, len(param), 32):
        chunk = param[i:i + 32]
        utf8_encoded = chunk.encode('utf-8').hex()
        padding = '0' * (64 - len(utf8_encoded))
        param_line += utf8_encoded + padding
    return fn_id + line2 + line3 + param_line

def network_read(params):
    url = 'https://rpc-mainnet.matic.quiknode.pro'
    payload = {"jsonrpc": "2.0", "method": "eth_call", "params": params, "id": 1}
    headers = {"Content-Type": "application/json"}
    r = requests.post(url,
                      headers=headers,
                      json=payload)
    return r.json()['result']

def get_competition_address(competition_name = 'ROCKET'):
    registry = '0x0Ee5AFF42564C0D293164b39D85653666ae151Eb'
    data = encode_string(competition_name)
    params = [{'to': registry,
               'data': data},
              'latest']
    return '0x{}'.format(network_read(params)[-40:])

def get_latest_challenge(competition):
    fn_id = '0x736d8c91'
    params = [{'to': competition,
               'data': fn_id},
              'latest']
    return int(network_read(params), 16)

def get_dataset_hash(competition, challenge=None):
    fn_id = '0x39e28777'
    if challenge is None:
        challenge = get_latest_challenge(competition)
    encoded_challenge = hex(challenge)[2:]
    encoded_challenge = '0' * (64-len(encoded_challenge)) + encoded_challenge
    data = fn_id + encoded_challenge
    params = [{'to': competition,
               'data': data},
              'latest']
    return network_read(params)

def hash_to_cid(hash_id):
    if hash_id[:2] == '0x': hash_id = hash_id[2:]
    hash_id = '1220' + str(hash_id)
    hash_id = int(hash_id, 16)
    return base58.b58encode_int(hash_id).decode('utf-8')

def get_from_ipfs(hash_id, challenge, gateways, verbose = True):
    filename = 'challenge_{}_dataset.zip'.format(challenge)
    base_timeout=15
    timeout = base_timeout
    chunk_size = 4096
    gateway_length = len(gateways)
    max_retries = gateway_length * 3
    retries = 0
    gateway_index = 0
    no_redirects = '#x-ipfs-companion-no-redirect'
    if verbose: 
        print('Retrieving dataset for challenge {}..'.format(challenge))
        print('(Please do not unzip the file until the download is complete.)')
    while retries < max_retries:
        try:
            gateway = gateways[gateway_index]
            r = requests.get(
            gateway + hash_to_cid(hash_id) + no_redirects,
            timeout=1,stream=True)
            with open('{}'.format(filename), 'wb') as f:
                start_time = time.time()
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                    if time.time() - start_time > timeout:
                        raise Exception('Request timeout.')

            if verbose: print('Dataset saved to {}'.format(filename))
            return filename
        except:
            retries += 1
            gateway_index = (gateway_index + 1) % gateway_length
            timeout = (1 + (retries // gateway_length)) * base_timeout
    
    print('Gateways unavailable. Please try again later.')
    raise Exception('Gateways unavailable. Please try again later.')
    

def download_dataset(challenge = None, competition_name = 'ROCKET', verbose = True):
    competition = get_competition_address(competition_name)
    if challenge is None:
        challenge = get_latest_challenge(competition)
    hash_id = get_dataset_hash(competition, challenge)
    filename = get_from_ipfs(hash_id, challenge, gateways=GATEWAYS, verbose=True)
    return filename