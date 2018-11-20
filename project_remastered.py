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

def get_teacher_ratings(teachers, subjects):
	ratings = []
	for teacher in teachers:
		teacher_ratings = []
		for subject in subjects:
			rating = -1
			while rating < 0 or rating > 5:
				try:
					rating = int(input("Enter the rating of " + teacher + " in " + subject + " on a scale of 1 (Best) to 5 (Worst)"))
				except Exception:
					print("Please enter a valid value")
			teacher_ratings.append(rating)
		ratings.append(teacher_ratings)
	return ratings

def teachers_available(teachers):
	for teacher in teachers:
		if teacher[1] > 0:
			return True
	return False

def subjects_unassigned(subjects):
	for subject in subjects:
		if subject[1] > 0:
			return True
	return False

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
			matrix[j][i] -= minimum
	return matrix

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

def get_minimum_lines(matrix, row_selection):
	selected_rows = []
	for i, selection in enumerate(row_selection):
		if selection == -1:
			selected_rows.append(i)
	selected_columns = []
	for row in selected_rows:
		for i, value in enumerate(matrix[row]):
			if value == 0 and i not in selected_columns:
				selected_columns.append(i)
				if i in row_selection:
					selected_rows.append(row_selection.index(i))
	unselected_rows = []
	for i in range(len(matrix)):
		if i not in selected_rows:
			unselected_rows.append(i)
	return [unselected_rows, selected_columns]

def sublists_empty(parent_list):
	for sub_list in parent_list:
		if len(sub_list) > 0:
			return False
	return True

FINAL_ASSIGNMENTS = []

def main():
	subjects = get_subjects()
	teachers = get_teachers()

	teacher_names = []
	for teacher in teachers:
		teacher_names.append(teacher[0])

	subject_names = []
	for subject in subjects:
		subject_names.append(subject[0])

	ratings = get_teacher_ratings(teacher_names, subject_names)

	assignments = []

	while teachers_available(teachers) and subjects_unassigned(subjects):
		teachers_in_use = []
		subjects_in_use = []
		for row, teacher in enumerate(teachers):
			if teacher[1] > 0:
				teachers_in_use.append(row)
				teachers[row][1] -= 1
		for row, subject in enumerate(subjects):
			if subject[1] > 0:
				subjects_in_use.append(row)
				subjects[row][1] -= 1
		extra_zeros = len(teachers_in_use) - len(subjects_in_use)
		matrix = []
		for teacher_index in teachers_in_use:
			teacher_ratings = []
			for subject_index in subjects_in_use:
				teacher_ratings.append(ratings[teacher_index][subject_index])
			if extra_zeros > 0:
				teacher_ratings.extend([0] * extra_zeros)
			matrix.append(teacher_ratings)
		if extra_zeros < 0:
			extra_zeros = extra_zeros * -1
			for x in range(extra_zeros):
				matrix.append([0] * len(subjects_in_use))

		assignments = [-1] * len(matrix)

		optimal_solution_found = False
		while not optimal_solution_found:
			matrix = reduce_matrix(matrix)
			row_scan_result = row_scan(matrix, [])
			column_scan_result = column_scan(matrix, row_scan_result)
			if row_scan_result.count(-1) + column_scan_result.count(-1) != len(matrix):
				scan_updated = True
				while scan_updated:
					scan_updated = False
					extra_row_scan = row_scan_remaining_rows(matrix, column_scan_result, row_scan_result)
					for row, row in enumerate(extra_row_scan):
						if row != -1:
							scan_updated = True
							row_scan_result[row] = row
					extra_column_scan = column_scan_remaining_columns(matrix, row_scan_result, column_scan_result)
					for row, column in enumerate(extra_column_scan):
						if column != -1:
							scan_updated = True
							column_scan_result[row] = column

			if row_scan_result.count(-1) + column_scan_result.count(-1) != len(matrix):
				row_assignment = row_scan_result.copy()
				for row, value in enumerate(column_scan_result):
					if value != -1:
						row_assignment[value] = row
				minimum_lines = get_minimum_lines(matrix, row_assignment)
				if len(minimum_lines[0]) + len(minimum_lines[1]) != len(matrix):
					safe_rows = []
					safe_columns = []
					for row in range(len(matrix)):
						if row not in minimum_lines[0]:
							safe_rows.append(row)
						if row not in minimum_lines[1]:
							safe_columns.append(row)
					minimum = matrix[safe_rows[0]][safe_columns[0]]
					for row in safe_rows:
						for j in safe_columns:
							if matrix[row][j] < minimum:
								minimum = matrix[row][j]

					for row in range(len(matrix)):
						for j in range(len(matrix)):
							if row in minimum_lines[0] and j in minimum_lines[1]:
								matrix[row][j] += minimum
							if row not in minimum_lines[0] and j not in minimum_lines[1]:
								matrix[row][j] -= minimum
				else:
					optimal_solution_found = True
			if row_scan_result.count(-1) + column_scan_result.count(-1) == len(matrix):
				optimal_solution_found = True

		zero_locations = []
		available_columns_to_assign = []

		for row, row in enumerate(matrix):
			zero_positions = []
			for j, value in enumerate(row):
				if value == 0:
					zero_positions.append(j)
					if j not in available_columns_to_assign and j not in assignments:
						available_columns_to_assign.append(j)
			zero_locations.append(zero_positions)


		while not sublists_empty(zero_locations):
			column_count = []
			for column in available_columns_to_assign:
				count = 0
				for locations in zero_locations:
					if column in locations:
						count += 1
				column_count.append(count)

			least_index = column_count.index(min(column_count))
			column_to_assign = available_columns_to_assign[least_index]
			
			row_found = False
			row = 0
			while not row_found and row < len(matrix):
				if column_to_assign in zero_locations[row]:
					row_found = True
				else:
					row += 1
			if row_found:
				assignments[row] = column_to_assign
				available_columns_to_assign.remove(column_to_assign)
				zero_locations[row] = []
			
			
		for i, assignment in enumerate(assignments):
			if len(teachers_in_use) > i:
				if len(subjects_in_use) > assignment:
					FINAL_ASSIGNMENTS.append([teachers[teachers_in_use[i]][0], subjects[subjects_in_use[assignment]][0]])
				else:
					# print("FAILED " + teachers[i][0])
					teachers[teachers_in_use[i]][1] += 1
			else:
				# print("FAILED " + subjects[assignment][0])
				subjects[subjects_in_use[assignment]][1] += 1

	for assignment in FINAL_ASSIGNMENTS:
		print(assignment)
		


if __name__ == '__main__':
	main()
