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
