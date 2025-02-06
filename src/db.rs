use rusqlite::{Connection, OptionalExtension, Result};

pub fn connect() -> Result<Connection> {
    Connection::open("coins_db.db")
}

pub fn init_db() -> Result<()> {
    let conn = connect()?;
    conn.execute(
        "CREATE TABLE IF NOT EXISTS Users_coins (
            id INTEGER PRIMARY KEY,
            id_users INTEGER,
            id_pay TEXT,
            coins INTEGER
        )",
        [],
    )?;
    Ok(())
}

pub fn check_user(user_id: i64) -> Result<bool> {
    let conn = connect()?;
    let exists: Option<i64> = conn
        .query_row(
            "SELECT id_users FROM Users_coins WHERE id_users = ?1",
            [user_id],
            |row| row.get(0),
        )
        .optional()?;
    Ok(exists.is_some())
}

pub fn add_user(user_id: i64, id_pay: &str, coins: i64) -> Result<()> {
    let conn = connect()?;
    conn.execute(
        "INSERT INTO Users_coins (id_users, id_pay, coins) VALUES (?1, ?2, ?3)",
        (&user_id, id_pay, &coins),
    )?;
    Ok(())
}

pub fn get_user_balance(user_id: i64) -> Result<i64> {
    let conn = connect()?;
    let balance: Option<i64> = conn
        .query_row(
            "SELECT coins FROM Users_coins WHERE id_users = ?1",
            [user_id],
            |row| row.get(0),
        )
        .optional()?;
    Ok(balance.unwrap_or(0))
}

pub fn get_user_balance_by_idpay(user_idpay: &str) -> Result<i64> {
    let conn = connect()?;
    let balance: Option<i64> = conn
        .query_row(
            "SELECT coins FROM User_coins WHERE id_pay = ?1",
            [user_idpay],
            |row| row.get(1),
        )
        .optional()?;
    Ok(balance.unwrap_or(0))
}

pub fn get_user_idpay(user_id: i64) -> Result<Option<String>> {
    let conn = connect()?;
    let idpay: Option<String> = conn
        .query_row(
            "SELECT id_pay FROM Users_coins WHERE id_users = ?1",
            [user_id],
            |row| row.get(0),
        )
        .optional()?;
    Ok(idpay)
}

pub fn transfer_coins(
    sender_id: i64,
    receiver_idpay: &str,
    coin_amount: i64,
) -> Result<(bool, Option<i64>)> {
    let mut conn = connect()?;
    let tx = conn.transaction()?;

    let sender_balance: Option<i64> = tx
        .query_row(
            "SELECT coins FROM Users_coins WHERE id_users = ?1",
            [sender_id],
            |row| row.get(0),
        )
        .optional()?;
    let sender_balance = sender_balance.unwrap_or(0);
    if sender_balance < coin_amount {
        return Ok((false, None));
    }

    let receiver_balance: Option<i64> = tx
        .query_row(
            "SELECT coins FROM Users_coins WHERE id_pay = ?1",
            [receiver_idpay],
            |row| row.get(0),
        )
        .optional()?;
    let receiver_balance = match receiver_balance {
        Some(b) => b,
        None => return Ok((false, None)),
    };

    let new_sender_balance = sender_balance - coin_amount;
    let new_receiver_balance = receiver_balance + coin_amount;

    tx.execute(
        "UPDATE Users_coins SET coins = ?1 WHERE id_users = ?2",
        (&new_sender_balance, sender_id),
    )?;
    tx.execute(
        "UPDATE Users_coins SET coins = ?1 WHERE id_pay = ?2",
        (&new_receiver_balance, receiver_idpay),
    )?;
    tx.commit()?;
    Ok((true, Some(new_sender_balance)))
}
