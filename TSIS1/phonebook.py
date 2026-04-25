import json
from connect import get_connection

# --- ADD CONTACT ---
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()

    if not g:
        cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
        gid = cur.fetchone()[0]
    else:
        gid = g[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO NOTHING
    """, (name, email, birthday, gid))

    conn.commit()
    cur.close()
    conn.close()


# --- ADD PHONE ---
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()


# --- SEARCH ---
def search():
    q = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()


# --- FILTER BY GROUP ---
def filter_group():
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name=%s
    """, (group,))

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()


# --- EXPORT JSON ---
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str)

    print("Exported")

    cur.close()
    conn.close()


# --- IMPORT JSON ---
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for row in data:
        name, email, birthday, group, phone, ptype = row

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        g = cur.fetchone()

        if not g:
            cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
            gid = cur.fetchone()[0]
        else:
            gid = g[0]

        cur.execute("""
            INSERT INTO contacts(name,email,birthday,group_id)
            VALUES(%s,%s,%s,%s)
            RETURNING id
        """, (name,email,birthday,gid))

        cid = cur.fetchone()[0]

        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s)
            """,(cid,phone,ptype))

    conn.commit()
    cur.close()
    conn.close()


# --- MENU ---
def menu():
    while True:
        print("\n1.Add contact\n2.Add phone\n3.Search\n4.Filter group\n5.Export\n6.Import\n0.Exit")
        ch = input("> ")

        if ch == "1": add_contact()
        elif ch == "2": add_phone()
        elif ch == "3": search()
        elif ch == "4": filter_group()
        elif ch == "5": export_json()
        elif ch == "6": import_json()
        elif ch == "0": break


if __name__ == "__main__":
    menu()