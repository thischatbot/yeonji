from task2 import GradedStudent

## 문제 3: 다중 상속을 이용한 운동선수 학생 클래스
class Athlete:
    def __init__(self, sport):
        self.sport = sport
        print("운동선수")
    
    def train(self, hours):
        print(f"{self.sport} 종목에서 {hours}시간 동안 훈련했습니다.")

class StudentAthlete(GradedStudent, Athlete):
    def __init__(self, name, age, grade, sport):
        # GradedStudent와 Athlete의 __init__ 메서드를 모두 호출하세요.
        # YOUR CODE HERE
        GradedStudent.__init__(self, name, age, grade)
        Athlete.__init__(self, sport)
    
    def study(self, hours):
        # GradedStudent의 study 메서드를 호출하고, 추가로 train 메서드도 호출하세요. 이때 훈련은 공부시간의 절반만큼 훈련
        # YOUR CODE HERE
        GradedStudent.study(self, hours)
        Athlete.train(self, hours/2)

# StudentAthlete 클래스의 객체를 생성하고 study 메서드를 호출해보세요.
# YOUR CODE HERE
if __name__ == "__main__":
    studentAthlete = StudentAthlete("연지", 20, 3, "사격")
    studentAthlete.study(4)
