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



# 코드 실행
def main():
    conn = get_connection()
    drop_table(conn)
    create_board_table(conn)
    create_comment_table(conn)

    conn.close()

if __name__ == '__main__':
    main()