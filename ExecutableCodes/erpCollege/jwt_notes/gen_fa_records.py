'''

INSERT INTO public."appFaculty_faculty"
(id, date_created, faculty_email, faculty_name, faculty_id, faculty_designation, optionselected)
VALUES(0, '', '', '', '', '', '', '', '', '', 0, '', '', 0);

(1,NOW(),'faculty_erp1@erp.com','fa001','fa001','professor','Both_roles'),
(2,NOW(),'faculty_erp2@erp.com','fa002','fa002','professor','Both_roles'),
(3,NOW(),'faculty_erp3@erp.com','fa003','fa003','professor','Both_roles'),
(4,NOW(),'faculty_erp4@erp.com','fa004','fa004','professor','Both_roles'),
(5,NOW(),'faculty_erp5@erp.com','fa005','fa005','professor','Both_roles'),
(6,NOW(),'faculty_erp6@erp.com','fa006','fa006','professor','Both_roles'),
(7,NOW(),'faculty_erp7@erp.com','fa007','fa007','professor','Both_roles'),
(8,NOW(),'faculty_erp8@erp.com','fa008','fa008','professor','Both_roles'),
(9,NOW(),'faculty_erp9@erp.com','fa009','fa009','professor','Both_roles'),

'''

for i in range(1,10):
    print(f"({i},NOW(),'faculty_erp{i}@erp.com','fa00{i}','fa00{i}','professor','Both_roles'),")