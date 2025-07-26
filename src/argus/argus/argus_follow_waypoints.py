#!/usr/bin/env python3

# Copyright 2022 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

# 목표 : 원하는 구역 설정 시에 해당 경로로 이동하는 모듈 구현 -> 이거 테스트 해보고 이것을 함수로 만들고 
# 모듈화 하고 그것들을 연결해서 클래스로 생성해서 spin으로 blocking을 통해 node를 구현
# 사용자가 선택할 번호 5개이며 service를 통해 전달 받음
# 0 => hollway
# 1 => A-1
# 2 => A-2
# 3 => B-1
# 4 => B-2

#경유지 도착 시 바라보는 방향 설정
    # NORTH = 0 -> 이거 사용
    # NORTH_WEST = 45 
    # WEST = 90 -> 이거 사용
    # SOUTH_WEST = 135
    # SOUTH = 180 -> 이거 사용
    # SOUTH_EAST = 225
    # EAST = 270 -> 이거 사용 
    # NORTH_EAST = 315
import rclpy

from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator



# Set goal poses
def rotation360(userSelectValue, navigator): # 매개 변수로 사용자가 탐색 구역 선정
    # 0~4 사이의 값이 아니면 오류 발생하니 제한을 두자 재요청 또는 예외처리 하지만 ui를 통해서 선택할거라 괜찮을 듯하다.
    # 전송과정에서 노이즈가 발생해서 이상한 값이 들어오지 않는 이상...
    # 방향 회전 enum 값을 담은 리스트
    direction_rotationV = [TurtleBot4Directions.NORTH, TurtleBot4Directions.WEST,TurtleBot4Directions.SOUTH,TurtleBot4Directions.EAST]
    goal_pose = []
    section_list = {0 : [[-1.3686145544052124,-0.02707694284617901],[-2.8475544452667236,0.022672483697533607],[0.0,0.0]], # hallway
                    1 : [[-1.3166851997375488,-0.62477046251297],[-0.2772611677646637,-0.866601288318634],[0.0,0.0]], # A-1
                    2: [[-1.3166851997375488,-0.62477046251297],[-0.2772611677646637,-0.866601288318634],[-0.3072705864906311,-1.8993831872940063],[0.0,0.0]],
                    3: [[-1.3686145544052124,-0.02707694284617901],[-2.8475544452667236,0.022672483697533607],[-2.6845288276672363,-0.7209501266479492],[0.0,0.0]], 
                    4: [[-1.3686145544052124,-0.02707694284617901],[-2.8475544452667236,0.022672483697533607],[-2.6845288276672363,-0.7209501266479492],[-2.6721067428588867,-1.8574532270431519],[0.0,0.0]]} # float형태로 좌표를 넘겨야함
    
    if userSelectValue not in section_list:
        raise ValueError(f"Invalid section index: {userSelectValue}")
    
    for i in (section_list[userSelectValue] -1): # i를 통해 구역마다 이동할 경유지 좌표가 담김
        for j in direction_rotationV: # j를 통해 방향 값 뽑아옴
            goal_pose.append(navigator.getPoseStamped(i, j))
    return goal_pose

def main():
    rclpy.init()

    navigator = TurtleBot4Navigator(namespace='robot6') # nav2에게 좌표 값을 주기 위해 객체 생성 이객체 안에 함수들을 통해 경유지 전송
    # 우린 도킹에서 시작하기 때문에  Start on dock이 필요 없음
    # Start on dock
    if not navigator.getDockedStatus():
        navigator.info('Docking before intialising pose')
        navigator.dock()

    # Set initial pose
    initial_pose = navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH) # 실제 rviz의 북쪽이 내가 원하는 방향인지 체크해야함
    # navigator.clearAllCostmaps() # map 불러왔을떄 초기 화면으로 세팅
    navigator.setInitialPose(initial_pose) # map 불러왔을떄 초기 위치 세팅
    navigator.waitUntilNav2Active() # Wait for Nav2 -> Nav2가 동작할때까지 기다리는 함수
    
    navigator.undock() # 도킹 해제
    userSelectValue = int(input("0~4사이의 값을 입력하세요.")) # 여기에 서비스로 받은 구역 설정 응답 값이 세팅됨 -> 임시로 0~4 구역 선택했다 가정
    # Follow Waypoints
    navigator.startFollowWaypoints(rotation360(userSelectValue, navigator)) # 경유지 Nav2에게 넘겨서 세팅

    # navigator.cancelTask() # waypoint canceled
    # Finished navigating, dock
    navigator.dock() # 도킹하며 마무리
    # 끝났다는 알림
    rclpy.shutdown()


if __name__ == '__main__':
    main()
