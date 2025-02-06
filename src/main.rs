mod cfg;
mod context;
mod db;
mod handlers;
mod random_16;

use cfg::API_TOKEN;
use db::init_db;
use frankenstein::{Api, BotCommand, GetUpdatesParams, SetMyCommandsParams, TelegramApi};
use handlers::dispatch_message;
use paris::Logger;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let mut log = Logger::new();
    log.add_style("err", vec!["white", "red", "bold"]);
    log.add_style("suc", vec!["white", "bright-green", "bold"]);

    let _ = match init_db() {
        Ok(_) => log.success("<suc>Connected to the db succesfuly</>"),
        Err(_) => {
            log.error("<err>Failed to connect to the db</>");
            panic!();
        }
    };

    // Create the Telegram API instance
    let api = Api::new(API_TOKEN);

    // Set bot commands
    let commands = vec![
        BotCommand {
            command: "start".to_string(),
            description: "Start the bot".to_string(),
        },
        BotCommand {
            command: "commands".to_string(),
            description: "Available commands".to_string(),
        },
        BotCommand {
            command: "me".to_string(),
            description: "Show profile".to_string(),
        },
        BotCommand {
            command: "pay".to_string(),
            description: "Make a payment".to_string(),
        },
        BotCommand {
            command: "profile".to_string(),
            description: "Show profile".to_string(),
        },
    ];
    let cmds = SetMyCommandsParams::new(commands);
    let _ = match api.set_my_commands(&cmds) {
        Ok(_) => log.success("<suc>Started the bot</>"),
        Err(_) => {
            log.error("<err>Failed to start the bot</>");
            panic!();
        }
    };

    // Poll for updates
    let mut offset = 0;
    loop {
        let params = GetUpdatesParams {
            offset: Some(offset),
            limit: None,
            timeout: Some(100),
            allowed_updates: None,
        };
        let updates = api.get_updates(&params);
        for update in updates.unwrap().result {
            offset = update.update_id + 1;
            if let Some(message) = update.message {
                dispatch_message(&api, message).await;
            }
        }
    }
}
