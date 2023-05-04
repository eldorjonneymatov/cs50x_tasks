# Telegram Public Channel Latest Messages

### Video Demo: <https://drive.google.com/file/d/1gbsbQSCdAtodgGTDGQ5f1uxO7zGERXmS/view?usp=share_link>

## Description
This project is designed to connect to a user's Telegram account using their phone number and display the latest messages from their public channels. It also tranforms cyrillic messages to latin and drops channel\`s sign.

### Background
This app is built using flask and based on cs50 finance. Changes have been made to the design part. It is registered by phone number and automatically connected to your Telegram account in the process. After entering the registration information, a confirmation code will be sent to your Telegram account, if the code is not sent within 2 minutes, click the button to resend the code. After registration, enter the system using a password and phone number. By clicking the `view message` button, all the messages that have been on the site since the last time the user visited the site are displayed, and if the message is in **Cyrillic**, it will be converted to **Latin**. In most telegram channels, the channel signature is added as a suffix to determine whether the message is advertising or not.

## Code details
To connect user\`s telegram account via his number the following function is used:
```python
async def send_code_request():
    try:
        await client.connect()
        await client.send_code_request(session['phone'])
    except:
        return
```
After the verification code is entered, it authorizes by calling the following function:
```python
async def sign_in(phone, code):
    await client.sign_in(phone, code)
```
If the code is not entered or the wrong code is entered, according to the idea of cs50, the error is stated on the apology page.

If the verification code is correct, the usernames of all the public channels that the user is a member of are obtained through the following `get_public_channels` function:
```python
async def get_public_channels():
    await client.connect()
    channels = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            channel = await client.get_entity(dialog.id)
            username = channel.username
            if username:
                channels.append(username)
    return channels
```
</br>

Channel names are retrieved by their usernames by calling the `get_channels_titles` function below in '/':
```python
async def get_channels_titles():
    global CHATS
    await client.connect()
    titles = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            channel = await client.get_entity(dialog.id)
            username = channel.username
            if username:
                titles.append({'username': username, 'title': dialog.name})
    return titles
```

If the time of his last login is not saved, it will be automatically set to the previous day:
```python
  BEGIN = session.get('last_time')
  if not BEGIN:
      yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
      BEGIN = yesterday.strftime("(%Y, %m, %d, %H, %M, %S)")
      session['last_time'] = BEGIN
```
This could be done efficiently by adding a separate column to the users table. But considering that the site was created mainly for reading the latest news, a very simple method was chosen.

Finally this method is used to get messages:
```python
async def get_messages():
    global DATA
    await client.connect()
    DATA = pd.DataFrame({"link":[], "date":[], "text":[], "ad":[]})
    BEGIN = session['last_time']
    BEGIN = string_to_tuple(BEGIN)
    BEGIN = datetime.datetime(*BEGIN)
    # Iterate through channels
    for CHAT in CHATS:
        chat = await client.get_entity(CHAT)
        links, dates, texts, ad = [], [], [], []
        # Iterate through messages in the channel
        async for message in client.iter_messages(chat, reverse=True, offset_date=BEGIN):
            if message.text:
                links.append(f"{CHAT}/{message.id}")
                dates.append(message.date)
                texts.append(cyrillic_to_latin(message.text))
        if texts: texts, ad = drop_channel_sign(texts)
        chat_df = pd.DataFrame({'link': links, 'date': dates, 'text': texts, 'ad': ad})
        DATA = pd.concat([DATA, chat_df])
    current_date_time = datetime.datetime.now()
    BEGIN = current_date_time.strftime("(%Y, %m, %d, %H, %M, %S)")
    session['last_time'] = BEGIN
    DATA.to_csv(f"{session['user_id']}_data.csv", index=False)
```