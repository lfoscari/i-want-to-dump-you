import json, os, time
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

user_id = 418896318

# Call get_user to load the user info

user = tg.get_user(user_id)
user.wait()

# Download all the text from the private chat

history = []
messages = []

offset = 0
from_message_id = 0

while True:
    if offset <= -100:
        offset = 0
        from_message_id = messages[-1]["id"]
    
    part_history = tg.call_method("getChatHistory", {
        "chat_id": user_id,
        "from_message_id": from_message_id,
        "offset": offset,
        "limit": 100,
        "only_local": True
    })
    part_history.wait()

    if part_history.error_info is not None:
        # TODO: Even if it's likely a flood error, you but should check
        print(part_history.error_info)
        print(f"Downloaded {-offset} messages, now sleeping a little bit...")
        time.sleep(30)
    
    messages = part_history.update["messages"]

    # TODO: Filter out non-text messages
    history.extend([m["content"] for m in messages])

    # Testing
    if len(history) > 100:
        break

    if len(messages) == 0:
        break
    
    offset -= len(messages)

for h in history:
    print(json.dumps(h, indent=2))

# Download all the text from groups in common

# chats = tg.call_method("getGroupsInCommon", {"user_id": user_id, "offset_chat_id": 0, "limit": 99})
# chats.wait()
# chats = chats.update["chat_ids"]

# print(chats)



# chats = tg.get_chats()
# chats.wait()

# for chat_id in chats.update["chat_ids"]:
#     chat = tg.get_chat(chat_id)
#     chat.wait()

#     chat_type = chat.update["type"]["@type"]

#     match chat_type:
#         case "chatTypePrivate":
#             chat_id = chat.update["type"]["user_id"]
#             print(f"user {chat_id}")

#         case "chatTypeBasicGroup":
#             chat_id = chat.update["type"]["basic_group_id"]
#             print(f"group {chat_id}")

#             group_info = tg.call_method("getBasicGroupFullInfo", {"basic_group_id": chat_id})
#             group_info.wait()

#             members = group_info.update["members"]
#             print("members: " + ", ".join(str(member['member_id']['user_id']) for member in members))
            
#         case _:
#             chat_id = chat.update["type"]["supergroup_id"]
#             print(f"supergroup: {chat_id} (skipping)")
        
#     print("=" * 30)

tg.stop()
