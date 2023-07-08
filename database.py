from datetime import datetime


class Fire_Base:

    def present(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Attendance").child(
                    self.year()).child(
                    "06_06").child("Present")

                return ref.get()

    def absent(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Attendance").child(
                    self.year()).child(
                    "06_06").child("Absent")

                return ref.get()

    def lecture_code(self, location):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("Modules")

                # Query for retailers in a specific location
                lecture_codes = ref.order_by_child('lecture_name').equal_to(location).get()

                return lecture_codes

    def set_modules(self, name, Mcode, Bname, Mname):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("Modules").child(Mcode)
                ref.set(
                    {
                        "lecture_name": name,
                        "module_code": Mcode,
                        "program_name": Bname,
                        "module_name": Mname

                    }
                )

    def Attend(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                stude = self.Get_Stud()
                for i in stude:
                    ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Attendance") \
                        .child(self.year()).child(self.month_date()).child("Present").child(i)
                    ref.set(self.Get()[i])

                self.absence()

    def Get_Stud(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Students")
                data = ref.get()

                data_list = []
                count = 0
                for i, y in data.items():

                    count = count + 1

                    if count < 10:
                        data_list.append(i)
                    else:
                        return data_list

    def absence(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                all_student = self.Get()
                present_student = self.get_Prese()
                absent_student = {student: status for student, status in all_student.items() if
                                  student not in present_student}
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Attendance") \
                    .child(self.year()).child(self.month_date()).child("Absent")
                for student, status in absent_student.items():
                    ref.child(student).set(status)

    def Get(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Students")
                data = ref.get()

                return data

    def get_Prese(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('FingerPrint').child("Programs").child("BCICT").child("Attendance") \
                    .child(self.year()).child(self.month_date()).child("Present")
                data = ref.get()

                return data

    def year(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return y

    def month_date(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return f"{m}_{d}"

Fire_Base.Attend(Fire_Base())