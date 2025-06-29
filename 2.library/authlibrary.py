#2. BaseLibrary class 상속받아서 users 정보 받아오는 AuthLibrary 만들기
from lib import BaseLibrary
from user import User

class AuthLibrary(BaseLibrary):
    def __init__(self):
        super().__init__()
        self.users = []
    
    # 3. 유저 정보 찾는 함수 만들기 (find_user) 
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None # 모든 유저정보에 대해 매칭이 안될때 None 반환
    
    # 4. 유저 등록 함수 만들기 (register_user)
    def register_user(self, username, password):
        if self.find_user(username):
            return False
        self.users.append(User(username, password))
        return True
    
    # 5. 로그인 함수 만들기 (login)
    def login(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            return True
        else:
            return False

class LoanLibrary(AuthLibrary):
    def __init__(self):
        super().__init__()
        self.loans = {} # {username: [Book, ...]}
        
    #2. 책 빌리는 행위를 함수로 만들어주기 : 유저, 책정보
    def borrow_book(self, username, title):
        book = self.search_book(title)
        if book:
            self.books.remove_book(book)
            self.loans.setdefault(username, []).append(book)
            print("📦대출 완료")
        else:
            print("❌ 책 없음")
        
    #3. 책을 반납받는 행위 함수로 만들어주기 : 유저, 책정보
    def return_book(self, username, title):
        if username not in self.loans:
            print("❌ 대출 기록 없음")
            return None # 함수 종료 (None 반환)
        
        for book in self.loans.get(username, []):
            if book.title == title:
                self.loans[username].remove_book(book)
                self.books.append(book)
                print("📥 반납 완료")
                return None # 함수 종료 (None 반환)
            print("❌ 반납 대상 아님")