import os

def get_subjects():
	numberOfSubjects = int(input("Enter the number of subjects to be taught"))
	subjects = []
	for x in range(numberOfSubjects):
		subjects.append(input("Enter subject #" + str(x + 1)))
	return subjects

def get_teachers():
	numberOfTeachers = int(input("Enter the number of teachers available"))
	teachers = []
	for x in range(numberOfTeachers):
		teachers.append(input("Enter teacher #" + str(x + 1)))
	return teachers

def build_matrix(subjects, teachers):
	
	ratings_matrix = []

	extra_columns = len(teachers) - len(subjects)
	
	for teacher in teachers:
		ratings = []
	
		for subject in subjects:
			ratings.append(int(input("Enter rating for " + teacher + " in " + subject)))
		if extra_columns > 0:
			for x in range(extra_columns):
				ratings.append(0)
		ratings_matrix.append(ratings)
	
	if extra_columns < 0:
		for x in range(extra_columns * -1):
			ratings_matrix.append([0] * len(subjects))
	return ratings_matrix

def get_column(matrix, column_number):
	column = []
	for i in range(len(matrix[0])):
		column.append(matrix[i][column_number])
	return column

def reduce_matrix(matrix):
	new_matrix = []
	for row in matrix:
		new_matrix.append([x - min(row) for x in row])
	for i in range(len(new_matrix[0])):
		column_minimum = min(get_column(new_matrix, i))
		if column_minimum == 0:
			continue
		for j in range(len(new_matrix[0])):
			new_matrix[j][i] -= column_minimum
	return new_matrix

def row_scan(matrix):
	eliminated_columns = []
	for row in matrix:
		zero_count = row.count(0)
		if zero_count == 1 and row.index(0) not in eliminated_columns:
			eliminated_columns.append(row.index(0))
		else:
			zero_locations = []
			x = 0
			while len(zero_locations) != zero_count:
				if row[x] == 0:
					if x in eliminated_columns:
						zero_count -= 1
					else:
						zero_locations.append(x)
				if len(zero_locations) > 1:
					break
				x += 1
			if zero_count == 1:
				eliminated_columns.append(zero_locations[0])
			else:
				eliminated_columns.append(-1)
	return eliminated_columns


def column_scan(matrix, eliminated):
	eliminated_rows = []
	for i, value in enumerate(matrix):
		if i in eliminated:
			eliminated_rows.append(-1)
			continue
		column = get_column(matrix, i)
		zero_count = column.count(0)
		if zero_count == 1 and column.index(0) not in eliminated_rows:
			eliminated_rows.append(column.index(0))
		else:
			zero_locations = []
			x = 0
			while len(zero_locations) != zero_count:
				if column[x] == 0:
					if x in eliminated_rows:
						zero_count -= 1
					else:
						zero_locations.append(x)
				if len(zero_locations) > 1:
					break
				x += 1
			if zero_count == 1:
				eliminated_rows.append(zero_locations[0])
			else:
				eliminated_rows.append(-1)
	return eliminated_rows

def main():
	subjects = get_subjects()

	teachers = get_teachers()

	ratings_matrix = build_matrix(subjects, teachers)

	ratings_matrix = reduce_matrix(ratings_matrix)

	row_scan_result = row_scan(ratings_matrix)

	column_scan_results = None

	if row_scan_result.count(-1) != 0:
		column_scan_results = column_scan(ratings_matrix, row_scan_result)
	else:
		column_scan_results = [-1] * len(ratings_matrix)

	while row_scan_result.count(-1) + column_scan_results.count(-1) != len(ratings_matrix):
		for i in column_scan_results:
			if i == -1:
				continue
			for j in row_scan_result:
				if j == -1:
					continue
				ratings_matrix[i][j] += 1

		available_rows = [x for x in list(range(len(ratings_matrix))) if x not in column_scan_results]
		available_columns = [x for x in list(range(len(ratings_matrix))) if x not in row_scan_result]

		for i in available_rows:
			for j in available_columns:
				ratings_matrix[i][j] -= 1

		ratings_matrix = reduce_matrix(ratings_matrix)
		row_scan_result = row_scan(ratings_matrix)

		if row_scan_result.count(-1) != 0:
			column_scan_results = column_scan(ratings_matrix, row_scan_result)
		else:
			column_scan_results = [-1] * len(ratings_matrix)

	optimal = row_scan_result.copy()
	for i, value in enumerate(column_scan_results):
		if value != -1:
			optimal[value] = i
	print("____________________________________________________________________________")
	print(optimal)

if __name__ == '__main__':
	main()
	