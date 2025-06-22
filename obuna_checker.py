async def check_subscription(user_id, bot):
    try:
        member = await bot.get_chat_member(chat_id='@zakovatprogr', user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
