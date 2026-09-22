import pymysql

# 1. DB 연결
def get_connection():
    conn = pymysql.connect(host="127.0.0.1", user="root", port=3306,
                           password="12341234", database="mysqlDB", charset="utf8")
    return conn

# 2. 테이블 만들기
def create_board_table(conn):
    cur = conn.cursor()
    # 테이블 생성
    cur.execute("""
        CREATE TABLE boardTable (
            board_no BIGINT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(100) NOT NULL,
            contents TEXT NOT NULL,
            board_writer CHAR(10) NOT NULL,
            reg_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (board_writer) REFERENCES userTable(id)
        )
    """)

    conn.commit()
    print('board_table 생성완료')
    cur.close()

def create_comment_table(conn):
    cur = conn.cursor()
    # 테이블 생성
    cur.execute("""
        CREATE TABLE commentTable (
            comment_no BIGINT PRIMARY KEY AUTO_INCREMENT,
            board_no BIGINT NOT NULL,
            comment_writer CHAR(10) NOT NULL,
            comment VARCHAR(500) NOT NULL,
            reg_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (board_no) REFERENCES boardTable(board_no) ON DELETE CASCADE,
            FOREIGN KEY (comment_writer) REFERENCES userTable(id)
        )
    """)

    conn.commit()
    print('comment_table 생성완료')
    cur.close()

# 3. 기존 테이블 삭제하기
def drop_table(conn):
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS commentTable")
    cur.execute("DROP TABLE IF EXISTS boardTable")

    conn.commit()

    print('테이블 삭제 성공!')
    cur.close()

# 회원가입
def signup(conn):
    cur = conn.cursor()

    while True:
        user_id = input('아이디 : ')

        # 아이디 중복 체크
        cur.execute(
            'SELECT id FROM userTable WHERE id = %s',
            (user_id,)
        )

        result = cur.fetchone()

        if result is not None:
            print('이미 존재하는 아이디 입니다.')
            # 아이디가 중복이면 아이디 재입력
            continue

        break

    user_pwd = input('비밀번호 : ')
    user_name = input('이름 : ')
    user_email = input('이메일 : ')
    user_addr = input('주소 : ')

    # 아이디가 중복이 아니면 회원 정보 추가
    cur.execute(
        '''
        INSERT INTO userTable (id, pwd, name, email, addr)
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (user_id, user_pwd, user_name, user_email, user_addr)
    )

    conn.commit()
    cur.close()

    print(f'{user_id}님 회원가입 완료 되었습니다.')

# 로그인
def login(conn):
    # SQL를 실행하기 위한 커서 생성
    cur = conn.cursor()

    while True:
        user_id = input('아이디 : ')
        user_pwd = input('비밀번호 : ')

        # 로그인한 아이디가 DB에 있는지 확인
        cur.execute(
            'SELECT id, pwd FROM userTable WHERE id = %s',
            (user_id,)
        )

        # 조회한 값을 result에 저장
        # result는 조회된 한 행이 튜플 형태로 반환됨 ('아이디', '비밀번호')
        result = cur.fetchone()

        # ID가 존재하지 않는 경우
        if result is None:
            print('존재하지 않는 아이디 입니다.')
            continue

        # ID가 존재 하는 경우
        else:
            # 비밀번호가 맞는지 체크
            if result[1] == user_pwd:
                print()
                print(f'🎉 {result[0]}님, 로그인 성공! 환영합니다! 😆')
                # 조회 결과를 가져온 뒤 커서를 닫는다
                cur.close()

                return user_id
            else:
                print('비밀번호가 틀렸습니다.')
                continue

# 게시글 작성
def write_post(conn, current_user):
    cur = conn.cursor()

    title = input('제목을 입력하세요. : ')
    contents = input('내용을 입력하세요. : ')

    cur.execute(
        '''
        INSERT INTO boardTable (title, contents, board_writer)
        VALUES (%s, %s, %s)
        '''
        ,(title, contents, current_user)

    )

    conn.commit()
    cur.close()

    print('게시글이 등록되었습니다.')

# 게시글 목록
def list_posts(conn):
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT a.board_no, a.title, b.name, a.reg_date 
        FROM boardTable a 
        JOIN userTable b
            ON a.board_writer = b.id 
        ORDER BY a.board_no DESC
        '''
    )

    rows = cur.fetchall()
    if not rows:
        print('등록된 게시글이 없습니다.')
    else:
        print('NO\t\t\t제목\t\t\t작성자\t\t\t작성일')
        for row in rows:
            print(f'{row[0]}\t\t{row[1]}\t\t{row[2]}\t\t{row[3]}')

    cur.close()

# 게시글 상세 조회
def view_post(conn):
    pass

# 댓글 작성
def write_comment(conn, current_user):
    pass

# 게시글 삭제
def delete_post(conn, current_user):
    pass

# 코드 실행
def main():
    # 로그인 상태
    current_user = None

    conn = get_connection()

    while True:
        if current_user is None:
            print('[1] 로그인')
            print('[2] 회원가입')
            print('[0] 종료')

            menu_num = input('메뉴 번호를 입력하세요. : ')

            if not menu_num.isdigit():
                print('번호를 입력해주세요.')
                continue

            menu_num = int(menu_num)

            # 로그인
            if menu_num == 1:
                current_user = login(conn)
            # 회원가입
            elif menu_num == 2:
                signup(conn)
            elif menu_num == 0:
                print('프로그램을 종료합니다.')
                break
            else:
                print('존재 하지 않는 메뉴 입니다.')
        else:
            # 게시판 메뉴
            print()
            print('[1] 게시글 작성')
            print('[2] 게시글 목록')
            print('[3] 게시글 상세 조회')
            print('[4] 댓글 작성')
            print('[5] 게시글 삭제')
            print('[6] 로그아웃')
            print('[0] 종료')


            menu_num = input('메뉴 번호를 입력하세요. : ')

            if not menu_num.isdigit():
                print('번호를 입력하세요.')
                continue

            menu_num = int(menu_num)

            # 게시글 작성
            if menu_num == 1:
                write_post(conn, current_user)
            # 게시글 조회
            elif menu_num == 2:
                list_posts(conn)



    conn = get_connection()
    drop_table(conn)
    create_board_table(conn)
    create_comment_table(conn)

    conn.close()

if __name__ == '__main__':
    main()