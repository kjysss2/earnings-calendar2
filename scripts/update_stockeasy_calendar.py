#!/usr/bin/env python3
"""2026년 2분기 한국 실적발표 캘린더 JSON 생성."""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_FILE = os.path.join(
    ROOT,
    "data",
    "calendar.json",
)

START_DATE = "2026-07-16"
END_DATE = "2026-08-14"


# ============================================================
# 실적발표 일정
#
# 기존 잠정 일정을 유지했습니다.
#
# 단, OCI홀딩스는 공식 기업설명회 공시에 따라
# 2026년 7월 23일로 수정했습니다.
# ============================================================

SCHEDULE = {
    "2026-07-22": [
        "LG디스플레이",
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
        "OCI홀딩스",
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
        "LG에너지솔루션",
        "삼성전기",
        "POSCO홀딩스",
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


# ============================================================
# 공식 기업설명회 또는 회사 IR 공시에서
# 정확한 개최시각이 확인된 종목
#
# 시각이 없는 종목은 추측하지 않고
# 화면에 "시간 미공개"로 표시합니다.
# ============================================================

CONFIRMED_TIMES = {
    # 7월 22일
    "LG디스플레이": "10:00",
    "OCI": "15:30",

    # 7월 23일
    "신한지주": "14:00",
    "두산밥캣": "15:30",
    "OCI홀딩스": "15:30",
    "KB금융": "16:00",

    # 7월 24일
    "현대모비스": "10:10",
    "LX세미콘": "11:00",
    "삼성중공업": "16:00",

    # 7월 29일
    "SK하이닉스": "09:00",
    "넥센타이어": "15:30",

    # 7월 30일
    "삼성전자": "10:00",
    "LG에너지솔루션": "10:00",
    "삼성전기": "13:30",
    "POSCO홀딩스": "15:00",
    "SK아이이테크놀로지": "16:00",
    "케이뱅크": "16:00",

    # 7월 31일
    "LG씨엔에스": "10:30",
    "LG화학": "14:00",

    # 8월 5일
    "카카오뱅크": "10:00",

    # 8월 6일
    "CJ ENM": "14:00",
    "스튜디오드래곤": "14:00",
}


# ============================================================
# 종목코드 및 시장 정보
#
# 필요한 종목부터 넣어두었습니다.
# 없는 기업은 회사명과 시간만 표시됩니다.
# ============================================================

COMPANY_META = {
    "LG디스플레이": {
        "ticker": "034220",
        "market": "KOSPI",
    },

    "OCI": {
        "ticker": "456040",
        "market": "KOSPI",
    },

    "OCI홀딩스": {
        "ticker": "010060",
        "market": "KOSPI",
    },

    "두산밥캣": {
        "ticker": "241560",
        "market": "KOSPI",
    },

    "KB금융": {
        "ticker": "105560",
        "market": "KOSPI",
    },

    "신한지주": {
        "ticker": "055550",
        "market": "KOSPI",
    },

    "삼성중공업": {
        "ticker": "010140",
        "market": "KOSPI",
    },

    "현대모비스": {
        "ticker": "012330",
        "market": "KOSPI",
    },

    "LX세미콘": {
        "ticker": "108320",
        "market": "KOSPI",
    },

    "SK하이닉스": {
        "ticker": "000660",
        "market": "KOSPI",
    },

    "넥센타이어": {
        "ticker": "002350",
        "market": "KOSPI",
    },

    "삼성전자": {
        "ticker": "005930",
        "market": "KOSPI",
    },

    "LG에너지솔루션": {
        "ticker": "373220",
        "market": "KOSPI",
    },

    "삼성전기": {
        "ticker": "009150",
        "market": "KOSPI",
    },

    "POSCO홀딩스": {
        "ticker": "005490",
        "market": "KOSPI",
    },

    "SK아이이테크놀로지": {
        "ticker": "361610",
        "market": "KOSPI",
    },

    "케이뱅크": {
        "ticker": "279570",
        "market": "KOSPI",
    },

    "LG화학": {
        "ticker": "051910",
        "market": "KOSPI",
    },

    "LG씨엔에스": {
        "ticker": "064400",
        "market": "KOSPI",
    },

    "카카오뱅크": {
        "ticker": "323410",
        "market": "KOSPI",
    },

    "CJ ENM": {
        "ticker": "035760",
        "market": "KOSDAQ",
    },

    "스튜디오드래곤": {
        "ticker": "253450",
        "market": "KOSDAQ",
    },
}


# ============================================================
# 빨간색으로 강조할 종목
#
# index.html에서 hl=True이면 빨간색으로 표시됩니다.
# ============================================================

HIGHLIGHT_COMPANIES = {
    "SK하이닉스",
    "삼성전자",
}


def format_korean_time(value):
    """
    24시간 형식의 HH:MM을
    오전/오후 형식으로 변환합니다.

    예:
    09:00 -> 오전 9:00
    13:30 -> 오후 1:30
    16:00 -> 오후 4:00
    """

    hour, minute = map(
        int,
        value.split(":"),
    )

    if hour < 12:
        period = "오전"
    else:
        period = "오후"

    if hour == 0:
        display_hour = 12
    elif hour > 12:
        display_hour = hour - 12
    else:
        display_hour = hour

    return (
        f"{period} "
        f"{display_hour}:"
        f"{minute:02d}"
    )


def make_entry(date, name):
    """
    캘린더에 들어갈 개별 기업 데이터를 만듭니다.
    """

    entry = {
        "date": date,
        "session": "tba",
        "name": name,
    }

    # 종목코드와 시장 정보 추가
    meta = COMPANY_META.get(name)

    if meta:
        entry.update(meta)

    # 공식 발표시각 추가
    confirmed_time = CONFIRMED_TIMES.get(name)

    if confirmed_time:
        entry["time"] = confirmed_time

        entry["detail"] = (
            f"{format_korean_time(confirmed_time)}"
            " · 공식 확인"
        )

    else:
        entry["detail"] = "시간 미공개"

    # 삼성전자와 SK하이닉스만 빨간색 표시
    if name in HIGHLIGHT_COMPANIES:
        entry["hl"] = True

    return entry


def build_calendar():
    """
    전체 캘린더 데이터를 생성합니다.
    """

    entries = [
        make_entry(
            date,
            name,
        )
        for date, names in SCHEDULE.items()
        for name in names
    ]

    now = datetime.now(
        ZoneInfo("Asia/Seoul")
    )

    return {
        "title": (
            "한국 잠정실적발표 일정"
            "(시간 포함·변동 가능)"
        ),

        "source": (
            "기업 IR·기업설명회 공시 "
            "및 기존 잠정실적 일정"
        ),

        "updated": now.strftime(
            "%Y-%m-%d %H:%M KST"
        ),

        "startDate": START_DATE,
        "endDate": END_DATE,
        "entries": entries,
    }


def write_json(path, data):
    """
    생성한 데이터를 JSON 파일로 저장합니다.
    """

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:
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

    confirmed_count = sum(
        1
        for entry in calendar["entries"]
        if entry.get("time")
    )

    unknown_count = (
        len(calendar["entries"])
        - confirmed_count
    )

    print(
        f"Updated: {OUTPUT_FILE}"
    )

    print(
        f"Entries: "
        f"{len(calendar['entries'])}"
    )

    print(
        f"Confirmed times: "
        f"{confirmed_count}"
    )

    print(
        f"Unknown times: "
        f"{unknown_count}"
    )

    print(
        f"Range: "
        f"{calendar['startDate']} "
        f"~ "
        f"{calendar['endDate']}"
    )


if __name__ == "__main__":
    main()
