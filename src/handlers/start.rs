use crate::db;
use crate::random_16::random_string;
use frankenstein::{Api, Message, SendMessageParams, TelegramApi};

pub async fn handle_start(api: &Api, message: Message) {
    // Extract user information from the message
    let user_id = message.from.as_ref().map(|u| u.id).unwrap_or(0);
    let full_name = message
        .from
        .as_ref()
        .map(|u| u.first_name.clone())
        .unwrap_or_else(|| "User".to_string());

    let exists = db::check_user(user_id as i64).unwrap_or(false);
    let response: String;
    if !exists {
        let new_idpay = random_string(16);
        if let Err(e) = db::add_user(user_id as i64, &new_idpay, 2) {
            response = format!("Error creating user: {}", e);
        } else {
            response = format!(
                "Hello, *{}*!\nNice to meet you.\nYour profile has been *created* and we have replenished your balance with 2 lowi coins!\nTap /commands to start or /help to _... help message?_!",
                full_name
            );
        }
    } else {
        response = format!(
            "Welcome back, *{}*!\nYour profile already exists. Tap /commands to start or /help to _... help message?_!",
            full_name
        );
    }

    let params = SendMessageParams {
        chat_id: frankenstein::ChatId::Integer(message.chat.id),
        text: response,
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
