import asyncio
import hjson
import time
from telethon import TelegramClient
import datetime
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
import os
import ctypes

with open('settings.json') as f:
    settings = hjson.load(f)

def CheckFolders():
    if os.path.exists('data'):
        if os.path.exists('data\\Result') == 0:
            os.mkdir('data\\Result')
        if os.path.exists('data\\TelethonSessions') == 0:
            os.mkdir('data\\TelethonSessions')
    else:
        os.mkdir('data')
        if os.path.exists('data\\Result') == 0:
            os.mkdir('data\\Result')
        if os.path.exists('data\\TelethonSessions') == 0:
            os.mkdir('data\\TelethonSessions')

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printf(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {message}')


async def dump_members():
    printf('Connecting to the account...')
    async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:

        printf('Connected!')

        if os.path.exists(f"data\\Result\\{settings['group_id']}_from_members.txt") != 1:
            countofusers = 0
            printf('Started scrapping from group user list...')
            all_participants = await client.get_participants(settings['group_id'], aggressive=True)
            with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'a') as f:
                for member in all_participants:
                    if member.username != None:
                        countofusers += 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Scrapping... | Scrapped {countofusers}")
                        f.write(f"{member.username}\n")
                f.close()
            printf(f'Scrapped {len(all_participants)} usernames')

            ctypes.windll.kernel32.SetConsoleTitleW(f"Scrapped {countofusers} users! | Adding to your group...")

            with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'r') as f:
                sender_usernames = f.readlines()
                printf(f'Loaded {len(sender_usernames)} usernames')
            entity_group = await client.get_entity(settings['group_to_invite'])

            for user in sender_usernames:
                try:
                    result = await client(AddChatUserRequest(
                        entity_group.id,
                        user_id=user,
                        fwd_limit=100
                    ))
                    printf(f'Added @{user[:-1]} to group')
                    countofusers -= 1
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                    time.sleep(settings['timeout'])
                except Exception as e:
                    if 'is not a mutual contact' in str(e):
                        printf(f'Cant add @{user[:-1]} because hes not in mutual contacts')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'privacy settings' in str(e):
                        printf(f'The @{user[:-1]} privacy settings does not allow add him to group')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'seconds' in str(e):
                        printf(
                            f'Got telegram timeout error, need to wait {str(e).split(" ")[3]} seconds, to continue adding (recommend to change account)...')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(int(str(e).split(" ")[3]))
                    elif 'already' in str(e):
                        printf(f'The user @{user[:-1]} is already in group')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    else:
                        printf(e)
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])

        else:
            printf(f"Seems that {settings['group_id']} members are already scrapped, loading them...")
            with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'r') as f:
                sender_usernames = f.readlines()
                printf(f'Loaded {len(sender_usernames)} usernames')
                countofusers = len(sender_usernames)
                ctypes.windll.kernel32.SetConsoleTitleW(f"Loaded {countofusers} users! | Adding to your group...")
            entity_group = await client.get_entity(settings['group_to_invite'])

            for user in sender_usernames:
                try:
                    await client(AddChatUserRequest(
                        entity_group.id,
                        user_id=user,
                        fwd_limit=100
                    ))
                    printf(f'Added @{user[:-1]} to group')
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                    countofusers -= 1
                    time.sleep(settings['timeout'])
                except Exception as e:
                    if 'is not a mutual contact' in str(e):
                        printf(f'Cant add @{user[:-1]} because hes not in mutual contacts')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'privacy settings' in str(e):
                        printf(f'The @{user[:-1]} privacy settings does not allow add him to group')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'seconds' in str(e):
                        printf(
                            f'Got telegram timeout error, need to wait {str(e).split(" ")[3]} seconds, to continue adding (recommend to change account)...')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(int(str(e).split(" ")[3]))
                    elif 'already' in str(e):
                        printf(f'The user @{user[:-1]} is already in group')
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(int(str(e).split(" ")[3]))
                    else:
                        printf(e)
                        countofusers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofusers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])

