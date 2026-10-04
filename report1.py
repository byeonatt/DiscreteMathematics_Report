### 20235274 안수민
### 이산수학 report 1

# 1. 행렬 입력 기능 구현(리스트(2차원 배열)로 저장 / n*n 정방행렬
def input_matrix():
    n = int(input("정수 n을 입력하세요: "))
    matrix = []
    print("행렬의 각 원소를 행 단위로 입력하세요:\n")
    for i in range(n):
        row = list(map(float, input(f"{i+1}번째 행: ").split()))
        if len(row) != n:
            print(f">> 오류: {n}개의 원소를 입력해야 합니다.")
            return None
        matrix.append(row)
    return matrix, n

# 2. 행렬식을 이용한 역행렬 계산 기능
def calculate_inverse_determinant(matrix, n):
    determinant = calculate_determinant(matrix, n)
    if determinant == 0:
        print("\n>> 오류: 역행렬이 존재하지 않습니다. (행렬식 0)")
        return None

    # 역행렬 계산
    inverse_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
            cofactor = ((-1) ** (i + j)) * calculate_determinant(minor, n - 1)
            inverse_matrix[j][i] = cofactor / determinant  # 전치 후 나누기 행렬식
    return inverse_matrix

# 2-1. 행렬식 계산 함수
def calculate_determinant(matrix, n):       
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        determinant = 0
        for c in range(n):
            minor = [row[:c] + row[c+1:] for row in (matrix[:0] + matrix[1:])]
            determinant += ((-1) ** c) * matrix[0][c] * calculate_determinant(minor, n - 1)
        return determinant

# 3. 가우스-조던 소거법을 이용한 역행렬 계산 기능
def calculate_inverse_gauss_jordan(matrix, n):
    augmented_matrix = [
        row + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]

    for i in range(n):
        pivot = augmented_matrix[i][i] # 대각 원소

        if pivot == 0:          # 대각 원소가 0일 경우, 아래 행과 교환
            for k in range(i + 1, n):
                if augmented_matrix[k][i] != 0:
                    augmented_matrix[i], augmented_matrix[k] = augmented_matrix[k], augmented_matrix[i]
                    pivot = augmented_matrix[i][i]
                    break
            if pivot == 0:
                print("오류: 역행렬이 존재하지 않습니다. (가우스-조던 소거 불가)")
                return None

        for j in range(2 * n):  # pivot을 1로 만들기
            augmented_matrix[i][j] /= pivot

        for k in range(n):      # 나머지 행의 해당 열을 0으로 만들기
            if k != i:
                factor = augmented_matrix[k][i]

                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    return [[round(value, 2) for value in row[n:]] for row in augmented_matrix]

# 4. 역행렬 계산 결과를 출력하고 비교하는 기능
def compare_inverses(matrix_1, matrix_2, n):
    if matrix_1 is None or matrix_2 is None:
        print("역행렬이 존재하지 않아 비교할 수 없습니다.")
        return

    print("\n\n행렬식 방법으로 계산된 역행렬:")
    for row in matrix_1:
        print(row)

    print("\n가우스-조던 소거법으로 계산된 역행렬:")
    for row in matrix_2:
        print(row)

    # 두 역행렬 비교
    equal = all(
        all(abs(matrix_1[i][j] - matrix_2[i][j]) < 1e-9 for j in range(n))
        for i in range(n)
    )
    if equal:
        print("\n>> 두 방법으로 계산된 역행렬은 동일합니다.")
    else:
        print("\n>> 두 방법으로 계산된 역행렬은 동일하지 않습니다.")




### main 클래스
class Main:
    def __init__(self):
        self.matrix = None
        n = 0

    def run(self):
        ### 정방 행렬 크기 n 및 행렬 입력 함수
        self.matrix, self.n = input_matrix() 
        if self.matrix is not None:
            print("\n입력된 행렬:")
            for row in self.matrix:
                print(row)

            ### 역행렬 계산
            # 행렬식을 이용한 역행렬 계산
            inverse_determinant = calculate_inverse_determinant(self.matrix, self.n)
            # 가우스-조던 소거법을 이용한 역행렬 계산
            inverse_gauss_jordan = calculate_inverse_gauss_jordan(self.matrix, self.n)

            ### 역행렬 비교
            compare_inverses(inverse_determinant, inverse_gauss_jordan, self.n)


            ### 추가 기능) 직교 행렬 검사
            if inverse_determinant is None:
                return
            
            transpose_matrix = [
                [self.matrix[j][i] for j in range(self.n)]
                for i in range(self.n)
            ]

            is_orthogonal = all(
                round(inverse_gauss_jordan[i][j], 2) == round(transpose_matrix[i][j], 2)
                for i in range(self.n)
                for j in range(self.n)
            )

            if is_orthogonal:
                print(">> 주어진 행렬은 직교 행렬입니다.")
            else:
                print(">> 주어진 행렬은 직교 행렬이 아닙니다.")

### main
m = Main()
m.run()



