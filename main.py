import os
import shutil
import yaml

from datetime import datetime


# 설정 파일 불러오기 함수
def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)



#설정 로드
config = load_config()
#폴더
KAKAO_FOLDER = config["target_folder"]
#정리 기준
FILE_TYPES = config["file_types"]
#기본
DEFAULT_FOLDER = "기타"



    
def get_file_list(folder_path):
    """지정 폴더 내 모든 파일 목록 반환"""
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def classify_file(file_name, file_types):
    """파일 확장자 기반으로 폴더명 반환"""
    ext = os.path.splitext(file_name)[1].lower()
    for folder, ext_list in file_types.items():
        if ext in ext_list:
            return folder
    return DEFAULT_FOLDER

def get_modified_date(file_path):
    """파일 수정일 기반으로 날짜 문자열 반환 (YYYY-MM-DD)"""
    mod_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")

def move_file(file_path, dest_folder):
    """파일을 지정된 폴더로 이동"""
    os.makedirs(dest_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))

def save_log_to_file(log_data):
    """로그 생성"""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(log_dir, f"{today}.log")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 실행 ===\n")
        for file, folder in log_data:
            f.write(f"{file} → {folder}\n")
    

def run_sorting(base_path, file_types, sort_by_date=False):
    """파일 정리 메인 로직"""
    if not os.path.exists(base_path):
        return "경로가 존재하지 않습니다."

    files = get_file_list(base_path)
    moved_log = []

    for file in files:
        full_path = os.path.join(base_path, file)
        category = classify_file(file, file_types)
        target_folder = os.path.join(base_path, category)

        if sort_by_date:
            date_folder = get_modified_date(full_path)
            target_folder = os.path.join(target_folder, date_folder)

        move_file(full_path, target_folder)
        moved_log.append((file, os.path.relpath(target_folder, base_path)))

    return moved_log



# 실행 (날짜별 정리 포함)
#메인
if __name__ == "__main__":
    result = run_sorting(KAKAO_FOLDER, FILE_TYPES, sort_by_date=True)

    if isinstance(result, str):
        print(f"오류발생 : {result}")
    else:
        print("정리결과")
        for file, folder in result:
            print(f" - {file} → {folder}")
        save_log_to_file(result)
            