async def dump_from_messages():
    printf('Connecting to the account...')
    async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:
        printf('Connected!')
        printf('Started scrapping from messages...')
        sender_ids = []

        if os.path.exists(f"data\\Result\\{settings['group_id']}_from_messages.txt") != 1:
            countofmembers = 0
            with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'a') as f:
                async for message in client.iter_messages(settings['group_id']):
                        try:
                            if message.from_id.user_id not in sender_ids:
                                sender_ids.append(message.from_id.user_id)
                                username = await client.get_entity(message.from_id.user_id)
                                if username.username != None:
                                    countofmembers+=1
                                    ctypes.windll.kernel32.SetConsoleTitleW(f"Scrapping... | Scrapped {countofmembers}")
                                    f.write(f"{username.username}\n")
                        except:
                            continue
                f.close()

                with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'r') as f:
                    sender_usernames = f.readlines()
                    printf(f'Loaded {len(sender_usernames)} uniq ids')
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Loaded {countofmembers} users | Start adding")
                entity_group = await client.get_entity(settings['group_to_invite'])

                for user in sender_usernames:
                    try:
                        await client(AddChatUserRequest(
                            entity_group.id,
                            user_id=user,
                            fwd_limit=100
                        ))
                        printf(f'Added @{user[:-1]} to group')
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['timeout'])
                    except Exception as e:
                        if 'is not a mutual contact' in str(e):
                            printf(f'Cant add @{user[:-1]} because hes not in mutual contacts')
                            countofmembers -= 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f"Left {countofmembers}\\{len(sender_usernames)} to add")
                            time.sleep(settings['error_timeout'])
                        elif 'privacy settings' in str(e):
                            printf(f'The @{user[:-1]} privacy settings does not allow add him to group')
                            countofmembers -= 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f"Left {countofmembers}\\{len(sender_usernames)} to add")
                            time.sleep(settings['error_timeout'])
                        elif 'seconds' in str(e):
                            printf(
                                f'Got telegram timeout error, need to wait {str(e).split(" ")[3]} seconds, to continue adding (recommend to change account)...')
                            countofmembers -= 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f"Left {countofmembers}\\{len(sender_usernames)} to add")
                            time.sleep(int(str(e).split(" ")[3]))
                        elif 'already' in str(e):
                            printf(f'The user @{user[:-1]} is already in group')
                            countofmembers -= 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f"Left {countofmembers}\\{len(sender_usernames)} to add")
                            time.sleep(settings['error_timeout'])
                        else:
                            printf(e)
                            countofmembers -= 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f"Left {countofmembers}\\{len(sender_usernames)} to add")
                            time.sleep(settings['error_timeout'])

        else:
            printf(f"Seems that {settings['group_id']} members are already scrapped, loading them...")
            with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'r') as f:
                sender_usernames = f.readlines()
                printf(f'Loaded {len(sender_usernames)} uniq ids')
                countofmembers = len(sender_usernames)
                ctypes.windll.kernel32.SetConsoleTitleW(f"Loaded {countofmembers} users! | Adding to your group...")
            entity_group = await client.get_entity(settings['group_to_invite'])
            for user in sender_usernames:
                try:
                    await client(AddChatUserRequest(
                        entity_group.id,
                        user_id=user,
                        fwd_limit=100
                    ))
                    printf(f'Added @{user[:-1]} to group')
                    countofmembers -= 1
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Left {countofmembers}\\{len(sender_usernames)} to add")
                    time.sleep(settings['timeout'])
                except Exception as e:
                    if 'is not a mutual contact' in str(e):
                        printf(f'Cant add @{user[:-1]} because hes not in mutual contacts')
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'privacy settings' in str(e):
                        printf(f'The @{user[:-1]} privacy settings does not allow add him to group')
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    elif 'seconds' in str(e):
                        printf(
                            f'Got telegram timeout error, need to wait {str(e).split(" ")[3]} seconds, to continue adding (recommend to change account)...')
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(int(str(e).split(" ")[3]))
                    elif 'already' in str(e):
                        printf(f'The user @{user[:-1]} is already in group')
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])
                    else:
                        printf(e)
                        countofmembers -= 1
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Left {countofmembers}\\{len(sender_usernames)} to add")
                        time.sleep(settings['error_timeout'])


async def add_to_supergroup_from_messages():
    printf('Connecting to the account...')
    async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:
        printf('Connected!')
        printf(f"Seems that {settings['group_id']} members are already scrapped, loading them...")
        with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'r') as f:
            sender_usernames = f.readlines()
            printf(f'Loaded {len(sender_usernames)} uniq ids')
            countofmembers = len(sender_usernames)
            ctypes.windll.kernel32.SetConsoleTitleW(f"Loaded {countofmembers} users! | Adding to your group...")

        entity_group = await client.get_entity(settings['group_to_invite'])

        sender_entities = []
        count = 0

        for user in sender_usernames:
            sender_entities.append(await client.get_entity(user))
            sender_usernames.remove(user)

            count += 1
            if count % settings['supergroup_add'] == 0 or len(sender_usernames) < settings['supergroup_add']:
                sender_entities = list(sender_entities)
                try:
                    response = await client(InviteToChannelRequest(
                        entity_group,
                        sender_entities
                    ))
                    sender_entities.clear()
                    time.sleep(settings['timeout'])
                except Exception as e:
                    printf(e)

