pub mod commands;
pub mod default;
pub mod me;
pub mod payment;
pub mod profile;
pub mod start;
use frankenstein::{Api, Message};

pub async fn dispatch_message(api: &Api, message: Message) {
    if let Some(text) = message.text.clone() {
        if text.starts_with("/start") {
            start::handle_start(api, message).await;
        } else if text.starts_with("/commands") {
            commands::handle_commands(api, message).await;
        } else if text.starts_with("/pay") {
            payment::handle_pay(api, message).await;
        } else if text.starts_with("/me") {
            me::handle_me(api, message).await;
        } else if text.starts_with("/profile") {
            profile::handle_profile(api, message).await;
        } else {
            default::handle_default(api, message).await;
        }
    }
}
