"""
Python script to perform the hungarian method of solving the assignment problem
While making this, certain python features were avoided in some instances to ensure
people using other languages may read the code
"""

def get_subjects():
	""" Gets the list of subjects that should be taught from the user """
	number_of_subjects = int(input("Enter the number of subjects to be taught"))
	subjects = []
	for i in range(number_of_subjects):
		subject_name = ""
		while subject_name == "":
			subject_name = input("Enter the subject's name")
		number_of_instances = -1
		while number_of_instances < 0:
			try:
				number_of_instances = int(input("Enter the number of instances the subject is to have"))
			except Exception:
				print("Please enter a valid number")
				number_of_instances = -1
		subjects.append([subject_name, number_of_instances])
	return subjects


def get_teachers():
	""" Gets a list of teachers to teach the subjects """
	number_of_teachers = int(input("Enter the number of teachers available"))
	teachers = []
	for i in range(number_of_teachers):
		teacher_name = ""
		while teacher_name == "":
			teacher_name = input("Enter the teacher's name")
		number_of_classes = -1
		while number_of_classes < 0:
			try:
				number_of_classes = int(input("Enter the number of classes the person is to teach"))
			except Exception:
				print("Please enter a valid value")
				number_of_classes = -1
		teachers.append([teacher_name, number_of_classes])
	return teachers

def build_matrix(teachers, subjects):
	matrix = []
	number_of_teachers = 0
	number_of_subjects = 0
	for teacher in teachers:
		teacher_name = teacher[0]
		amount_of_classes = teacher[1]
		number_of_teachers += amount_of_classes
		teacher_ratings = []
		for subject in subjects:
			subject_name = subject[0]
			amount_of_instances = subject[1]
			rating = -1
			# while rating < 0 or rating > 5:
			while rating < 0:
				try:
					rating = int(input("Enter the rating of " + teacher_name + " in " + subject_name + " on a scale of 1 (Best) to 5 (Worst)"))
				except Exception:
					print("Please enter a valid value")
			for i in range(amount_of_instances):
				teacher_ratings.append(rating)
		matrix.append(teacher_ratings)
	for subject in subjects:
		amount_of_instances = subject[1]
		number_of_subjects += amount_of_instances

	#Calculates the difference in the amount of rows and columns
	extra_zeroes = number_of_teachers - number_of_subjects

	#Zero padding
	if extra_zeroes < 0:
		amount_of_zeroes = extra_zeroes * -1
		for row in matrix:
			for i in range(amount_of_zeroes):
				row.append(0)
	if extra_zeroes > 0:
		for i in range(extra_zeroes):
			row = []
			for j in range(number_of_teachers):
				row.append(0)
			matrix.append(row)
	return matrix

def get_column(matrix, column_number):
	column = []
	for row in matrix:
		column.append(row[column_number])
	return column

def reduce_matrix(matrix):
	for i, row in enumerate(matrix):
		minimum = min(row)
		matrix[i] = [value - minimum for value in row]
	
	for i, value in enumerate(matrix):
		column = get_column(matrix, i)
		minimum = min(column)
		for j in range(len(column)):
			matrix[i][j] -= minimum
		
	return matrix

# def row_scan(matrix, eliminated_columns):
# 	row_scan_result = []
# 	for i, row in enumerate(matrix):
# 		if i not in eliminated_columns:
# 			zero_positions = []
# 			for j, value in enumerate(row):
# 				if eliminated_columns[j] == -1 and j not in row_scan_result:
# 					if value == 0:
# 						zero_positions.append(j)
# 				if len(zero_positions) > 1:
# 					break
# 			if len(zero_positions) == 1:
# 				row_scan_result.append(zero_positions[0])
# 			else:
# 				row_scan_result.append(-1)
# 	return row_scan_result

def row_scan(matrix, eliminated_columns):
	row_scan_result = []
	for i, row in enumerate(matrix):
		if row.count(0) == 1 and i not in eliminated_columns and row.index(0) not in row_scan_result:
			row_scan_result.append(row.index(0))
		else:
			row_scan_result.append(-1)
	return row_scan_result

def row_scan_remaining_rows(matrix, eliminated_columns, eliminated_rows):
	row_scan_result = eliminated_rows.copy()
	for i, row in enumerate(matrix):
		if row_scan_result[i] == -1 and i not in eliminated_columns:
			zero_locations = []
			for j, value in enumerate(row):
				if value == 0:
					if j not in row_scan_result and j not in eliminated_rows:
						zero_locations.append(j)
					if len(zero_locations) > 1:
						break
			if len(zero_locations) == 1:
				row_scan_result[i] = zero_locations[0]
			else:
				row_scan_result[i] = -1
		else:
			row_scan_result[i] = -1
	return row_scan_result

