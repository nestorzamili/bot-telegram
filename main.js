const TelegramBot = require("node-telegram-bot-api");
const axios = require("axios");
const express = require("express");
const dotenv = require("dotenv");

dotenv.config();

const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });
const app = express();
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("Server is running");
});

bot.on("message", (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;
  let ids;

  if (text.includes("EOD Ceria Report")) {
    ids = process.env.EOD_CERIA_REPORT_ID;
  } else if (
    text.includes("Report Autodebet") ||
    text.includes("Early CERIA")
  ) {
    ids = process.env.REPORT_AUTODEBET_ID;
  }

  if (ids) {
    const apiUrl = process.env.API_URL;
    const headers = {
      "x-api-key": process.env.API_KEY,
      ids,
      "Content-Type": "text/plain",
    };

    axios
      .post(apiUrl, text, { headers })
      .then((response) => {
        console.log(response.data);
        bot.sendMessage(chatId, response.data);
      })
      .catch((error) => {
        console.error("Gagal mengirim pesan ke API:", error);
        bot.sendMessage(chatId, "Gagal mengirim pesan ke API.");
      });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
