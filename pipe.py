import openai
from ocr.recog import ocr_img
from crawl.crawling import retrieve
from img_video.video import vid_generate
from crawl.crawling import extract_locations
import os 
import random


openai.api_key = ''


def chat_gpt(contents,prompt):

    conversation=[]
    conversation.append({"role": "system", "content": contents})
    conversation.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    answer = response.choices[0].message.content.strip()
    

    return answer


def recommending(script):
   
        input=f"""
             
            추천 장소: 갤러리 청람
            주소: 대전광역시 서구 만년동 393
             
             ==> 위와 같은 템플릿 형태로 제목: , 해시태그: , 게시물: 이 적혀있는 아래 문서를 읽고 문서내 분위기와 
             내용을 파악하여 아래 문서를 작성한 유저가 갈만한 실제 대전광역시와 관련된 장소(음식점이나 관광지)를 3곳을 추천하시오,
             추천된 장소와 이레 문서내의 제목에 있는 장소와 같아서는 안된다. 그리고 출력은 추천 장소이름과 주소만 하도록한다.
             추천한 이유도 짧은 1줄로 간략히 설명한다. 해당 추천된 장소는 실제로 대전에 있는곳이어야한다. 주소도
             실제로 존재하는 대전 내의 주소여야한다. 추천장소기준은 아래 문서의 제목에 해당 하는 장소를 유저가 떠난 후에 바로 갈만한곳으로 추천하시오.
             음식점과 음식점아닌 관광지 등 다양히 추천하시오. 추천장소명에는 대전 이라는 단어가 있도록해야하고 그장소는
             실제로 대전에 있는 장소여야한다.

             다음은 아래 문서 내용이다.
             
             --->

             {script}

             """
      
        a="당신은 한국어를 잘하는 모델입니다"
        answer=chat_gpt(a,input)
        return answer
    
def main_pipe(user_name2,input_path2,input_prompt2="관광 홍보 영상"):
            

            user_name=user_name2 # 사용자 이름
            input_path=input_path2 # 유저가 게시글을 쓰고 전체화면 촬영되어서 나온이미지 
            input_prompt=input_prompt2 # 비디오에 나왔으면 하는 효과

            steps2=38
            scale2=9.0

            num=int(random.random()*100)

            if os.path.exists(user_name):
                  user_name=user_name+f"_{num}"

            A="/root/naver/members/soo/pipeline2/"
            user_name=A+user_name
            os.makedirs(user_name,exist_ok=True)

            if input_prompt.find(".")>-1:
                  pass
            else:
                  input_prompt+="."

            texts=ocr_img(input_path)
            
            texts2=recommending(texts)
            
            locations=extract_locations(texts2)
            name=user_name.split("/")[-1]

            with open(f"{user_name}/log_{name}.txt","a") as log:
                  log.writelines(f"{name} 의 게시글")
                  log.writelines("\n")
                  log.writelines("\n")
                  log.writelines(f"{texts}")
                  log.writelines("\n")
                  log.writelines("\n")
                  log.writelines(f"{name} 위한 추천장소들")
                  log.writelines("\n")
                  log.writelines("\n")
                  log.writelines(f"{locations}")
                  log.writelines("\n")
                  log.writelines("\n")
                  log.close()

            gif_list=[]

            recommend_img_path=retrieve(locations[0],user_name)
            print(recommend_img_path)
            gif_path=vid_generate(recommend_img_path,input_prompt,steps2,scale2,user_name)
            gif_list.append(gif_path)
            os.remove(input_path2)
            os.makedirs("/root/naver/members/soo/pipeline2/user_input",exist_ok=True)

            return gif_list[0],recommend_img_path,locations[0]

       
if __name__ == '__main__':

      gif_path,img_path=main_pipe("user11","/root/naver/members/soo/pipeline2/user_input/input.png","관광 홍보위한 동영상")
      print(gif_path)
      print(img_path)
  

    
    


        
