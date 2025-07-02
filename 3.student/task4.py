# 3. 고급 문제
from task2 import GradedStudent

## 문제 4: 메타클래스를 이용한 싱글톤 패턴 구현
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class School(metaclass=Singleton):
    def __init__(self, name):
        self.name = name
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)
    
    def get_top_student(self):
        # students 리스트에서 가장 높은 평균 점수를 가진 학생을 반환하는 메서드를 작성하세요.
        # GradedStudent 또는 그 자식 클래스의 인스턴스만 고려하세요.
        # YOUR CODE HERE
        return max(
            (s for s in self.students if isinstance(s, GradedStudent)),
            key=lambda s: s.calculate_average(),
            default=None
        )
        
# School 클래스의 객체를 생성하고, 여러 학생을 추가한 후 최고 성적의 학생을 찾아보세요.
# YOUR CODE HERE
# 싱글톤 객체 생성
school = School("떡잎유치원")

# 짱구
student1 = GradedStudent("짱구", 5, 2)
student1.add_score(90)
student1.add_score(82)
student1.add_score(85)
student1.add_score(88)
student1.add_score(92)
student1.calculate_average()
school.add_student(student1)

# 유리
student2 = GradedStudent("유리", 5, 2)
student2.add_score(95)
student2.add_score(91)
student2.add_score(89)
student2.add_score(93)
student2.add_score(90)
student2.calculate_average()
school.add_student(student2)

# 훈이
student3 = GradedStudent("훈이", 5, 2)
student3.add_score(70)
student3.add_score(75)
student3.add_score(80)
student3.add_score(85)
student3.add_score(90)
student3.calculate_average()
school.add_student(student3)

# 철수
student4 = GradedStudent("철수", 5, 2)
student4.add_score(60)
student4.add_score(62)
student4.add_score(65)
student4.add_score(70)
student4.add_score(72)
student4.calculate_average()
school.add_student(student4)

# 맹구
student5 = GradedStudent("맹구", 5, 2)
student5.add_score(88)
student5.add_score(87)
student5.add_score(90)
student5.add_score(91)
student5.add_score(89)
student5.calculate_average()
school.add_student(student5)

# 최고 성적 학생 출력
top_student = school.get_top_student()
print(f"최고 성적 학생: {top_student.name}, 평균: {top_student.calculate_average()}")
