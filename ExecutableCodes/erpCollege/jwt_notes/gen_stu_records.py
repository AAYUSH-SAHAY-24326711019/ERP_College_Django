'''
string for reference:

INSERT INTO public."appStudent_student"
(id, "name", student_id, course, "session", image, date_created, email, user_id)
(0, '', '', '', '', '', '', '', 0);

1	student1	stu001	MCA',	2024-2026	students/images.jpg	2026-05-12 17:27:43.426 +0530	student1@erp.com	


({i}, 'student{i}', 'stu00{i}', 'MCA',	2024-2026', 'students/images.jpg', NOW(), 'student{i}@erp.com')
'''

for i in range (2,10):
    print(f"('student{i}', 'stu00{i}', 'MCA',	2024-2026', 'students/images.jpg', NOW(), 'student{i}@erp.com'),")

'''
INSERT INTO public."appStudent_student"
(id ,"name", student_id, course, "session", image, date_created, email)
values
(2,'student2', 'stu002', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student2@erp.com'),
(3,'student3', 'stu003', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student3@erp.com'),
(4,'student4', 'stu004', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student4@erp.com'),
(5,'student5', 'stu005', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student5@erp.com'),
(6,'student6', 'stu006', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student6@erp.com'),
(7,'student7', 'stu007', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student7@erp.com'),
(8,'student8', 'stu008', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student8@erp.com'),
(9,'student9', 'stu009', 'MCA','2024-2026', 'students/images.jpg', NOW(), 'student9@erp.com')
'''