### 20235274 안수민
### 이산수학 report 2

# 1. 관계 행렬 입력 기능 구현(리스트(2차원 배열)로 저장 / 5*5 정방행렬)
def input_matrix():
    while True:
        matrix = []
        print("5*5 관계 행렬의 각 원소를 행 단위로 입력하세요:\n")

        for i in range(5):
            try:
                row = list(map(int, input(f"{i+1}번째 행: ").split()))

                if len(row) != 5:
                    print(">> 오류: 5개의 원소를 입력해야 합니다.")
                    break
                if any(x not in (0, 1) for x in row):
                    print(">> 오류: 행렬의 원소는 0 또는 1이어야 합니다.")
                    break
                matrix.append(row)

            except ValueError:
                print(">> 오류: 정수만 입력할 수 있습니다.")
                break

        if len(matrix) == 5:
            return matrix



# 2. 주어진 관계 행렬의 동치 관계 판별 기능
# 2-1. 반사성 판별
def is_reflexive(matrix):
    for i in range(5):
        if matrix[i][i] != 1:
            return False
    return True

# 2-2. 대칭성 판별
def is_symmetric(matrix):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# 2-3. 추이성 판별
def is_transitive(matrix):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == 1:
                for k in range(5):
                    if matrix[j][k] == 1 and matrix[i][k] != 1:
                        return False
    return True

# 2-4. 최종 동치 관계 판별
def is_equivalence_relation(matrix):
    if not is_reflexive(matrix):
        return False
    elif not is_symmetric(matrix):
        return False
    elif not is_transitive(matrix):
        return False
                    
    return True



# 3. 동치 관계인 행렬의 동치류 출력 기능
def print_equivalence_classes(matrix):
    equivalence_classes = []
    visited = [False] * 5

    for i in range(5):
        if not visited[i]:
            equivalence_class = []
            for j in range(5):
                if matrix[i][j] == 1:
                    equivalence_class.append(j + 1)
                    visited[j] = True
            equivalence_classes.append(equivalence_class)

    print(">> 동치류:", end=" ")
    for idx, eq_class in enumerate(equivalence_classes):
        print(eq_class, end=" ")



# 4. 동치 관계가 아닌 행렬의 폐포 구현 기능
def calculate_closure(matrix):
    n = len(matrix)
    result = [row[:] for row in matrix]

    def print_matrix(matrix):
        for row in matrix:
            print(row)

    print("\n[폐포 변환 전 관계 행렬]")
    print_matrix(result)

    # 1. 반사 폐포
    if not is_reflexive(result):
        print("\n>> 반사 폐포 적용")
        for i in range(n):
            result[i][i] = 1

    # 2. 대칭 폐포
    elif not is_symmetric(result):
        print("\n>> 대칭 폐포 적용")
        for i in range(n):
            for j in range(i + 1, n):
                if result[i][j] == 1 or result[j][i] == 1:
                    result[i][j] = 1
                    result[j][i] = 1

    # 3. 추이 폐포
    elif not is_transitive(result):
        print("\n>> 추이 폐포 적용")
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if result[i][k] and result[k][j]:
                        result[i][j] = 1

    print("[폐포 변환 후 관계 행렬]")
    print_matrix(result)
    return result



class Main :
    def __init__(self):
            self.matrix = None

    def run(self):
        self.matrix = input_matrix()
        if self.matrix is None:
            print(">> 행렬 입력 실패, 프로그램을 다시 실행해주세요.")
            return

        # 주어진 관계 행렬이 동치가 아닐 경우
        while not is_equivalence_relation(self.matrix):
            print("\n>> 주어진 관계 행렬은 동치 관계가 아닙니다.")
            self.matrix = calculate_closure(self.matrix)
            print("\n>> 구한 폐포로 변환한 후, 동치 관계를 다시 판별합니다.")

        # 주어진 관계 행렬이 동치일 경우
        print("\n>> 주어진 관계 행렬은 동치 관계입니다.")
        print_equivalence_classes(self.matrix)

### main
m = Main()
m.run()