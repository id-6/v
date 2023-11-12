from config import Config 
from requests import Session
from requests import Response
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from re import Pattern, findall, compile as compiler


app = Client(
    "Views",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN 
)
s = Session()
pattern: str = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
DEV = InlineKeyboardMarkup([
    [InlineKeyboardButton("- المطور -", user_id=6673736816)]
])

@app.on_message(filters.command("start"))
async def start(_: Client, message: Message) -> None:
    await message.reply(
        "- مرحبا بك في بوت رشق مشاهدات تليجرام.\n- قم بإرسال رابط ليتم الرشق اليه.\n- يمكنك ارسال اكثر من رابط بنفس الرساله.\n- ممنوع تكرار الرابط (سيتم حظر القناه تلقائيا)",
        reply_to_message_id=message.id,
        reply_markup=DEV
    )

@app.on_message(filters.regex(pattern))
async def receiver(_: Client, message: Message) -> None:
    compiled_p: Pattern = compiler(pattern)
    matches: list = findall(compiled_p, message.text)
    if not matches: return await message.reply("- لم يتم العثور على اي رابط.", reply_to_message_id=message.id, reply_markup=DEV)
    wait: Message = await message.reply("- جارٍ الرشق....", reply_to_message_id=message.id, reply_markup=DEV, )
    for match in matches:
        await wait.edit_text(f"- جارٍ الرشق إلى : \n- {match}")
        response: bool = views(match)
        if not response: matches.remove(match)
        await wait.edit_text(f"- تم رشق المشاهدات إلى: \n- {match}" if response else f"- حدث خطأ اثناء الرشق الى: \n- {matches[0]}")
        await sleep(0.5)
    if len(matches) == 1: return
    caption: str = "- انتهى رشق المشاهدات إلى الروابط التاليه:\n- "
    urls: str = "\n- ".join(matches)
    caption += urls
    await wait.edit_text(caption)


def views(tgurl: str) -> bool:
    params: dict = {
        "jack" : tgurl
    }
    url: str = "https://ava-tar.online/api/kro" # API owner: @uu4uo
    response: Response = s.get(url, params=params).json()
    return True if "تم الرشق بنجاح" in response["text"] else False


# 𝗪𝗥𝗜𝗧𝗧𝗘𝗡 𝗕𝗬 : @BENN_DEV, @UP_UO 
# 𝗦𝗢𝗨𝗥𝗖𝗘 : @BENfiles , @UI_XB 
if __name__ == "__main__": app.run()