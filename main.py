import requests
import json
from bs4 import BeautifulSoup

page = requests.get("https://web.uvic.ca/calendar2019-05/CDs/STAT/254.html")

soup = BeautifulSoup(page.content, "html.parser")

courseSubjectNumber = soup.find_all(class_="subject-and-number")[0].get_text()
courseTitle = soup.find_all(class_="course-title")[0].get_text()
courseUnits = soup.select(".units b")[0].get_text()
courseHours = soup.select(".hours b")[0].get_text()
courseDescription = soup.find_all(class_="description")[0].get_text()
courseNotes = [x.get_text() for x in soup.select(".notes li")]

## Nearly all courses have prereqs, some have coreqs section
coursePrereqs = [x.get_text() for x in soup.select(".prereq li")]
courseCoreqs = [x.get_text() for x in soup.select(".coreq li")]

## Some ccourses contain pre/co-reqs intertwined section
coursePreCoreqs = [x.get_text() for x in soup.select(".precoreq li")]

class Main():
    courseListings = []
    _calendarWebsiteVersion = "calendar2019-05"
    
    def __init__(self):
        pass

    def getAllSubjectNumberListings(self):

        ## Load all course subjects, and then search for course numbers accordingly
        with open("data/subjects.json") as f:
            data = json.load(f)

        for subject in data:
            page = requests.get("https://web.uvic.ca/"+self._calendarWebsiteVersion+"/CDs/"+subject+"/CTs.html")
            soup = BeautifulSoup(page.content, "html.parser")

            ## Search for all courses in the subject's listings
            courseNumbersList = [x.select("td:nth-of-type(1) a")[0].get_text()
                                 for x in soup.select(".crs-list table tr")
                                 if len(x.select("td:nth-of-type(1) a")) == 1]

            ## For each course, fetch all relevant data and add to courseListings
            for courseNumber in courseNumbersList:
                courseData = {}
                
                page = requests.get("https://web.uvic.ca/"+self._calendarWebsiteVersion+"/CDs/"+subject+"/"+courseNumber+".html")
                soup = BeautifulSoup(page.content, "html.parser")

                ## Fetch all relevant data from course page
                courseData["course_str"] = soup.find_all(class_="subject-and-number")[0].get_text()
                courseData["course_subject"] = courseData["course_str"].split(" ")[0]
                courseData["course_number"] = courseData["course_str"].split(" ")[1]
                courseData["credits"] = float(soup.select(".units b")[0].get_text())

                courseData["description"] = {}
                courseData["description"]["title"] = soup.find_all(class_="course-title")[0].get_text()
                courseData["description"]["hours"] = soup.select(".hours b")[0].get_text()
                courseData["description"]["description"] = soup.find_all(class_="description")[0].get_text()
                courseData["description"]["link"] = subject+"/"+courseNumber+".html"
                
                print(courseData)
            

if __name__ == "__main__":
    main = Main()
    main.getAllSubjectNumberListings()














    

    
