from notion.client import notion

def index_callout_updator(target):

    df = target["df"]
    close = df["close"].iloc[-1]
    change = df["change"].iloc[-1]
    rate = df["rate"].iloc[-1]

    triangle = "▲" if change > 0 else "▼" if change < 0 else "-"
    symbol = "+" if change > 0 else ""
    target["color"] = "red" if change > 0 else "blue" if change < 0 else "default"
    target["text"] = f"    {close:,}                {triangle} {abs(change):,}                {symbol}{rate}%"

    call_out = notion.blocks.children.list(block_id=target["call_out_ID"])

    for i in range(len(call_out["results"])):
        notion.blocks.delete(call_out["results"][i]["id"])

    # -----------------------------------------------------------------------------------
    # NOTION BLOCK CREATE
    # -----------------------------------------------------------------------------------
    new_children = [
        # 1. heading_2
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": target["title"], "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                    }
                ],
                "is_toggleable": False,
                "color": "default",
            },
        },
        # 2. divider (구분선)
        {
            "object": "block",
            "type": "divider",
            "divider": {},
        },
        # 3. heading_3 (지수 및 변동률 텍스트)
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": target["text"],
                            "link": None,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": target["color"],
                        },
                    }
                ],
                "is_toggleable": False,
                "color": "default_background",
            },
        },
        # 4. image (차트 이미지)
        {
            "object": "block",
            "type": "image",
            "image": {
                "caption": [],
                "type": "external",
                "external": {
                    "url": target["chart_url"]
                },
            },
        },
    ]

    # 지정한 페이지 하위에 블록 추가 실행
    response = notion.blocks.children.append(
        block_id=target["call_out_ID"],
        children=new_children,
    )
