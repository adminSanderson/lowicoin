pub mod start;
pub mod commands;
pub mod payment;
pub mod profile;
pub mod default;

use frankenstein::{Api, Message};

pub async fn dispatch_message(api: &Api, message: Message) {
    if let Some(text) = message.text.clone() {
        if text.starts_with("/start") {
            start::handle_start(api, message).await;
        } else if text.starts_with("/commands") {
            commands::handle_commands(api, message).await;
        } else if text.starts_with("/pay") {
            payment::handle_pay(api, message).await;
        } else if text.starts_with("/me") || text.starts_with("/profile") {
            profile::handle_profile(api, message).await;
        } else {
            default::handle_default(api, message).await;
        }
    }
}