async def add_to_supergroup_from_members():
    printf('Connecting to the account...')
    async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:
        printf('Connected!')
        printf(f"Seems that {settings['group_id']} members are already scrapped, loading them...")
        with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'r') as f:
            sender_usernames = f.readlines()
            printf(f'Loaded {len(sender_usernames)} uniq ids')
            countofmembers = len(sender_usernames)
            ctypes.windll.kernel32.SetConsoleTitleW(f"Loaded {countofmembers} users! | Adding to your group...")

        entity_group = await client.get_entity(settings['group_to_invite'])

        sender_entities = []
        count = 0

        for user in sender_usernames:
            sender_entities.append(await client.get_entity(user))
            sender_usernames.remove(user)

            count += 1
            if count % settings['supergroup_add'] == 0 or len(sender_usernames) < settings['supergroup_add']:
                sender_entities = list(sender_entities)
                try:
                    response = await client(InviteToChannelRequest(
                        entity_group,
                        sender_entities
                    ))
                    sender_entities.clear()
                    time.sleep(settings['timeout'])
                except Exception as e:
                    printf(e)

def returnonlytrue(data):
    info = []
    data = {"id": data.id, "username": data.username, "first_name": data.first_name, "last_name": data.first_name, "phone": data.phone}
    for key in data.keys():
        for setting in settings.keys():
            if settings[setting] == True or settings[setting] == False:
                if settings[setting] == True:
                    if setting == key:
                        if data[key] != None:
                            info.append(data[key])
    info = list(map(str, info))
    return info
async def scrape_From_Members():
    printf('Connecting to the account...')
    try:
        async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:
            printf('Connected!')
            printf('Started scrapping from group user list...')
            all_participants = await client.get_participants(settings['group_id'], aggressive=True)
            for member in all_participants:
                with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'a') as f:
                    try:
                        if len(returnonlytrue(member)) > 0:
                            f.write(settings['seperate_symbols'].join(returnonlytrue(member)) + '\n')
                        else:
                            continue
                    except:
                        if {member.username} != 'None':
                            printf(f'Cant save @{member.username}, because of emojis in name. Turn off scrapping first and last names, to save this user.')
                        else:
                            printf(
                                f'Cant save user with id: {member.id}, because of emojis in name. Turn off scrapping first and last names, to save this user.')
            with open(f"data\\Result\\{settings['group_id']}_from_members.txt", 'r') as f:
                printf(f'Scrapped {len(f.readlines())} users...')
                a = f"data\\Result\\{settings['group_id']}_from_members.txt"
                printf(f'Saved all in {a}')
    except Exception as e:
        printf(str(e))
        time.sleep(2)


async def scrape_from_messages():
    printf('Connecting to the account...')
    try:
        async with TelegramClient('data\\TelethonSessions\\Session', settings['api_id'], settings['api_hash']) as client:
            printf('Connected!')
            printf('Started scrapping from messages...')

            sender_ids = []

            async for message in client.iter_messages(settings['group_id']):
                try:
                    if message.from_id.user_id not in sender_ids:
                        sender_ids.append(message.from_id.user_id)

                        data = await client.get_entity(message.from_id.user_id)

                        with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'a') as f:
                            try:
                                if len(returnonlytrue(data)) > 0:
                                    f.write(settings['seperate_symbols'].join(returnonlytrue(data)) + '\n')
                                else:
                                    continue
                            except:
                                if {data.username} != 'None':
                                    printf(f'Cant save @{data.username}, because of emojis in name. Turn off scrapping first and last names, to save this user.')
                                else:
                                    printf(f'Cant save user with id: {data.id}, because of emojis in name. Turn off scrapping first and last names, to save this user.')

                except: continue

            with open(f"data\\Result\\{settings['group_id']}_from_messages.txt", 'r') as f:
                printf(f'Scrapped {len(f.readlines())} users...')
                a = f"data\\Result\\{settings['group_id']}_from_messages.txt"
                printf(f'Saved all in {a}')

    except Exception as e:
        printf(str(e))
        time.sleep(2)

if __name__ == '__main__':
    CheckFolders()
    print('[1] Add & Scrape to regular group from members')
    print('[2] Add & Scrape to regular group from messages')
    print()
    print('[3] Add to supergroup from messages')
    print('[4] Add to supergroup from members')
    print()
    print('[5] Scrape from members')
    print('[6] Scrape from messages')
    choice = input()
    cls()
    if choice == str(1):
        asyncio.run(dump_members())
        printf('Done...')
        input()
    elif choice == str(2):
        asyncio.run(dump_from_messages())
        printf('Done...')
        input()
    elif choice == str(3):
        asyncio.run(add_to_supergroup_from_messages())
        printf('Done...')
        input()
    elif choice == str(4):
        asyncio.run(add_to_supergroup_from_members())
        printf('Done...')
        input()
    elif choice == str(5):
        asyncio.run(scrape_From_Members())
        printf('Done...')
        input()
    elif choice == str(6):
        asyncio.run(scrape_from_messages())
        printf('Done...')
        input()