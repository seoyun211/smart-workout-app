user_data = """user,password
seoyun,tjdbs0191"""

# 파일에 데이터 쓰기
with open("users.txt", "w") as file:
    file.write(user_data)

print("users.txt 파일이 생성되었습니다.")