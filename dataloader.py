import requests, base58, time, zipfile


class COMPETITION_NAME:
    UPDOWN = "UPDOWN"
    NEUTRAL = "NEUTRAL"


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
    url = 'https://rpc.ankr.com/polygon_mumbai'
    payload = {"jsonrpc": "2.0", "method": "eth_call", "params": params, "id": 1}
    headers = {"Content-Type": "application/json"}
    r = requests.post(url,
                      headers=headers,
                      json=payload)
    return r.json()['result']


def get_competition_address(competition_name = 'ROCKET'):
    registry = '0x98cEa95085397F45007bC5F1A1B859F8E87bD6C3'
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


def get_from_ipfs(hash_id, challenge, gateway, unlimited_search=False, verbose = False):
    filename = 'challenge_{}_dataset.zip'.format(challenge)
    request_timeout = 300
    chunk_size = 1024 * 4
    tries_per_gateway = 20
    max_retries = tries_per_gateway
    retries = 0
    downloaded = 0
    mode = 'wb'
    start_time = time.time()
    if gateway[-1] != '/':
        gateway += '/'
    gateway += 'ipfs/'
    print('Retrieving dataset for challenge {}. (Please do not unzip the file until the download is complete.)'.format(challenge))
    print('Download times may take up to several hours. If your download is taking too long, please download the dataset file directly from https://competition.rocketcapital.ai.')
    while True:
        if not unlimited_search:
            if retries >= max_retries:
                break
        try:
            r = requests.get(
            gateway + hash_to_cid(hash_id),
            timeout=request_timeout,
            stream=True,
            headers={'Range':'bytes={}-2147483648'.format(downloaded)}
            )

            assert r.ok, 'Unable to get proper response. Reconnecting..'
            total_size = int(r.headers.get('content-length'))
                
            if downloaded > 0: 
                mode = 'ab'
            else:
                actual_total_size = total_size
            
            with open('{}'.format(filename), mode) as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += chunk_size
                        print(end='\r')
                        pct_progress = downloaded * 100 / actual_total_size
                        elapsed = time.time() - start_time
                        est_time_remaining = int(1.7 * elapsed * actual_total_size / downloaded)
                        hours, mins = est_time_remaining // 3600, est_time_remaining % 3600 // 60 + 1
                        print('Download Progress: {:.3f}% (Estimated time remaining: {} h {} min)'.format(pct_progress, hours, mins), end=' ')

            assert downloaded >= actual_total_size, 'Download halted. Reconnecting..'

            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall()
            except:
                downloaded = 0
                mode = 'wb'
                retries += 1
                print(end='\r')
                print('Retrying download..', end='')
                continue
            print(end='\r')
            print('Download Progress: {:.3f}% (Estimated time remaining: 0 h 0 min)'.format(pct_progress), end=' ')
            print('\nDataset saved and unzipped to "dataset" folder.')
            return filename

        except Exception as e:
            print(end='\r')
            if verbose: print(e)
            retries += 1

    print('Gateway {} is unavailable. Please try again later.'.format(gateway))
    raise Exception('Gateway {} is unavailable. Please try again later.'.format(gateway))


def download_dataset(gateway: str, challenge = None, competition_name=COMPETITION_NAME.UPDOWN, verbose = False):
    competition = get_competition_address(competition_name)
    if challenge is None:
        challenge = get_latest_challenge(competition)
    hash_id = get_dataset_hash(competition, challenge)
    filename = get_from_ipfs(hash_id, challenge, gateway=gateway, unlimited_search=False, verbose=verbose)
    return filename