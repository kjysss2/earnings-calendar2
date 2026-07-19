#!/usr/bin/env python3
"""Write the photo-based Korean provisional earnings calendar."""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(ROOT, "data", "calendar.json")

START_DATE = "2026-07-16"
END_DATE = "2026-08-14"
PHOTO_UPDATED = "2026-07-19 기준 (기존 이미지 + 삼성전자·SK하이닉스 공식 IR 일정 반영)"

PHOTO_SCHEDULE = {
    "2026-07-22": [
        "LG디스플레이",
        "OCI홀딩스",
        "OCI",
        "유니드",
        "제주은행",
    ],
    "2026-07-23": [
        "삼성E&A",
        "삼성바이오로직스",
        "두산밥캣",
        "KB금융",
        "신한지주",
    ],
    "2026-07-24": [
        "삼성중공업",
        "삼성에피스홀딩스",
        "현대로템",
        "현대제철",
        "현대모비스",
        "LX세미콘",
        "제일기획",
    ],
    "2026-07-27": [
        "LG이노텍",
        "한화오션",
        "HD현대마린솔루션",
        "HDC랩스",
    ],
    "2026-07-28": [
        "한미사이언스",
        "한미약품",
    ],
    "2026-07-29": [
        "SK하이닉스",
        "HD한국조선해양",
        "GS건설",
        "한화솔루션",
        "크래프톤",
        "넥센타이어",
    ],
    "2026-07-30": [
        "삼성전자",
        "삼성전기",
        "POSCO홀딩스",
        "LG에너지솔루션",
        "삼성SDI",
        "SK아이이테크놀로지",
        "삼성에스디에스",
        "케이뱅크",
    ],
    "2026-07-31": [
        "LG화학",
        "에코프로비엠",
        "한온시스템",
        "현대건설",
        "한화에어로스페이스",
        "LG씨엔에스",
    ],
    "2026-08-04": [
        "에코프로",
        "에코프로머티",
        "에코프로에이치엔",
    ],
    "2026-08-05": [
        "카카오뱅크",
    ],
    "2026-08-06": [
        "LG유플러스",
        "CJ ENM",
        "스튜디오드래곤",
    ],
    "2026-08-07": [
        "파마리서치",
    ],
    "2026-08-13": [
        "달바글로벌",
    ],
    "2026-08-14": [
        "삼양식품",
        "피에스케이",
        "피에스케이홀딩스",
        "HPSP",
        "예스티",
        "프로텍",
        "하나마이크론",
        "티에스이",
        "마이크로투나노",
        "두산테스나",
        "LB세미콘",
        "와이씨",
        "유니테스트",
        "인텍플러스",
        "제우스",
        "마이크로컨텍솔",
        "오킨스전자",
        "메가터치",
        "웰덱스",
        "에프에스티",
        "솔브레인",
        "솔브레인홀딩스",
        "KX하이텍",
        "와이씨켐",
        "이엔에프테크놀로지",
        "덕산테코피아",
        "퓨릿",
        "에스에이엠티",
        "유니퀘스트",
        "미코",
        "제주반도체",
        "코리아써키트",
        "이수페타시스",
        "한양디지텍",
        "타이거일렉",
        "덕산하이메탈",
        "인터플렉스",
        "기가비스",
        "삼화콘덴서",
        "아모텍",
        "LS",
        "LS ELECTRIC",
        "LS머트리얼즈",
        "가온전선",
        "비에이치아이",
        "보성파워텍",
        "비나텍",
        "아모센스",
        "서진시스템",
        "한진칼",
        "대웅제약",
        "제닉",
        "STX엔진",
        "세진중공업",
        "아이티센글로벌",
        "이수화학",
        "이수스페셜티케미컬",
        "현대해상",
    ],
}

# 아래 두 종목은 hl=True로 설정되어 빨간색으로 표시됩니다.
SPECIAL_ENTRIES = {
    "SK하이닉스": {
        "ticker": "000660",
        "market": "KOSPI",
        "detail": "오전 9시",
        "hl": True,
    },
    "삼성전자": {
        "ticker": "005930",
        "market": "KOSPI",
        "detail": "오전 10시",
        "hl": True,
    },
}


def make_entry(date, name):
    entry = {
        "date": date,
        "session": "tba",
        "name": name,
    }

    special = SPECIAL_ENTRIES.get(name)

    if special:
        entry.update(special)

    return entry


def build_calendar():
    entries = [
        make_entry(date, name)
        for date, names in PHOTO_SCHEDULE.items()
        for name in names
    ]

    return {
        "title": "한국 잠정실적발표 일정(변동 가능)",
        "source": (
            "사용자 제공 잠정실적발표 일정 이미지 "
            "+ 삼성전자·SK하이닉스 공식 IR"
        ),
        "updated": PHOTO_UPDATED,
        "startDate": START_DATE,
        "endDate": END_DATE,
        "entries": entries,
    }


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )
        file.write("\n")


def main():
    calendar = build_calendar()

    write_json(
        OUTPUT_FILE,
        calendar,
    )

    print(f"Updated {OUTPUT_FILE}")
    print(f"Entries: {len(calendar['entries'])}")
    print(
        f"Range: "
        f"{calendar['startDate']} ~ "
        f"{calendar['endDate']}"
    )


if __name__ == "__main__":
    main()
