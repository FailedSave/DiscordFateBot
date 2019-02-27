import stats_storage
import setting_storage

async def handle_view_stats (client, message, name, channel):
    stats_string = f"""
**Fates Served:** {stats_storage.stats["fates_delivered"]}
**Users:** {setting_storage.get_users_count()}
**Helpless Users:** {setting_storage.get_helpless_users_count()}
"""
    await client.send_message(channel, stats_string)    