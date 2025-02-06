use std::f32::NAN;

use frankenstein::{Api, Message, SendMessageParams, TelegramApi};

pub async fn handle_pay(api: &Api, message: Message) {
    let text = match message.text.clone() {
        Some(t) => t,
        None => return,
    };

    let parts: Vec<&str> = text.split_whitespace().collect();

    if parts.len() < 3 {
        let params = SendMessageParams {
            chat_id: frankenstein::ChatId::Integer(message.chat.id),
            text: "❌ Incorrect command format. Example: /pay 2 (coins) jnRHDtjlCfhNfc5b (Pay id)"
                .to_string(),
            parse_mode: None,
            entities: None,
            disable_web_page_preview: None,
            disable_notification: None,
            reply_to_message_id: None,
            allow_sending_without_reply: None,
            reply_markup: None,
        };
        let _ = api.send_message(&params);
        return;
    }

    let coin_amount = match parts[1].parse::<i64>() {
        Ok(val) => val,
        Err(_) => {
            let params = SendMessageParams {
                chat_id: frankenstein::ChatId::Integer(message.chat.id),
                text: "❌ Specify the correct number for coin.".to_string(),
                parse_mode: None,
                entities: None,
                disable_web_page_preview: None,
                disable_notification: None,
                reply_to_message_id: None,
                allow_sending_without_reply: None,
                reply_markup: None,
            };
            let _ = api.send_message(&params);
            return;
        }
    };

    if coin_amount == 0 {
        let params = SendMessageParams {
            chat_id: frankenstein::ChatId::Integer(message.chat.id),
            text: "❌ Minimum transfer amount: 1 coin.".to_string(),
            parse_mode: None,
            entities: None,
            disable_web_page_preview: None,
            disable_notification: None,
            reply_to_message_id: None,
            allow_sending_without_reply: None,
            reply_markup: None,
        };
        let _ = api.send_message(&params);
        return;
    }

    let user_key = parts[2];
    let sender_id = message.from.as_ref().map(|u| u.id).unwrap_or(0);

    let sender_balance = crate::db::get_user_balance(sender_id as i64).unwrap_or(0);
    if sender_balance < coin_amount {
        let params = SendMessageParams {
            chat_id: frankenstein::ChatId::Integer(message.chat.id),
            text: "❌ There are not enough coins to transfer.".to_string(),
            parse_mode: None,
            entities: None,
            disable_web_page_preview: None,
            disable_notification: None,
            reply_to_message_id: None,
            allow_sending_without_reply: None,
            reply_markup: None,
        };
        let _ = api.send_message(&params);
        return;
    }
    if crate::db::get_user_idpay(sender_id as i64)
        .unwrap()
        .unwrap()
        == user_key
    {
        let params = SendMessageParams {
            chat_id: frankenstein::ChatId::Integer(message.chat.id),
            text: "❌ Can't send coins to yourself".to_string(),
            parse_mode: None,
            entities: None,
            disable_web_page_preview: None,
            disable_notification: None,
            reply_to_message_id: None,
            allow_sending_without_reply: None,
            reply_markup: None,
        };
        let _ = api.send_message(&params);
        return;
    }

    let (success, new_sender_balance) =
        crate::db::transfer_coins(sender_id as i64, user_key, coin_amount).unwrap_or((false, None));
    if !success {
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
        return;
    }

    let response = format!(
        "✅ Successfully transferred {} tokens to the user with the ID PAY {}.\n💳 Your new balance: {} coins.",
        coin_amount,
        user_key,
        new_sender_balance.unwrap_or(sender_balance)
    );
    let params = SendMessageParams {
        chat_id: frankenstein::ChatId::Integer(message.chat.id),
        text: response,
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
