'''
string for reference:

INSERT INTO public."appStudent_student"
(id, "name", student_id, course, "session", image, date_created, email, user_id)
(0, '', '', '', '', '', '', '', 0);

1	student1	stu001	MCA',	2024-2026	students/images.jpg	2026-05-12 17:27:43.426 +0530	student1@erp.com	


({i}, 'student{i}', 'stu00{i}', 'MCA',	2024-2026', 'students/images.jpg', NOW(), 'student{i}@erp.com')
'''

for i in range (1,11):
    print(f"('student{i}', 'stu00{i}', 'MCA',	2024-2026', null, NOW(), 'student{i}@erp.com'),")

'''
('student1', 'stu001', 'MCA',   2024-2026', null, NOW(), 'student1@erp.com'),
('student2', 'stu002', 'MCA',   2024-2026', null, NOW(), 'student2@erp.com'),
('student3', 'stu003', 'MCA',   2024-2026', null, NOW(), 'student3@erp.com'),
('student4', 'stu004', 'MCA',   2024-2026', null, NOW(), 'student4@erp.com'),
('student5', 'stu005', 'MCA',   2024-2026', null, NOW(), 'student5@erp.com'),
('student6', 'stu006', 'MCA',   2024-2026', null, NOW(), 'student6@erp.com'),
('student7', 'stu007', 'MCA',   2024-2026', null, NOW(), 'student7@erp.com'),
('student8', 'stu008', 'MCA',   2024-2026', null, NOW(), 'student8@erp.com'),
('student9', 'stu009', 'MCA',   2024-2026', null, NOW(), 'student9@erp.com'),
('student10', 'stu0010', 'MCA', 2024-2026', null, NOW(), 'student10@erp.com')


'''
