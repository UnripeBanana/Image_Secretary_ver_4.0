from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할

def get_all_pages(database_id):
    pages = []
    cursor = None

    while True:
        if cursor:
            response = notion.databases.query(
                database_id=database_id,
                start_cursor=cursor
            )
        else:
            response = notion.databases.query(
                database_id=database_id
            )

        pages.extend(response["results"])

        if not response["has_more"]:
            break

        cursor = response["next_cursor"]

    return pages
