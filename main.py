import os

from fastapi import FastAPI
from dotenv import load_dotenv

import requests

from models import Course, Discussion, DiscussionEntry


app = FastAPI()
# /courses/:course_id/discussion_topics
# /courses

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {
    "Authorization": f"Bearer {access_token}"
}

@app.get("/courses")
async def get_courses() -> list[Course]:
    response = requests.get(url=f"{base_url}/courses", headers=headers)
    r_json = response.json()
   
    courses: list[Course] = []
    for course_json in r_json:
        course = Course(id=course_json["id"], name=course_json["name"])

    courses.append(course)
    
    return courses

@app.get("/discussions")
async def get_discussions(course_id: int) -> list[Discussion]:
    response = requests.get(url=f"{base_url}/courses/{course_id}/discussion_topics", headers=headers)
    r_json = response.json()

    discussions: list[Discussion] = []
    for discussion_json in r_json:
        discussion = Discussion(id=discussion_json["id"], title=discussion_json["title"])
        discussions.append(discussion)

    return discussions
    

@app.post("/discussions")
async def create_discussion_entry(body: DiscussionEntry, course_id: int = 942225, topic_id: int = 6613305):
    body = {"message": "HOTDOG"}
    response = requests.post(url=f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries", headers=headers, data=body.model_dump())

    return response.json()


#    body = DiscussionEntry(message=message)
 #   response = requests.post(url=f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries", headers=headers, data=body.model_dump_json())
  #  r_json = response.json()
   # return

