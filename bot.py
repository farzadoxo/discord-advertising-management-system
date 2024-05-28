from discord import (app_commands , Intents  , Interaction ,
                      Status , Activity , ActivityType ,
                        ButtonStyle , TextStyle , Member ,
                        Embed , Colour , SelectOption , Emoji)
from discord.ext.commands import Bot , has_permissions
from discord.ext import commands
from discord.ui import (Button , View , Modal , TextInput)
import datetime
from datacenter import DataBase




client = Bot(command_prefix="!",
             intents=Intents.all(),
             status=Status.online,
             activity=Activity(type=ActivityType.watching , name="Ads 📈"))


def sign_up(user_id:int):
    try:
        DataBase.cursor.execute(f"INSERT INTO table1 VALUES ({user_id} , 500 , 0 , 0)")
        DataBase.connection.commit()
    except:
        pass



@client.event
async def on_ready():
    print("Bot is online !")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} command synced successfully.")
    except Exception as error :
        print(error)




welcome_embed = Embed(title="به نظر کاربر جدید هستی :thinking:",
description="""**سلام کاربر عزیز ، به سیستم تبلیغاتی ما خوش اومدی!
اینجا میتونی به صورت کاملن رایگان هر بنر تبلیغاتی رو به راحتی تبلیغ کنی 👍🏼
با استفاده از خدمات ما میتونی سرور دیسکورد ، صفحات اجتماعی ، محصولات ، فروشگاهتو به راحتی تبلیغ کنی و ویو ، ممبر ، مشتری و... جذب کنی !😎
\n**""",color=Colour.gold())
welcome_embed.set_footer(text="ثبت نام شما با موفقیت انجام شد ✅")
welcome_embed.add_field(name=" 🔰 از کجا شروع کنم؟",value="""برای اطلاعات بیشتر در مورد خدمات تبلیغاتی ما و آموزش کارکردن با بات از دستور `help/` استفاده کنید """)



# class DataExtractor:
#     def __init__(self , userid:int):
#         self.userid = userid

#     DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {.userid}")
#     item = DataBase.cursor.fetchone()
#     try:
#         # User Data
#         user_balance = item[1]
#         user_ads = item[2]
#         user_warn = item[3]
#     except:
#         pass

    

    



