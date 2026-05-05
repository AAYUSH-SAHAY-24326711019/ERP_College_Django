from django.shortcuts import render
import sqlite3
from django.contrib.auth.hashers import check_password

# Create your views here.


def admin_home(request):
    return render(request, 'erpadmin/index.html')

def admin_login(request):

    if request.method == "POST":

        empid = request.POST.get("empid")
        password = request.POST.get("password")

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT passwordHash, status
            FROM erp_admins
            WHERE empid=?
        """, (empid,))

        row = cursor.fetchone()
        conn.close()

        if row:
            stored_hash, status = row

            if status == "active" and check_password(password, stored_hash):
                return render(request, "erpadmin/success.html")

        return render(request, "erpadmin/failure.html")

    return render(request, "erpadmin/index.html")
