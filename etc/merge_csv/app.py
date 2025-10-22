# app_cli.py
import sys
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="여러 CSV 파일을 병합하는 스크립트입니다.\n아래 옵션을 참고하세요.",
        epilog="예시: python app_cli.py -f ./data/data1.csv ./data/data2.csv -o ./result/result.csv (옵션)-s timeStamp"
    )

    parser.add_argument(
        "-f", "--files",
        nargs="+",
        required=True,
        help="(필수) 병합할 CSV 파일 목록을 공백으로 구분하여 입력하세요."
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="(필수) 결과 CSV 파일의 저장 경로를 지정하세요."
    )

    parser.add_argument(
        "-s", "--sort",
        default="timeStamp",
        help="(선택) 정렬 기준 컬럼명 (미입력 시 기본값: timeStamp)"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        print("\n//error// CSV 파일 목록(-f)과 결과 파일(-o)을 지정해야 합니다.")
        sys.exit(1)

    args = parser.parse_args()

    # 파일 개수 검증
    if len(args.files) < 2:
        print("//error// 최소 2개의 CSV 파일을 입력해야 합니다. 예: -f a.csv b.csv -o result.csv")
        sys.exit(1)

    # CSV 병합
    dfs = []
    for file in args.files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"//error// {file} 읽는 중 오류 발생: {e}")

    if not dfs:
        print("//error// 병합할 데이터가 없습니다.")
        sys.exit(1)

    df_all = pd.concat(dfs, ignore_index=True)

    # 정렬
    if args.sort in df_all.columns:
        df_all = df_all.sort_values(args.sort)
    else:
        print(f"//pass// 정렬 컬럼 '{args.sort}' 이(가) 존재하지 않습니다. 정렬을 건너뜁니다.")

    # 저장
    df_all.to_csv(args.output, index=False)
    print(f"//complete// 병합 완료: {args.output} 에 저장됨")

if __name__ == "__main__":
    main()