def column_scan(matrix, eliminated_rows):
	column_scan_results = []
	for i, row in enumerate(matrix):
		if eliminated_rows[i] == -1:
			column = get_column(matrix, i)
			if column.count(0) == 1 and column.index(0) not in column_scan_results:
				column_scan_results.append(column.index(0))
			else:
				column_scan_results.append(-1)
		else:
			column_scan_results.append(-1)
	return column_scan_results


def column_scan_remaining_columns(matrix, eliminated_rows, eliminated_columns):
	column_scan_results = eliminated_columns.copy()
	for i, row in enumerate(matrix):
		if eliminated_columns[i] == -1 and i not in eliminated_rows:
			if i not in eliminated_rows:
				column = get_column(matrix, i)
				zero_positions = []
				for j, value in enumerate(column):
					if j not in column_scan_results and j not in eliminated_columns:
						if value == 0:
							zero_positions.append(j)
					if len(zero_positions) > 1:
						break
				if len(zero_positions) == 1:
					column_scan_results[i] = zero_positions[0]
				else:
					column_scan_results[i] = -1
			else:
				column_scan_results[i] = -1
		else:
			column_scan_results[i] = -1
	return column_scan_results

def get_minimum_lines(matrix, row_scan_results, column_scan_results):
	print("Scan results")
	print(row_scan_results)
	print(column_scan_results)
	print("-")
	row_assigned_to_columns = []
	for i, value in enumerate(column_scan_results):
		if value != -1:
			row_assigned_to_columns.append(value)
		else:
			if i in row_scan_results:
				row_assigned_to_columns.append(row_scan_results.index(i))
			else:
				row_assigned_to_columns.append(-1)
	rows_selected = []
	for i in range(len(matrix)):
		if i not in row_assigned_to_columns:
			rows_selected.append(i)
	print("Rows Selected")
	print(row_assigned_to_columns)
	print(rows_selected)
	columns_selected = []
	for row in rows_selected:
		for i, value in enumerate(matrix[row]):
			if value == 0 and i not in columns_selected:
				columns_selected.append(i)
	for column in columns_selected:
		if row_assigned_to_columns[column] != -1:
			rows_selected.append(row_assigned_to_columns[column])
	rows_not_selected = []
	for i in range(len(matrix)):
		if i not in rows_selected:
			rows_not_selected.append(i)
	print("SELECTED ROWS AND COLUMNS")
	print(rows_not_selected)
	print(columns_selected)
	return [rows_not_selected, columns_selected]

def adjust_matrix_by_lines(matrix, lines_on_rows, lines_on_columns):
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if i in lines_on_rows and j in lines_on_columns:
				matrix[i][j] += 1
			elif i not in lines_on_rows and j not in lines_on_columns:
				matrix[i][j] -= 1
	return matrix

def find_optimal_solution(matrix):
	eliminated_columns = [-1] * len(matrix)
	row_scan_result = row_scan(matrix, eliminated_columns)
	column_scan_result = column_scan(matrix, row_scan_result)
	extra_assignment_found = True
	while extra_assignment_found:
		extra_assignment_found = False
		extra_row_assignment = row_scan_remaining_rows(matrix, column_scan_result, row_scan_result)
		print("EXTRA ROW")
		print(row_scan_result)
		for i, row in enumerate(extra_row_assignment):
			if row != -1:
				extra_assignment_found = True
				row_scan_result[i] = row
		print(extra_row_assignment)
		# print(row_scan_result)
		print("EXTRA COLUMN")
		print(column_scan_result)
		extra_column_assignment = column_scan_remaining_columns(matrix, row_scan_result, column_scan_result)
		for i, column in enumerate(extra_column_assignment):
			if column != -1:
				extra_assignment_found = True
				column_scan_result[i] = column
		print(extra_column_assignment)
		# print(column_scan_result)
	if row_scan_result.count(-1) + column_scan_result.count(-1) == len(matrix):
		optimal = []
		for i, value in enumerate(row_scan_result):
			if value != -1:
				optimal.append(value)
			else:
				optimal.append(column_scan_result.index(i))
		return optimal
	else:
		minimum_lines = get_minimum_lines(matrix, row_scan_result, column_scan_result)
		while len(minimum_lines[0]) + len(minimum_lines[1]) != len(matrix):
			matrix = adjust_matrix_by_lines(matrix, minimum_lines[0], minimum_lines[1])
			row_scan_result = row_scan(matrix, [])
			column_scan_result = column_scan(matrix, row_scan_result)
			minimum_lines = get_minimum_lines(matrix, row_scan_result, column_scan_result)
			print("______________________________________")
			for row in matrix:
				print(row)


ratings_matrix = []

def main():
	subjects = get_subjects()
	teachers = get_teachers()

	ratings_matrix = build_matrix(teachers, subjects)

	ratings_matrix = reduce_matrix(ratings_matrix)

	optimal_solution = find_optimal_solution(ratings_matrix)

	# print(row_scan_result)
	# print(column_scan_result)



if __name__ == '__main__':
	main()
