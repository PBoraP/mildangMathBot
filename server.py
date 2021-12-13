import os, logging
import re

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    next()

# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.view("gratitude-modal")
def view_submission(ack, body, client, logger):
    ack()
    logger.info(body["view"]["state"]["values"])
    # Extra Credit: Uncomment out this section
    # thank_you_channel = "your_channel_id"
    # user_text = body["view"]["state"]["values"]["my_block"]["my_action"]["value"]
    # client.chat_postMessage(channel=thank_you_channel, text=user_text)

    
######################### Say Everything  
@app.message("결석")
def say_hello(message, say):
    say(f"학생이 결석 통보 > 어머님으로 하여금 원장님께 결석사실 통보하도록 얘기하기 \
        \n 어머님으로부터 결석 사실이 전달 된 경우 > 휴강,  \
        \n 이외의 상황이면 원장님에게 슬랙주세요")
    
@app.message("지각")
def say_hello(message, say):
    say(f"1. 보이스톡을 걸어봅니다. \
      \n  2. 10분 이상 오지 않으면 '학습관리 이슈공유' 채널에 다음과 같이 올려주세요. \
      \n  '김밀당 학생이 미출석입니다. 원장님, 연락부탁드려요!' " \
       + message.user)
  
    
@app.message("단원정리?")
def send_img(img, say):
    say("https://cdn.glitch.me/21931b43-4140-4070-bad6-b338fac8f618%2FKakaoTalk_20211004_194744277.jpg?v=1638868203835")
    say("오늘 *단원정리* 날인가요? \
    \n 단원 정리 날에는 교재에 이론 정리를 할 수 있게 해주세요. 이 예시처럼요!")

@app.message("일일업무?")
def send_img(message, say):
    say(" 1. 출근 직후 : 오늘 피드가 제대로 잘 나갔는지 확인 \
    \n 2. 수업 진행 : 정해진 스케줄 대로 수업 진행 \
    \n 3. 수업 마무리 : 일일 보고 작성 및 카카오톡 익스포터 실행")
    
@app.message("일일보고")
def send_img(message, say):
    say("일일보고에는, 학생에 관한 정성적인 부분을 써주세요! \
    \n (예) 밀당 수학에 적응하고 있음, 대답을 잘 안함, 점점 정답률이 높아지고 있음.. \
    \n 일일보고 링크 : https://coda.io/d/_dPm6zaoftLf/_suAk9#_lupl4")
    
    
@app.message(re.compile("오타"))
def report_issue(message, say):
    say("콘텐츠 오류를 발견하셨군요! :scream: \
    \n 해당 오류는 *'코다 > 학습관리 > 학습관리 모음 > 콘텐츠 수정 요청'*에 올려주세요. :pray:\
    \n 링크 : https://coda.io/d/_dPm6zaoftLf/_su0Es#_luQIG")
    
@app.message("익스포터")
def exporter_say(message, say):
    say("다운로드 및 설명 : https://mildangeng.slack.com/archives/C01T91TNPLK/p1631605565044900 \
    \n                    \
    \n * ## 주의 사항 ##* \
    \n 1. 카카오톡 익스포터 설치, 실행 가능하려면 카카오톡 대화명이 '밀당영어 000' 이어야 합니다. \
    \n 2. 어드민 페이지 > purchase > 학생목록 > 등록 (학생 한명씩 개별등록) 하셔야 합니다.  ")

    
@app.message("개념")
def study1(message, say):
    say("*수업 흐름* : \
    \n Part1 강의 > Part1 문제, Part2 강의 > Part2 문제\
    \n \
    \n *수업안내 이미지*: https://cdn.glitch.me/21931b43-4140-4070-bad6-b338fac8f618%2F%EB%B0%80%EB%8B%B9%EC%88%98%ED%95%99_%EA%B0%9C%EB%85%90Day.png?v=1638952822631")
    
@app.message("유형")
def study1(message, say):
    say("*수업 흐름* \n Part1 강의 > Part1 문제, Part2 강의 > Part2 문제\
    \n \
    \n '유형 강의 듣는 법이 좀 복잡해! 아래 이미지 먼저 보면서 이해해보자!'라고 가이드를 먼저 주세요! \
    \n (온택트 선생님도 실제 피드를 보내서, 학생에게 어떻게 피드가 전달되는지 확인해보세요! :) \
    \n \
    \n *수업안내 이미지*: https://cdn.glitch.me/21931b43-4140-4070-bad6-b338fac8f618%2F%EB%B0%80%EB%8B%B9%EC%88%98%ED%95%99_%EC%9C%A0%ED%98%95Day.png?v=1638952826668")

@app.message("검수")
def send_img(message, say):
    say("손강의 검수 방법이 궁금하시군요! :hand:\
    \n 아래 페이지를 참고해주세요! \
    \n https://coda.io/d/_dw8wtYH3hSJ/_su9-0#_luZxa")
    
    
    
######################### event
@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")
    
@app.event("reaction_added")
def say_something_to_reaction(say):
    say("OK!")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    
######################### slash command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")

@app.command("/hello-bora")
def hello(body, ack):
    ack(f"안녕하세요! <@{body['user_id']}>님! 잘 지내시죠 :) \
    \n 늘 힘내세요! 응원할게요 :) ") 
    

    
# test
@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    # regular expression matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")    

    
## error handler
@app.error
def global_error_handler(error, body, logger):
    logger.exception(error)
    logger.info(body)
 
    
if __name__ == "__main__":
    app.start(3000)
