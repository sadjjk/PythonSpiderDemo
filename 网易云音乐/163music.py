import requests
import execjs

def get_music_file_url(music_id):
    with open('./163music.js', 'r') as f:
        jscode = f.read()

    d = "{\"ids\":\"[" + str(music_id) + "]\",\"level\":\"standard\",\"encodeType\":\"aac\",\"csrf_token\":\"\"}"
    ctx = execjs.compile(jscode).call('d', d)
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    response = requests.post(url, data=ctx, headers=headers).json()
    return response['data'][0]["url"]
if __name__ == '__main__':
    print(get_music_file_url(1956514098))
