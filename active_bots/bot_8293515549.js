const { Telegraf, Markup } = require('telegraf');
const fs = require('fs');

// البيانات المتغيرة التي سيتم استبدالها تلقائياً عند الصنع
const BOT_TOKEN = "8975709913:AAE9T9OnxtzYhgZhbr0g61c0OS9fjm7SGsY";
const OWNER_ID = 8293515549;
const MAIN_MAKER_NAME = "• 𝐀𝐒𝐓𝐀 𝐅𝐀𝐂𝐓𝐎𝐑𝐘 •"; 
const MAIN_MAKER_LINK = "https://t.me/tsuoxbot"; 

const bot = new Telegraf(BOT_TOKEN);

// إعدادات البوت الخاص بالمستخدم (مخزنة محلياً)
let botSettings = {
  requiredChannel: "" // قناة الاشتراك الإجباري الخاصة بهذا البوت
};

// --- 1. فحص الاشتراك الإجباري ---
async function checkSubscription(ctx, userId) {
  if (!botSettings.requiredChannel) return true; // لا توجد قناة مضافة
  try {
    const member = await ctx.telegram.getChatMember(botSettings.requiredChannel, userId);
    return ['creator', 'administrator', 'member'].includes(member.status);
  } catch (e) {
    return true; // في حال وجود خطأ في معرف القناة
  }
}

// --- 2. أمر البداية /start ---
bot.start(async (ctx) => {
  const userId = ctx.from.id;

  // التحقق من الاشتراك الإجباري للمستخدم العادي
  const isSubscribed = await checkSubscription(ctx, userId);
  if (!isSubscribed) {
    return ctx.reply(
      `⚠️ **عذراً، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:**\n${botSettings.requiredChannel}`,
      Markup.inlineKeyboard([
        [Markup.button.url('🔗 اضغط هنا للاشتراك', `https://t.me/${botSettings.requiredChannel.replace('@', '')}`)],
        [Markup.button.callback('✅ تحقق من الاشتراك', 'check_sub')]
      ])
    );
  }

  // رسالة الترحيب الرئيسية مع إظهار اسم الصانع كرابط مباشر بدون أي زيادات
  let text = `مرحباً بك في البوت! 👋\n\n`;
  text += `[${MAIN_MAKER_NAME}](${MAIN_MAKER_LINK})`;

  let buttons = [];

  // إذا كان المستخدم هو صانع البوت نفسه، تظهر له لوحة التحكم
  if (userId === OWNER_ID) {
    buttons.push([Markup.button.callback('🎛 لوحة تحكم البوت', 'admin_panel')]);
  }

  ctx.replyWithMarkdown(text, Markup.inlineKeyboard(buttons));
});

// زر التحقق من الاشتراك الإجباري
bot.action('check_sub', async (ctx) => {
  const isSubscribed = await checkSubscription(ctx, ctx.from.id);
  if (isSubscribed) {
    ctx.answerCbQuery('✅ تم التحقق بنجاح! يمكنك الآن استخدام البوت.');
    ctx.deleteMessage();
    ctx.reply(`مرحباً بك! البوت جاهز للاستخدام.\n\n[${MAIN_MAKER_NAME}](${MAIN_MAKER_LINK})`, { parse_mode: 'Markdown' });
  } else {
    ctx.answerCbQuery('❌ لم تشترك في القناة بعد!', { show_alert: true });
  }
});

// --- 3. لوحة تحكم مالك البوت (Admin Panel) ---
bot.action('admin_panel', (ctx) => {
  if (ctx.from.id !== OWNER_ID) return ctx.answerCbQuery('غير مسموح لك!');

  const text = `🎛 **لوحة تحكم البوت الخاص بك**\n\n` +
               `📢 **القناة الإجبارية الحالية:** ${botSettings.requiredChannel || "لا يوجد"}\n` +
               `👑 **المالك:** ${OWNER_ID}\n` +
               `[${MAIN_MAKER_NAME}](${MAIN_MAKER_LINK})`;

  ctx.editMessageText(text, {
    parse_mode: 'Markdown',
    ...Markup.inlineKeyboard([
      [Markup.button.callback('📢 تعيين / تغيير القناة الإجبارية', 'set_channel')],
      [Markup.button.callback('🗑 إزالة القناة الإجبارية', 'remove_channel')],
      [Markup.button.callback('❌ إغلاق', 'close')]
    ])
  });
});

// تعيين القناة الإجبارية
let awaitingChannel = {};
bot.action('set_channel', (ctx) => {
  if (ctx.from.id !== OWNER_ID) return;
  awaitingChannel[ctx.from.id] = true;
  ctx.reply('أرسل الآن يوزر القناة مع علامة @ (مثال: @MyChannel):');
});

bot.on('text', (ctx) => {
  const userId = ctx.from.id;
  
  // حفظ القناة الإجبارية عند إرسالها من المالك
  if (awaitingChannel[userId]) {
    botSettings.requiredChannel = ctx.text.trim();
    delete awaitingChannel[userId];
    return ctx.reply(`✅ تم تعيين القناة الإجبارية بنجاح إلى: ${botSettings.requiredChannel}`);
  }
});

// إزالة القناة الإجبارية
bot.action('remove_channel', (ctx) => {
  if (ctx.from.id !== OWNER_ID) return;
  botSettings.requiredChannel = "";
  ctx.reply('✅ تم إزالة القناة الإجبارية بنجاح.');
});

bot.action('close', (ctx) => ctx.deleteMessage());

bot.launch();
