import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 네이버 모바일 스포츠 URL
BASE_URL = "https://m.sports.naver.com/player/index"

# 업데이트할 투수 리스트 (선수명, playerId)
pitchers = [
    ("에르난데스", 54119), ("치리노스", 55146), ("손주영", 67143), ("임찬규", 61101),
    ("코엔윈", 55138), ("최채흥", 68419), ("송승기", 51111), ("폰세", 55730),
    ("류현진", 76715), ("문동주", 52701), ("와이스", 54755), ("엄상백", 65056),
    ("데이비슨", 55536), ("박세웅", 64021), ("나균안", 67539), ("박진", 69594),
    ("이민석", 52530), ("김진욱", 51516), ("후라도", 53375), ("원태인", 69446),
    ("최원태", 65320), ("레예스", 54443), ("이승현", 51454), ("앤더슨", 54833),
    ("화이트", 55855), ("문승원", 62869), ("김광현", 77829), ("송영진", 53898),
    ("박종훈", 60841), ("라일리", 55903), ("로건", 55912), ("신민혁", 68902),
    ("최성영", 66920), ("목지훈", 53973), ("김녹원", 52995), ("잭로그", 55239),
    ("박정수", 65639), ("콜어빈", 55257), ("최원준", 67263), ("최승용", 51264),
    ("최준호", 53259), ("김유성", 53262), ("네일", 54640), ("김도현", 69745),
    ("올러", 55633), ("황동하", 52641), ("양현종", 77637), ("윤영철", 53613),
    ("헤이수스", 54354), ("오원석", 50859), ("소형준", 50030), ("고영표", 64001),
    ("쿠에바스", 69032), ("로젠버그", 55322), ("정현우", 55313), ("하영민", 64350),
    ("김선기", 66018), ("김윤하", 54319), ("조영건", 69360), ("김연주", 54368), ("박주성", 69328)
]

def get_record_stats(player_id):
    url = f"{BASE_URL}?playerId={player_id}&category=kbo&tab=record"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        cells = soup.select("ul.record_list li")
        for cell in cells:
            spans = cell.find_all("span")
            if len(spans) >= 7:
                era = spans[3].text.strip()
                whip = spans[6].text.strip()
                return float(era), float(whip)
    except:
        pass
    return None, None

def get_recent_5_era(player_id):
    url = f"{BASE_URL}?playerId={player_id}&category=kbo&tab=game"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        rows = soup.select("ul.record_list > li")
        data = []
        for row in rows:
            spans = row.find_all("span")
            if len(spans) < 9: continue
            ip = spans[5].text.strip()
            er = spans[7].text.strip()
            if not ip or not er: continue
            if "." in ip:
                main, sub = ip.split(".")
                ip_float = int(main) + int(sub)/3
            else:
                ip_float = float(ip)
            data.append((ip_float, float(er)))
            if len(data) == 5:
                break

        total_ip = sum(d[0] for d in data)
        total_er = sum(d[1] for d in data)
        if total_ip == 0:
            return None
        return round((total_er / total_ip) * 9, 2)
    except:
        return None

def update_all():
    result = []
    for name, pid in pitchers:
        print(f"[처리 중] {name} ({pid})")
        era, whip = get_record_stats(pid)
        recent5 = get_recent_5_era(pid)
        result.append({"name": name, "playerId": pid, "ERA": era, "Recent5_ERA": recent5, "WHIP": whip})
        time.sleep(0.5)

    df = pd.DataFrame(result)
    df.to_csv("data/naver_pitcher_stats.csv", index=False)
    print("\n✅ 저장 완료: data/naver_pitcher_stats.csv")

if __name__ == "__main__":
    update_all()
