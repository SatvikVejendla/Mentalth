// NPM Packages
const Discord = require("discord.js");

const path = require("path");

// Built-in Packages
const fs = require("fs");

// User-made Modules
const classify = require("./brain/classify.js");
const getScore = require("./brain/score.js");

// Config
require("dotenv").config();

let token = process.env.DISCORD_TOKEN;

const client = new Discord.Client();
const toArray = require("./array/toArray.js");
/*
const handler = tfn.io.fileSystem("./path/to/your/model.json");
const model = await tf.loadModel(handler);*/
let users = {};

client.on("ready", () => {
  console.log(`Running as ${client.user.username}\n`);
  console.log(
    `${client.users.cache.size} users\n${client.channels.cache.size} channels\n${client.guilds.cache.size} servers`
  );
  client.user.setActivity("-help", { type: "PLAYING" });
  client.user.setUsername("Mental Health Bot");
});

client.on("message", (msg) => {
  if (msg.author.bot || msg.author == client.user) return;

  if (!users[msg.author.id]) {
    users[msg.author.id] = {
      score: 0,
      messages: [],
    };
  }

  const txt = msg.content;

  let messages = users[msg.author.id].messages;
  for (let i = messages.length - 1; i >= 0; i--) {
    if (msg.createdTimestamp - messages[i].timeStamp > 259200000) {
      users[msg.author.id].messages.splice(i, 1);
    }
  }

  classify(txt).then((i) => {
    if (i[i.length - 1].results[0].match) {
      users[msg.author.id].score++;
      users[msg.author.id].messages.push({
        content: txt,
        timeStamp: msg.createdTimestamp,
      });

      console.log("TOXIC");

      for (let i = 0; i < Object.keys(users).length; i++) {
        let elem = users[Object.keys(users)[i]];

        let id = Object.keys(users)[i];

        console.log(getScore(users, i));

        if (getScore(users, i) >= 2) {
          const embed = new Discord.MessageEmbed()
            .setColor("#FF5733")
            .setTitle(`Calm down`)
            .setDescription(
              "Cyberbullying isn't cool. It's very detrimental to the victim and can cause them to have:\n - High stress levels\n - Low self-esteem\n - Depression\n - Suicidal Thoughts"
            )
            .addField(
              "Resources",
              "If you're being bullied, here are some resources:\n[Cybersmile](https://www.cybersmile.org/advice-help/category/who-to-call)\n[Lots of resources here](https://www.aft.org/online-safety-and-cyberbullying-resources)",
              false
            )
            .addField(
              "Stop Cyberbullying",
              "[StopBullying.gov](https://www.stopbullying.gov/)",
              false
            )
            .setThumbnail(
              "https://cyberbullying.org/wp-content/uploads/2014/02/2013_cyberbullying-logo_color_b_rectangle.png"
            )
            .setTimestamp();
          msg.channel.send(`<@${id}>`);
          msg.channel.send(embed);
        }
      }
    }
  });
});

client.login(token);
