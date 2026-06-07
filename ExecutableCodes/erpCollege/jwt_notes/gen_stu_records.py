'''
string for reference:

INSERT INTO public."appStudent_student"
(id, "name", student_id, course, "session", image, date_created, email, user_id)
(0, '', '', '', '', '', '', '', 0);

1	student1	stu001	MCA',	2024-2026	students/images.jpg	2026-05-12 17:27:43.426 +0530	student1@erp.com	


({i}, 'student{i}', 'stu00{i}', 'MCA',	2024-2026', 'students/images.jpg', NOW(), 'student{i}@erp.com')
'''

for i in range (2,10):
    print(f"('student{i}', 'stu00{i}', 'MCA',	2024-2026', null, NOW(), 'student{i}@erp.com'),")