@client.tree.command(name="order",description="سفارش تبلیغات 📮")
async def order(interaction:Interaction):
    ad_channel = client.get_channel(1224577122555920405)

    DataBase.cursor.execute(f"SELECT userid , balance , count FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    try:
        user_balance = item[1]
        user_ad_count = item[2]
    except:
        pass
    

    seen_button = Button(label="Seen",emoji="👁‍🗨")
    report_button = Button(label="Report",emoji="🚫",style=ButtonStyle.gray)

    async def seen_button_callback(interaction:Interaction):
        try:
            DataBase.cursor.execute(f"SELECT userid , balance , count FROM table1 WHERE userid = {interaction.user.id}")
            items = DataBase.cursor.fetchone()

            user_balance = items[1]
            
            if items == None:
                sign_up(user_id=interaction.user.id)
                await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
            else:
                DataBase.cursor.execute(f"UPDATE table1 SET balance = {user_balance + 10} WHERE userid = {interaction.user.id}")
                DataBase.connection.commit()
                
                await interaction.response.send_message("**10 سکه گرفتی 🤑**",ephemeral=True)
                
        except :
            pass


    async def report_button_callback(interaction:Interaction):
        report_channel = client.get_channel(1226883862924365947)

        report_embed = Embed(title="New report ❗",color=Colour.red())
        report_embed.add_field(name="Reported By : ",value=f"{interaction.user.mention}",inline=False)
        report_embed.add_field(name="For :" , value=interaction.message.jump_url,inline=False)

        try:
            await report_channel.send(embed=report_embed)
        except:
            pass
        await interaction.response.send_message("**گزارش جهت بررسی برای تیم مادریتور ارسال شد. لطفا از اسپم خودداری کنید ✅**",ephemeral=True)


    
    seen_button.callback = seen_button_callback
    report_button.callback = report_button_callback

    banner_view = View(timeout=None)
    banner_view.add_item(seen_button)
    banner_view.add_item(report_button)
    
    

    class BannerModal(Modal , title="ارسال بنر"):
        banner = TextInput(label="متن یا بنر تبلیغاتی خود را وارد کنید :",required=True,style=TextStyle.paragraph)

        async def on_submit(self, interaction: Interaction):
           
           try:
               banner_info_embed = Embed(color=Colour.random())
               banner_info_embed.add_field(name="👤 Owner :",value=f"{interaction.user.mention}")
               banner_info_embed.add_field(name="🕐 At :" , value=f"{datetime.datetime.now()}")
               await ad_channel.send(self.banner,view=banner_view,embed=banner_info_embed,delete_after=86400)
               DataBase.cursor.execute(f"UPDATE table1 SET balance = {user_balance - 500} , count = {user_ad_count + 1} WHERE userid = {interaction.user.id}")
               DataBase.connection.commit()
               await interaction.response.send_message("**بنر با موفقیت ارسال شد و مقدار 500 سکه از حساب شما کسر شد ✅**",ephemeral=True)
           except Exception as error:
               print(error)
               

    accept_button = Button(label="ثبت سفارش",emoji="✔",style=ButtonStyle.blurple)
    order_view = View(timeout=None)
    order_view.add_item(accept_button)

    async def accept_button_callback(interaction:Interaction):
        await interaction.response.send_modal(BannerModal())
    
    accept_button.callback = accept_button_callback

    

    if item == None:
        sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        if user_balance < 500:
            await interaction.response.send_message("**به اندازه کافی سکه نداری 💰**",ephemeral=True)
        else:
            order_embed = Embed(title="**لطفا موارد زیر را مطالعه کنید**",color=0xffffff)
            order_embed.add_field(name="📛1." , value="**ارسال هرگونه بنر حاوی محتوای جنسی ، کودک آزاری و ... ممنوع میشود**",inline=False)
            order_embed.add_field(name="📛2." , value="**بنر ارسال شده قابل ویرایش نیست! در ارسال بنر دقت کنید.**",inline=False)
            order_embed.add_field(name="📛3." , value="**موضوع بنر ارسالی میتواند تبلیغ سرور دیسکورد ، چنل یوتوب ، سایت و ... باشد**",inline=False)
            order_embed.add_field(name="در صورت تایید موارد بالا از دکمه ثبت سفارش استفاده کنید ✅",value="\ub200")
            await interaction.response.send_message(embed=order_embed,view=order_view,ephemeral=True)







@client.tree.command(name="account_info",description="اطلاعات کاربری من 📋")
async def account_info(interaction:Interaction):
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    if item == None:
        sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        account_info_embed = Embed(title="**اطلاعات حساب کاربری شما به صورت زیر میباشد :**",color=Colour.blue())
        account_info_embed.set_author(name=interaction.user.name,icon_url=interaction.user.avatar)
        account_info_embed.add_field(name="🆔 UserID :",value=interaction.user.id,inline=False)
        account_info_embed.add_field(name="💰 Coins :" ,value=item[1],inline=False)
        account_info_embed.add_field(name="🏷 Ads :",value=item[2],inline=False)
        account_info_embed.add_field(name="⚠ Warnings :",value=item[3],inline=False)
        await interaction.response.send_message(embed=account_info_embed,ephemeral=True)






@client.tree.command(name="transfer",description="انتقال سکه به کاربر دیگه 💰")
@app_commands.describe(amount="مقدار سکه جهت انتقال را وارد کنید")
@app_commands.describe(user="فرد موردنظر جهت انتقال سکه را وارد کنید")
async def transfer(interaction:Interaction,amount:int,user:Member):
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
    to = DataBase.cursor.fetchone()

    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    transporter = DataBase.cursor.fetchone()

    if transporter == None:
        sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        if to == None:
            sign_up(user_id=user.id)
            await interaction.response.send_message("**اطلاعات کاربری این کاربر در دیتابیس یافت نشد. عملیات ثبت نام این کاربر با موفقیت انجام شد لطفا دوباره از این کامند استفاده کنید. ✅**")
        else:
            if amount > transporter[1]:
                await interaction.response.send_message("**سکه های شما کمتر از مقدار موردنظر جهت انتقال است ❌**")
            else:
                try:
                    DataBase.cursor.execute(f"UPDATE table1 SET balance = {transporter[1] - amount} WHERE userid = {interaction.user.id}")
                    DataBase.connection.commit()
                    
                    DataBase.cursor.execute(f"UPDATE table1 SET balance = {to[1] + amount} WHERE userid = {user.id}")
                    DataBase.connection.commit()

                    await interaction.response.send_message(f"**مقدار `{amount}` سکه از کاربر {interaction.user.mention} کسر و به کاربر {user.mention} منتقل شد. ✅**")
                except Exception as error :
                    print(error)






@client.remove_command("help")
@client.tree.command(name="help",description="درباره بات و آموزشات 📚")
async def help(interaction:Interaction):

    get_started_embed = Embed(title="آموزش کار با بات و ثبت بنر تبلیغاتی 🤖",description="""
                              
                              
                              > ** برای ثبت بنر به چی نیاز دارم ؟ ❓**

                              خب اول از همه بگم برای ثبت بنر تبلیغاتی شما نیاز به سکه دارید!
                              اما چند تا ؟ شما نیاز به 500 سکه دارید.
                              در ابتدای شروع کار ما به شما 500 سکه هدیه میدیم 🎁

                              ----------------------------------------------------------------------------------

                              > ** چجوری سکه بگیرم؟ ❓**

                              اما برای به دست آوردن سکه شما میتوانید بنر های تبلیغاتی دیگران رو ببینید و از دکمه Seen زیر بنر هاشون استفاده کنید تا سکه بگیرید
                              با هر بار کلیک کردن روی دکمه Seen زیر بنر ها شما 10 سکه دریافت میکنید!

                              ----------------------------------------------------------------------------------

                              > ** از کجا بفهمم چند تاسکه دارم؟ ❓**

                              میتونید مقدار سکه هاتون رو با دستور `account_info/` مشاهده کنید.

                              ----------------------------------------------------------------------------------

                              > **چجوری بنرمو ثبت کنم؟ ❓**

                              خب اگر سکه هاتون کافی بود میتونید با استفاده از دستور `order/` بنر تبلیغاتیتون رو ثبت کنید.
                              به محض استفاده از این دستور پیامی مبنی بر قوانین ثبت بنر میبینید ، اون رو مطالعه کنید و روی دکمه میپذیرم کلیک کنید.
                              حالا یک صفحه فرم براتون باز میشه که میتونید توش بنر تبلیغاتیتون رو تایپ کپی پیست کنید.
                              فقط حواستون باشه که نمیتونید بیش از 4000 کاراکتر وارد کنید!
                              و حالا روی دکمه Submit کلیک کیند و بوم ...
                              بنر شما با موفقیت ثبت شد 😁 به همین سادگی 👌

                              ----------------------------------------------------------------------------------

                              > **داستان ریپورت چیه؟ ❓**

                              اگر شما قوانین ثبت بنر رو رعایت نکنید و کاربری بنر شما رو گزارش بده شما اخطار دریافت میکنید و بنرتون پاک میشه!
                              اگر این اخطار ها به 3 بار برسه متاسفانه شما برای همیشه از سرور بن میشید و نمیتونید دیگه از این خدمات استفاده کنید
                              راستی شما هم اگر بنر غیرمجازی رو دیدید میتونید گزارشش بدید ، گزارش ارسالی شما توسط تیم دیسکواد بررسی میشه و در صورت صحت گزارش 200 سکه به شما هدیه داده میشه 🤑
                              برای گزارش دادن هم کافیه از دکمه Report زیر بنر استفاده کنید.

                              ----------------------------------------------------------------------------------

                              > **میتونم سکه بخرم؟ ❓**

                              بله اگر حوصله مشاهده سایر بنر های تبلیغاتی رو ندارید میتونید مستقیما سکه بخرید و بنرتون رو ثبت کنید😊

                              ----------------------------------------------------------------------------------

                              > **محتوای بنرم چی میتونه باشه؟ ❓**

                              محتوای بنرتون میتونه شامل لینک اینوایت سرور دیسکورد ، تبلیغ یک سایت یا محصول ، ویدیوی یوتوب ، مدیا ، متن خالی و هر چیزی میتونه باشه.
                              البته در رابطه با لینک و مدیا یه سری قوانین هست که باید رعایت شه: مثلا لینک نباید لینک سایت های پورن و سایت های ممنوعه باشه و مدیا نباید حاوی محتوای جنسی یا ناجور باشه!

                              ----------------------------------------------------------------------------------

                              > **بنرم تا چه مدت باقی میمونه؟ ❓**

                              بنر شما در چنل <#1224577122555920405> 24 ساعت معادل یک شبانه روز کامل باقی میمونه و به صورت عمومی قابل مشاهده است.
                              بعد از این مدت بنر به صورت خودکار پاک میشه ♻

                            > ** لیست دستورات بات :**
""",color=Colour.blurple())
    get_started_embed.add_field(name="`/account_info`",value="**نمایش اطلاعات کاربری شما در سیستم بات و دیتابیس**",inline=False)
    get_started_embed.add_field(name="`/order`",value="**کامند اصلی بات جهت ثبت تبلیغات**",inline=False)
    get_started_embed.add_field(name="`/transfer`",value="**جهت انتقال سکه به سایر کاربران**",inline=False)

    help_embed = Embed(title=f" دیسکواد | DiscoAD 📢",
                       description="""** به دسیکواد خوش اومدی 🤗
                       دیسکواد یه بات تبلیغاتی توی دیسکورد هستش که میتونید با استفاده از اون سرور ، محصولات ، صفحات مجازی بنر تبلیغاتی و ... خود را به صورت کاملن رایگان تبلیغ کنید
                       این سیستم به شما کمک میکنه بتونید با تبلیغات گشترده ممبر ، مشتری ، ویو و ... جذب کنید.
                       به همین راحتی 😃
                       برای شروع کار میتونی از دکمه زیر استفاده کنی 👇**""",color=Colour.blurple())
    help_embed.set_footer(text="موفق باشی 😉")
    help_embed.set_author(name=interaction.user.display_name , icon_url=interaction.user.avatar.url)
    help_embed.set_thumbnail(url='https://png.pngtree.com/png-vector/20190826/ourmid/pngtree-marketing-png-image_1697508.jpg')
    
    get_started_button = Button(label="Get Started !",emoji="🔰",style=ButtonStyle.gray)
    


    async def get_started_button_callback(interaction:Interaction):
        await interaction.response.send_message(embed=get_started_embed,ephemeral=True)

    get_started_button.callback = get_started_button_callback




    help_view = View()
    help_view.add_item(get_started_button)
    
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    if item == None:
        sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        await interaction.response.send_message(embed=help_embed,view=help_view,ephemeral=True)







@client.tree.command(name='user_manager',description="مدیریت کاربر")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(user="کاربر موردنظر رو منشن کنید")
async def user_manager(interaction:Interaction,user:Member):
        DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
        show_item = DataBase.cursor.fetchone()
        #User Data
        try:
            user_balance = show_item[1]
            user_ads = show_item[2]
            user_warn = show_item[3]
        except:
            pass
        manager_embed = Embed(title="کاربر موردنظر با موفقیت از دیتابیس فچ شد",color=Colour.blurple())
        manager_embed.add_field(name="**🆔 UserID :**",value=user.id,inline=False)
        manager_embed.add_field(name="**👤 Mention :**",value=user.mention,inline=False)
        manager_embed.add_field(name="**💰 Coins :**",value=user_balance,inline=False)
        manager_embed.add_field(name="**🏷 Ads :**",value=user_ads,inline=False)
        manager_embed.add_field(name="**🛑 Warnings :**",value=user_warn,inline=False)
        manager_embed.set_footer(text="چه عملی انجام بدم؟ 😊")


        add_coin_button = Button(label="واریز سکه",emoji="➕",style=ButtonStyle.blurple)
        add_warn_button = Button(label="افزودن وارن",emoji="⚠",style=ButtonStyle.red)
        remove_coin_button = Button(label="برداشت سکه",emoji="➖",style=ButtonStyle.blurple)
        remove_user_button = Button(label="حذف کاربر",emoji="🗑",style=ButtonStyle.red)



        class AddCoinModal(Modal,title="واریز سکه"):
            add_amount = TextInput(label="چند سکه به کاربر واریز شه؟",required=True,style=TextStyle.short)
            
            async def on_submit(self,interaction:Interaction):
                DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                item = DataBase.cursor.fetchone()
                    #User Data
                    #try:
                        #user_balance = item[1]
                        #user_ads = item[2]
                        #user_warn = item[3]
                    #except:
                        #pass

                try:
                    DataBase.cursor.execute(f"UPDATE table1 SET balance = {item[1] + int(self.add_amount.value)} WHERE userid = {user.id}")
                    DataBase.connection.commit()
                    await interaction.response.send_message(f"**مقدار {self.add_amount} سکه به کاربر واریز شد. ✅**")
                except Exception as error:
                    await interaction.response.send_message("**در واریز سکه مشکلی پیش اومد ❌** {}".format(error))


        
        class RemoveCoinModal(Modal , title="برداشت سکه"):
            remove_amount = TextInput(label="چند سکه از کاربر برداشت شه؟",style=TextStyle.short)

            async def on_submit(self , interaction:Interaction):
                DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                item = DataBase.cursor.fetchone()
                    #User Data
                    #try:
                        #user_balance = item[1]
                        #user_ads = item[2]
                        #user_warn = item[3]
                    #except:
                        #pass
                try:
                    if  item[1]>= int(self.remove_amount.value):
                        DataBase.cursor.execute(f"UPDATE table1 SET balance = {item[1] - int(self.remove_amount.value)} WHERE userid = {user.id}")
                        DataBase.connection.commit()
                        await interaction.response.send_message(f"**مقدار {self.remove_amount} سکه از کاربر برداشت شد. ✅**")
                    else:
                        await interaction.response.send_message("**مقدار سکه کاربر از مقدار برداشت کمتر است ❌**")
                except Exception as error:
                        await interaction.response.send_message("**در برداشت سکه مشکلی پیش اومد ❌** {}".format(error))




        async def add_warn_button_callback(interaction:Interaction):
            try:
                DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                item = DataBase.cursor.fetchone()
                if item[3] + 1 == 3:
                    await user.ban(reason="رعایت نکردن قوانین ثبت بنر 🚫")
                    await interaction.response.send_message("**وارن های این کاربر به 3 تا رسید. کاربر با موفقیت بن شد ✅**")
                    DataBase.cursor.execute(f"DELETE FROM table1 WHERE userid = {user.id}")
                    DataBase.connection.commit()
                else:
                    DataBase.cursor.execute(f"UPDATE table1 SET warnings = {item[3] + 1} WHERE userid = {user.id}")
                    DataBase.connection.commit()
                    await interaction.response.send_message("**برای کاربر یک وارن افزوده شد ✅**")
            except Exception as error:
                await interaction.response.send_message("**در افزودن وارن مشکلی پیش اومد ❌**")
                print(error)


        async def add_coin_button_callback(interaction:Interaction):
            await interaction.response.send_modal(AddCoinModal())



        async def remove_coin_button_callback(interaction:Interaction):
            await interaction.response.send_modal(RemoveCoinModal())

        
        async def remove_user_button_callback(interaction:Interaction):
            confirm_view = View()
            confirm_embed = Embed(title="**آیا از حذف کاربر اطمینان دارید؟**",description="با انجام این کار تمامی اطلاعات کاربر از دیتابیس حذف میشود",color=Colour.blurple())
            yes_button = Button(label="بله",emoji="✔",style=ButtonStyle.green)
            no_button = Button(label="نه",emoji="✖",style=ButtonStyle.red)


            async def yes_button_callback(interaction:Interaction):
                try:
                    DataBase.cursor.execute(f"DELETE FROM table1 WHERE userid = {user.id}")
                    DataBase.connection.commit()
                    await interaction.response.send_message("**تمامی اطلاعات ماربر با موفقیت از دیتابیس پاک شد**",ephemeral=True)
                except:
                    await interaction.response.send_message("**در حذف کاربر خطایی رخ داد دوباره تلاش کنید ❌**",ephemeral=True)
            
            async def no_button_callback(interaction:Interaction):
                await interaction.response.send_message("**عملیات با موفقیت لغو شد✅**",ephemeral=True)


            yes_button.callback = yes_button_callback
            no_button.callback = no_button_callback

            confirm_view.add_item(yes_button)
            confirm_view.add_item(no_button)
            
            await interaction.response.send_message(embed=confirm_embed,view=confirm_view,ephemeral=True)

            

        add_coin_button.callback = add_coin_button_callback
        add_warn_button.callback = add_warn_button_callback
        remove_coin_button.callback = remove_coin_button_callback
        remove_user_button.callback = remove_user_button_callback

        user_manager_view = View()
        user_manager_view.add_item(add_coin_button)
        user_manager_view.add_item(remove_coin_button)
        user_manager_view.add_item(add_warn_button)
        user_manager_view.add_item(remove_user_button)


        await interaction.response.send_message(embed=manager_embed,view=user_manager_view)






client.run('MTIyNTc1ODQ5MTc3NjY1MTI2NA.Gkks-J.6a1oF1Rkcay5jCwnv6l6mMkMMmiwH3ZnXiD2PY')