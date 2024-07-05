<h1>Kakao E-scooter 🛴 Geocoding Project(킥보드 불법주차 지오코딩) V2</h1> 

<h2>About ℹ️</h2>

Illegal parking of E-scooters is a serious problem in South Korea where there is no significant administrative effort to mitigate the problem(with the exception of the City of Seoul). The plague of E-scooters on walkaways severely impedes pedestrian safety and software limitations such as return area restriction fail to provide a viable solution against illegal parkers who tend to find loopholes in the onboard GPS. 

I first noticed the severity of this problem during my internship in Yongin, a city located within Gyeonggi province in the vicinity of the larger Seoul Metropolitan Area. I saw countless E-scooters just lying about near metro entrances and pedestrian walkaways on my way to work. 

As residents of this city had nowhere but Kakaotalk, a popular messenger application in Korea, to report and move illegally parked E-scooters, I conducted a geospatial analysis of the E-scooters by scaping illegal parking spots from Kakaotalk chat records and geocoding them into mappable x(longitude) and y(latitude) coordinates to identify the major center of complaints and offer measures that would hopefully alleviate pedestrian discomfort associated with E-scooter illegal parking.  

This project was first created with win32gui by referring to this post on velog: https://velog.io/@solarrrrr1010/Python-study-2 but I wanted to start fresh and get some experience with pywinauto, hence the V2 as you see here. 


한국에서 전기킥보드 등의 PM불법주차는 보행자의 통행을 방해하고 도보 사고위험성을 늘리는 문제를 야기하고 있습니다. 

또한 서울 외 지역은 법적 제제방안의 미비로 인해 이에 대한 제대로 된 대응을 전혀 하지 못하고, PM이용자들이 GPS음영지역 등을 이용해 좁은 도보나 횡단보도 앞 등 통행이 많은 지역에 마음대로 불법주차를 할 수 있는것이 현 실태입니다.

용인시청에서 공공빅데이터 인턴을 하면서 출퇴근할때 실제로 도보에 이렇게 불법주차되어 늘어진 킥보드들이 상당수였고 이로 인해 걸려 넘어질 뻔하는 등 위험한 상황이 발생하는 것도 실제로 목격했습니다. 

현재 경기도에서는 카카오톡으로밖에 불법주차 신고 및 이동요구를 할 수밖에 없으므로 카카오톡 채팅 기록에서 주소를 추출하여 시각화할수 있는 위도와 경도로 지오코딩하는 절차를 거쳐 공간분석을 실시했고, 주요 불법주차 발생 지역을 식별하여 업체들이 회수 대기장소를 선정하고 신고에 빠르게 대응할 수 있도록 방안을 마련해보는 빅데이터 인턴 과제를 수행했습니다.

처음에는 https://velog.io/@solarrrrr1010/Python-study-2를 참고하여 win32gui를 사용했으나 pywinauto를 써서 직접 만들어보고자 새롭게 리팩토링해서 V2로 정리하였습니다.

<h2>How to use ▶️</h2>

1. Set path, target window, and keyword appropriately to locate the Kakaotalk chat window. Defaults are given but may differ depending on the system used/city you are residing on
  
3. Set filepath to where you want the chat record to be saved(in txt)
  
5. Open the Kakaotalk program and open the target chat window. The target chat window must be open and running for the script to run correctly.
  
7. Set desired geocoding function as the working geocoder on line #171 and run the script.
 
9. Import created csv file into a GIS program of your choice to create a coordinate layer.
    
❗Note: examples illustrate geopy(1) and Kakao map(2) geocoding results. While geopy is free, convenient and does not require any subscription, its functionalities are severely limited, and near-address matching in foreign language almost always fails. Recommended course of action is to register and use Kakao map API or Google Map API for optimal performance.

<h2>사용 방법 ▶️</h2>

1. 신고 채팅방을 포착할 수 있도록 path, target window, keyword를 설정해주세요. 디폴트로 값이 설정되어있지만 시스템 및 거주 도시에 따라 다를 수 있습니다.
   
2. 카카오톡 txt파일을 저장하기 위한 경로를 설정해주세요.
   
3. 카카오톡 프로그램을 실행해서 목표 카톡방을 열어주세요. 목표 카톡방이 열려 있어야만 작동합니다.
   
4. 171번째 줄에 원하는 지오코더를 넣어 설정하시고  실행해주세요.
   
5. 실행이 완료되면 생성된 csv파일을 원하는 GIS프로그램에서 열어 좌표 레이어를 생성해 사용하시면 됩니다.
   
❗주의: 예시(1) 은 geopy, 예시(2)는 카카오맵 API를 이용한 결과입니다. 보다시피 geopy는 무료이고 사용이 간편하며 아무 등록도 필요로 하지 않지만 기능이 떨어지고 주소가 정확하지 않은 경우 가까운 주소 검색을 거의 하지 못해 좌표 오류가 나는 경우가 대부분입니다. 최선의 결과를 위해서는 카카오맵 API나 구글맵의 유로 API를 사용하는것을 추천합니다.








