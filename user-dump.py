import json, os
from dotenv import load_dotenv
from telegram.client import Telegram

load_dotenv()

tg = Telegram(
    api_id=os.getenv('TELEGRAM_API_ID'),
    api_hash=os.getenv('TELEGRAM_API_HASH'),
    phone=os.getenv('PHONE'),
    database_encryption_key=os.getenv('DATABASE_ENCRYPTION_KEY'),
    files_directory=os.getenv('FILES_DIRECTORY'),
)
tg.login()

user_id = "418896318"

chats = tg.get_chats()
chats.wait()

for chat_id in chats.update["chat_ids"]:
    chat = tg.get_chat(chat_id)
    chat.wait()

    chat_type = chat.update["type"]["@type"]

    match chat_type:
        case "chatTypePrivate":
            chat_id = chat.update["type"]["user_id"]
            print(f"user {chat_id}")

        case "chatTypeBasicGroup":
            chat_id = chat.update["type"]["basic_group_id"]
            print(f"group {chat_id}")

            group_info = tg.call_method("getBasicGroupFullInfo", {"basic_group_id": chat_id})
            group_info.wait()

            members = group_info.update["members"]
            print("members: " + ", ".join(str(member['member_id']['user_id']) for member in members))
            
        case _:
            chat_id = chat.update["type"]["supergroup_id"]
            print(f"supergroup: {chat_id} (skipping)")
        
    print("=" * 30)

# chat_ids = [chat_id for chat_id in result.update["chat_ids"] if chat_id == user_id]
# print(f"{chat_ids=}")

# for chat_id in chat_ids:
#     result = tg.get_chat(chat_id)
#     result.wait()

#     print(json.dumps(result.update, indent=4))

#     user_id = result.update["type"]["user_id"]
#     print(f"{user_id=}")

tg.stop()
