use chrono::Local;
use frankenstein::{Api, Message, SendMessageParams, TelegramApi};

pub async fn handle_profile(api: &Api, message: Message) {
    let parts = message
        .text()
        .unwrap()
        .split_whitespace()
        .into_iter()
        .collect::<String>();
    if parts.len() == 1 as usize {
        crate::handlers::me::handle_me(api, message).await;
        return;
    };
    let user_id = message.from.as_ref().map(|u| u.id).unwrap_or(0);
    let full_name = message
        .from
        .as_ref()
        .map(|u| u.first_name.clone())
        .unwrap_or_else(|| "User".to_string());

    let balance = crate::db::get_user_balance(user_id as i64).unwrap_or(0);
    let idpay = crate::db::get_user_idpay(user_id as i64)
        .unwrap_or(None)
        .unwrap_or_else(|| "Unknown".to_string());

    let now = Local::now();
    let date = now.format("%Y-%m-%d").to_string();
    let time = now.format("%H:%M:%S").to_string();

    let profile_text = format!(
        "👤 *{}'s* profile\n\n*ID PAY:* `{}`\n*Date:* {}, {}\n*Balance:* {}",
        full_name, idpay, date, time, balance
    );

    let params = SendMessageParams {
        chat_id: frankenstein::ChatId::Integer(message.chat.id),
        text: profile_text,
        parse_mode: Some("Markdown".to_string()),
        entities: None,
        disable_web_page_preview: None,
        disable_notification: None,
        reply_to_message_id: None,
        allow_sending_without_reply: None,
        reply_markup: None,
    };
    let _ = api.send_message(&params);
}
