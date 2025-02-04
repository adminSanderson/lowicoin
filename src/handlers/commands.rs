use frankenstein::{Api, Message, SendMessageParams, TelegramApi};
use crate::context::COMMANDS_TEXT;

pub async fn handle_commands(api: &Api, message: Message) {
    let params = SendMessageParams {
        chat_id: frankenstein::ChatId::Integer(message.chat.id),
        text: COMMANDS_TEXT.to_string(),
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
