from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from google.cloud import vision



def detect_text(path):
    """Detects text in the file."""

    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations




    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return texts[0].description



triviaLinks = ["https://www.freekigames.com/wizard101-conjuring-trivia", "https://www.freekigames.com/wizard101-magical-trivia", "https://www.freekigames.com/wizard101-spells-trivia",
               "https://www.freekigames.com/wizard101-marleybone-trivia", "https://www.freekigames.com/wizard101-wizard-city-trivia", "https://www.freekigames.com/wizard101-zafaria-trivia",
               "https://www.freekigames.com/wizard101-mystical-trivia", "https://www.freekigames.com/wizard101-spellbinding-trivia", "https://www.freekigames.com/pirate101-aquila-trivia",
               "https://www.freekigames.com/pirate101-adventure-trivia"]


triviaPaths = ["C:/Users/harry/Desktop/KITriviaAnswers/Conjuring.txt", "C:/Users/harry/Desktop/KITriviaAnswers/Magical.txt", "C:/Users/harry/Desktop/KITriviaAnswers/Spells.txt",
               "C:/Users/harry/Desktop/KITriviaAnswers/Marleybone.txt", "C:/Users/harry/Desktop/KITriviaAnswers/WizardCity.txt", "C:/Users/harry/Desktop/KITriviaAnswers/Zafaria.txt",
               "C:/Users/harry/Desktop/KITriviaAnswers/Mystical.txt", "C:/Users/harry/Desktop/KITriviaAnswers/Spellbinding.txt", "C:/Users/harry/Desktop/KITriviaAnswers/P101Aquila.txt",
               "C:/Users/harry/Desktop/KITriviaAnswers/P101Adventure.txt"]


PATH = 'C:\Program Files (x86)\chromedriver.exe'

class Answer:
    htmlClass = "answerText"
    index = 0
    title = ""
    boxHtmlClass = "largecheckbox"
    def __init__(self, index):
        self.index = index


answers = [Answer(index=c) for c in range(4)]

driver = webdriver.Chrome(PATH)
for t in range(len(triviaLinks)):
    driver.get(triviaLinks[t])
    assert "Trivia" in driver.title
    if t == 0:
        driver.execute_script("openIframeSecure('/auth/popup/login/freekigames?fpShowRegister=true');")
        time.sleep(0.5)
        driver.switch_to.frame(driver.find_element_by_id("jPopFrame_content"))
        username = driver.find_element_by_id("userName")
        time.sleep(0.2)
        username.clear()
        time.sleep(0.2)
        username.send_keys("ENTER ACCOUNT USERNAME HERE")
        time.sleep(0.2)
        password = driver.find_element_by_id("password")
        time.sleep(0.2)
        password.clear()
        time.sleep(0.2)
        password.send_keys("ENTER ACCOUNT PASSWORD HERE")


        driver.execute_script("document.getElementById('login').click()")



    for j in range(12):

        try:
            question = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quizQuestion"))
            )
            print(question.text)
            #time.sleep(2)

            answerList = []
            answerList = driver.find_elements_by_class_name("answerText")

            foundQuestion = False

            with open(triviaPaths[t]) as myFile:
                for num, line in enumerate(myFile, 1):
                    # print(line)

                    if foundQuestion:
                        theAnswer = line
                        print(theAnswer)
                        foundQuestion = False
                        break

                    if question.text.rstrip() in line:
                        # print('found at line:', num)
                        foundQuestion = True
                        continue


            time.sleep(1)
            print(not all(i.text != "" for i in answerList))

            while not all(i.text != "" for i in answerList):
                time.sleep(0.5)
                answerList = driver.find_elements_by_class_name(Answer.htmlClass)
            for count, o in enumerate(answerList):
                answers[count].title = o.text
            time.sleep(2)
            print("passed ")
            boxList = driver.find_elements_by_class_name(Answer.boxHtmlClass)
            for count, i in enumerate(answers):
                if i.title in theAnswer:
                    boxList[i.index].click()
                    break
                elif count == len(answers):
                    boxList[2].click()

            driver.execute_script("updateQuiz();")

        except:
            print("unable to find element")
