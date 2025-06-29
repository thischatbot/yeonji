# 도서 클래스
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"제목: {self.title}, 저자: {self.author}"
    
# 도서관 클래스
class BaseLibrary:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        print("✅ 책이 추가되었습니다.")

    def remove_book(self, title):
        self.books = [b for b in self.books if b.title != title]
        print("🗑️ 삭제 시도 완료")

    def search_book(self, title):
        for book in self.books:
            if book.title == title:
                print("🔍 책을 찾았습니다:")
                return b    # Book 객체 변환
        print("❌ 해당 책이 없습니다.")
        return None

    def list_books(self):
        if not self.books:
            print("📚 등록된 책이 없습니다.")
        else:
            print("📚 도서 목록:")
            for book in self.books:
                print(book)
                