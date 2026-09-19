import sqlite3


DB_NAME = "foodshare.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    # ========================================================
    # DONATIONS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            food_name TEXT,

            quantity INTEGER,

            location TEXT,

            hours_old INTEGER,

            category TEXT,

            priority TEXT,

            recipient TEXT,

            recommendation TEXT,

            status TEXT

        )
    """)


    # ========================================================
    # RECIPIENTS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            recipient_type TEXT,

            location TEXT,

            capacity INTEGER,

            accepts_cooked INTEGER,

            accepts_packaged INTEGER,

            contact TEXT

        )
    """)


    # ========================================================
    # ADD SAMPLE RECIPIENTS
    # ========================================================

    cursor.execute(
        "SELECT COUNT(*) FROM recipients"
    )

    count = cursor.fetchone()[0]


    if count == 0:

        recipients = [

            (
                "Community Kitchen",
                "Community Kitchen",
                "College Area",
                100,
                1,
                0,
                "9000000001"
            ),

            (
                "Helping Hands NGO",
                "NGO",
                "MVP Colony",
                75,
                1,
                1,
                "9000000002"
            ),

            (
                "City Food Bank",
                "Food Bank",
                "Visakhapatnam",
                200,
                0,
                1,
                "9000000003"
            ),

            (
                "Community Care Center",
                "Community Center",
                "Maddilapalem",
                50,
                1,
                1,
                "9000000004"
            ),

            (
                "Hope Shelter",
                "Shelter",
                "Gajuwaka",
                40,
                1,
                1,
                "9000000005"
            ),

            (
                "Local Families Network",
                "Community Group",
                "College Area",
                30,
                1,
                1,
                "9000000006"
            )

        ]


        cursor.executemany("""

            INSERT INTO recipients (

                name,
                recipient_type,
                location,
                capacity,
                accepts_cooked,
                accepts_packaged,
                contact

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, recipients)


    conn.commit()

    conn.close()


# ============================================================
# ADD DONATION
# ============================================================

def add_donation(

    food_name,
    quantity,
    location,
    hours_old,
    category,
    priority,
    recipient,
    recommendation,
    status

):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""

        INSERT INTO donations (

            food_name,
            quantity,
            location,
            hours_old,
            category,
            priority,
            recipient,
            recommendation,
            status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        food_name,
        quantity,
        location,
        hours_old,
        category,
        priority,
        recipient,
        recommendation,
        status

    ))


    conn.commit()

    conn.close()


# ============================================================
# GET ALL DONATIONS
# ============================================================

def get_donations():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""

        SELECT

            id,
            food_name,
            quantity,
            location,
            hours_old,
            category,
            priority,
            recipient,
            recommendation,
            status

        FROM donations

        ORDER BY id DESC

    """)


    data = cursor.fetchall()

    conn.close()

    return data


# ============================================================
# GET ALL RECIPIENTS
# ============================================================

def get_recipients():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""

        SELECT

            id,
            name,
            recipient_type,
            location,
            capacity,
            accepts_cooked,
            accepts_packaged,
            contact

        FROM recipients

    """)


    data = cursor.fetchall()

    conn.close()

    return data


# ============================================================
# FIND SUITABLE RECIPIENTS
# ============================================================

def find_recipients(

    quantity,
    food_category,
    location

):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    # Determine food type

    cooked = food_category.lower() in [

        "cooked food",
        "cooked meal",
        "meal"

    ]


    if cooked:

        cursor.execute("""

            SELECT

                name,
                recipient_type,
                location,
                capacity,
                contact

            FROM recipients

            WHERE accepts_cooked = 1

            AND capacity >= ?

        """, (quantity,))

    else:

        cursor.execute("""

            SELECT

                name,
                recipient_type,
                location,
                capacity,
                contact

            FROM recipients

            WHERE accepts_packaged = 1

            AND capacity >= ?

        """, (quantity,))


    data = cursor.fetchall()

    conn.close()


    return data