# tx
import time
import serial

ser = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 상태 딕셔너리
status = {
    "parachute": "Not yet deploy",  # 예시 데이터, Not yet deploy:사출 전, Deploy:사출 후, Force Deploy:강제 사출 후
    "way": "",  # 예시 데이터, UP:상승시, DOWN(3):하강시 괄호 안은 카운트
    "gps": "",  # 예시 데이터, 212, 222: 위도, 경도
    "ebimu": "",  # 예시 데이터, 120,512,252: x,y,z
    "bmp": "",  # 예시 데이터,  50: 고도
    "bno": ""  # 예시 데이터, 20,60,90: 오일러 각도
}

while True:

    # 낙하산 사출 코드 내부
    status["parachute"] = "Deploy"
    # 방향 탐지 코드 내부
    status["way"] = "UP"
    # gps 상태확인 로직
    la = 0
    lo = 0
    datas = [la, lo]
    status["gps"] = ",".join(map(str, datas))
    # ebimu 상태확인 로직
    datas = [x, y, z]
    status["ebimu"] = ",".join(map(str, datas))
    # bmp 상태확인 로직
    status["bmp"] = str(altitude)
    # bno 상태확인 로직
    datas = [roll, pitch, yaw]
    status["bno"] = ",".join(map(str, datas))

    # 강제 사출 확인 로직
    if ser.in_waiting > 0:
        read_data = ser.read().decode()
    if read_data == "E":
        # 강제 사출 로직
        status["parachute"] = "Force Deploy"
        print("Ejection!!")

# 딕셔너리값 리스트화
status_values = list(status.values())
total_message = "/".join(map(str, status_values)) + ";"
for i in range(0, len(total_message), 55):
    message = total_message[i:i + 55]
    ser.write(message.encode())
print("OK")
time.sleep(0.5)