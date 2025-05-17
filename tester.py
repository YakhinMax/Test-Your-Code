import subprocess

# Назва вашого .py файлу
file = input('Enter your program file name: ')

# Номер задачі
case = int(input('Enter number of task: '))

if case not in [0, 1, 2, 3, 4, 5]:
    raise Exception("Task could not be found.")

if '.py' not in file:
    file = file + '.py'

# Загрузити тести
def load_test_cases(filename):
    test_cases = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if '=' in line:
                    input_part, output_part = line.strip().split('=')
                    inputs = [float(x) for x in input_part.split(',')]
                    expected_output = int(output_part.strip())
                    test_cases.append((inputs, expected_output))
    except Exception as e:
        print(f"Error reading test cases: {e}")
        exit(1)
    return test_cases

# Define test cases: (input_string, expected_output)
test_cases = load_test_cases('test_cases' + str(case) + '.txt')

def run_test(input_data, expected_output):
    for cmd in ["python", "python3"]:
        try:
            process = subprocess.Popen(
                [cmd, file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            input_text = '\n'.join([str(i) for i in input_data] + [""])

            output, error = process.communicate(input=input_text, timeout=3)

            return output.replace('\n','') == str(expected_output), output, expected_output, error

        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    raise EnvironmentError("No suitable Python 3 interpreter found.")

# Викликати всі тести
for i, (input_data, expected_output) in enumerate(test_cases):
    passed, output, expected, error = run_test(input_data, expected_output)
    if passed:
        print(f"Test {i+1} passed.")
    else:
        print(f"Test {i+1} failed.\n")
        print(f"Input:\n{input_data}\nExpected:\n{expected}\nGot:\n{output}")
        if error:
            print(f"Error:\n{error}")
            break
            
