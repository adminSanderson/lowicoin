use frankenstein::{Api, Message, SendMessageParams, TelegramApi};

pub async fn handle_default(api: &Api, message: Message) {
    if let Some(text) = message.text.clone() {
        let params = SendMessageParams {
            chat_id: frankenstein::ChatId::Integer(message.chat.id),
            text,
            parse_mode: None,
            entities: None,
            disable_web_page_preview: None,
            disable_notification: None,
            reply_to_message_id: None,
            allow_sending_without_reply: None,
            reply_markup: None,
        };
        let _ = api.send_message(&params);
    }
}
