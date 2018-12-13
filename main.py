import psycopg2
import base64
import json
import os
import string


templates = [
    # ["{{ logo }}", "logo", ""],
    # ["{{ under_logo }}", "under_logo", ""],
    # ["{{ analytical_reports_active }}", "analytical_reports_active", "analytical_reports_active"],
    # ["{{ analytical_reports_supplier_analysis }}", "analytical_reports_supplier_analysis", "analytical_reports_supplier_analysis"],
    # ["{{ analytical_reports_need }}", "analytical_reports_need", "analytical_reports_need"],
    # ["{{ analytical_reports_audit }}", "analytical_reports_audit", "analytical_reports_audit"],
    # ["{{ analytical_reports }}", "analytical_reports", "analytical_reports"],
    # ["{{ footer }}", "footer", ""]
    ["{{ single_link }}", "single_link", ""],
]

conn = psycopg2.connect(host="127.0.0.1", database="", user="", password="")
cur = conn.cursor()

cur.execute("SELECT id, email FROM emails_for_sender WHERE role > 50 ORDER BY role;")
users = []
for row in cur:
    users.append(row[0])


# try:
with open(r"/opt/index.html", "r") as file_r:
    body = file_r.read()
    for user in users:
        new_body = body
        for template in templates:
            # try:
            my_url = '{"email": "' + str(user) + '","stat_link": "' + str(template[1]) + '","link": "' + str(template[2]) + '"}'
            encod = "http://yousite/redirecting?linkname=" + base64.b64encode(str(my_url).encode("UTF-8")).decode("utf-8")

            new_body = new_body.replace(str(template[0]), encod)
            # except IOError:
            #     print("ERROR 2: IOError")
            # except Exception:
            #     print("ERROR 2: Другая ошибка")
        with open(r"/opt/edit.html", "w") as file_w:
            file_w.write(new_body)
            cmd = '(echo "Content-Type: text/html; charset=\"utf-8\""; echo "To: %s"; echo "From: Sender Name <info@yousite>"; echo "Subject: "; cat /opt/edit.html;) | sendmail -t -i' % user
            os.system(cmd)
            cur.execute("UPDATE emails_for_sender SET status = 1, updated = now() WHERE id = %s", (str(user),))
            conn.commit()

cur.close()
conn.close()

# except IOError:
#     print("ERROR: IOError")
# except Exception:
#     print("ERROR: Другая ошибка")
